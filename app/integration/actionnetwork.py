import logging

import requests
import sentry_sdk
from django.conf import settings
from django.core.cache import cache
from django.db.models import Exists, OuterRef

from absentee.models import BallotRequest
from common.apm import tracer
from common.enums import ExternalToolType
from multi_tenant.models import SubscriberIntegrationProperty
from register.models import Registration
from reminder.models import ReminderRequest
from verifier.models import Lookup

from .models import Link

FORM_ENDPOINT = "https://actionnetwork.org/api/v2/forms/"
ADD_ENDPOINT = "https://actionnetwork.org/api/v2/forms/{form_id}/submissions/"

logger = logging.getLogger("integration")

# actionnetwork ids must be lowercase, so we need both lower and CamelCase here
ACTIONS = {
    "lookup": "Lookup",
    "register": "Register",
    "ballotrequest": "BallotRequest",
    "reminderrequest": "ReminderRequest",
}

CACHE_KEY = "actionnetwork-forms"


class ActionNetworkError(Exception):
    pass


def get_api_key(subscriber_id):
    if subscriber_id:
        api_key = None
        for key in SubscriberIntegrationProperty.objects.filter(
            subscriber_id=subscriber_id,
            external_tool=ExternalToolType.ACTIONNETWORK,
            name="api_key",
        ):
            return key.value
        if not api_key:
            return None
    return settings.ACTIONNETWORK_KEY


def get_form_ids(ids, prefix):
    an_id = None
    va_action = None
    for gid in ids:
        (org, pid) = gid.split(":")
        if org == "action_network":
            an_id = pid
        elif org == "voteamerica" and pid.startswith(prefix + "_"):
            va_action = pid[len(prefix) + 1 :]
    return an_id, va_action


def setup_action_forms(subscriber_id):
    if subscriber_id:
        key = f"{CACHE_KEY}-{subscriber_id}"
    else:
        key = CACHE_KEY

    forms = cache.get(key) or {}
    missing = False
    for action in ACTIONS.keys():
        if action not in forms:
            missing = True
    if not missing:
        return forms

    logger.info(f"Fetching forms from ActionNetwork for subscriber {subscriber_id}")
    api_key = get_api_key(subscriber_id)
    prefix = settings.ACTIONNETWORK_FORM_PREFIX
    forms = {}
    with tracer.trace("an.form", service="actionnetwork"):
        nexturl = FORM_ENDPOINT
        while nexturl:
            logger.info(nexturl)
            response = requests.get(nexturl, headers={"OSDI-API-Token": api_key},)
            for form in response.json()["_embedded"]["osdi:forms"]:
                an_id, va_action = get_form_ids(form["identifiers"], prefix)
                if an_id and va_action:
                    forms[va_action] = an_id
            nexturl = response.json().get("_links", {}).get("next", {}).get("href")

    for action, action_desc in ACTIONS.items():
        if action not in forms:
            # This code runs once per action, ever.
            logger.info(f"Creating action form for {action_desc} ({prefix})")
            with tracer.trace("an.form.create", service="actionnetwork"):
                response = requests.post(
                    FORM_ENDPOINT,
                    headers={"OSDI-API-Token": api_key},
                    json={
                        "identifiers": [f"voteamerica:{prefix}_{action}"],
                        "title": f"VoteAmerica {action_desc} ({prefix})",
                        "origin_system": "voteamerica",
                    },
                )
                logger.info(response.json())
                an_id, va_action = get_form_ids(response.json()["identifiers"], prefix)
                if an_id and va_action:
                    forms[va_action] = an_id

    cache.set(key, forms, settings.ACTIONNETWORK_FORM_CACHE_TIMEOUT)

    return forms


def post_person(info, form_id, api_key):
    from common.apm import tracer

    url = ADD_ENDPOINT.format(form_id=form_id)
    with tracer.trace("an.form.submission", service="actionnetwork"):
        try:
            response = requests.post(
                url, json=info, headers={"OSDI-API-Token": api_key},
            )
        except Exception as e:
            extra = {"url": url, "info": info, "exception": str(e)}
            logger.error(
                "actionnetwork: Error posting to %(url)s, info %(info)s, exception %(exception)s",
                extra,
                extra=extra,
            )
            sentry_sdk.capture_exception(
                ActionNetworkError(f"Error posting to {url}, exception {str(e)}")
            )
            return None
    if response.status_code != 200:
        extra = {"url": url, "info": info, "status_code": response.status_code}
        logger.info(response.text)
        logger.error(
            "actionnetwork: Error posting to %(url)s, info %(info)s, status_code %(status_code)s",
            extra,
            extra=extra,
        )
        sentry_sdk.capture_exception(
            ActionNetworkError(
                f"Error posting to {url}, status code {response.status_code}"
            )
        )
        return None

    # return link to the *person*, not the submission
    return response.json()["_links"]["osdi:person"]["href"].split("/")[-1]


@tracer.wrap()
def sync_item(item):
    if settings.ACTIONNETWORK_SYNC and item.action:
        _sync_item(item, None)
        _sync_item(item, item.subscriber_id)


def _sync_item(item, subscriber_id):
    api_key = get_api_key(subscriber_id)
    if not api_key:
        return

    forms = setup_action_forms(subscriber_id)
    action = str(item.__class__.__name__).lower()
    form_id = forms.get(action)

    extra = {"subscriber_id": subscriber_id, "item": item}
    logger.info(
        f"actionnetwork: Sync %(item)s, subscriber %(subscriber_id)s",
        extra,
        extra=extra,
    )
    external_id = post_person(
        {
            "person": {
                "identifiers": [f"voteamerica_action:{item.action_id.hex_grouped}"],
                "given_name": item.first_name,
                "family_name": item.last_name,
                "email_addresses": [{"address": item.email}],
                "postal_addresses": [
                    {
                        "address_lines": [item.address1, item.address2],
                        "locality": item.city,
                        "region": item.state_id,
                        "postal_code": item.zipcode,
                        "country": "US",
                    },
                ],
            },
            "action_network:referrer_data": {
                "source": item.source or f"voteamerica_{action}",
                "website": item.embed_url,
                "email_referrer": item.email_referrer,
                "mobile_referrer": item.mobile_referrer,
            },
        },
        form_id,
        api_key,
    )
    if external_id:
        Link.objects.create(
            action_id=item.action_id,
            subscriber_id=subscriber_id,
            external_tool=ExternalToolType.ACTIONNETWORK,
            external_id=external_id,
        )


def sync_all_items(cls):
    for item in (
        cls.objects.annotate(
            no_sync=~Exists(
                Link.objects.filter(
                    subscriber_id=None,
                    external_tool=ExternalToolType.ACTIONNETWORK,
                    action=OuterRef("action"),
                )
            )
        )
        .filter(no_sync=True, action__isnull=False)
        .order_by("created_at")
    ):
        _sync_item(item, None)

    for item in (
        cls.objects.annotate(
            no_sync=~Exists(
                Link.objects.filter(
                    subscriber_id=OuterRef("subscriber"),
                    external_tool=ExternalToolType.ACTIONNETWORK,
                    action=OuterRef("action"),
                )
            )
        )
        .filter(no_sync=True, action__isnull=False)
        .order_by("created_at")
    ):
        _sync_item(item, item.subscriber_id)


@tracer.wrap()
def sync():
    sync_all_items(Lookup)
    sync_all_items(BallotRequest)
    sync_all_items(Registration)
    sync_all_items(ReminderRequest)
