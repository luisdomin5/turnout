import logging

import requests
from django.conf import settings

from common.apm import tracer
from election.models import StateInformation

MONITOR = {
    "external_tool_polling_place": "Polling Place Lookup",
    "external_tool_ovr": "Online Voter Registration",
    "external_tool_verify_status": "Voter Registration Status Verifier",
    "external_tool_vbm_application": "Absentee Ballot Request",
    "external_tool_absentee_ballot_tracker": "Absentee Ballot Tracker",
}

logger = logging.getLogger("integration")


@tracer.wrap()
def config_uptime():
    sites = {}  # description -> {url, metadata}
    for slug, slug_desc in MONITOR.items():
        for item in StateInformation.objects.filter(field_type__slug=slug):
            # some values are blank
            if not item.text:
                continue

            desc = f"{item.state_id} {slug_desc}"
            sites[desc] = {
                "url": item.text,
                "description": desc,
                "metadata": {"state_id": item.state_id, "slug": slug, "active": True,},
            }

    # list our existing sites
    session = requests.Session()
    session.auth = requests.auth.HTTPBasicAuth(
        settings.UPTIME_USER, settings.UPTIME_SECRET
    )

    nexturl = f"{settings.UPTIME_URL}/v1/uptime/sites-mine/"
    while nexturl:
        response = session.get(nexturl)
        response.raise_for_status()
        nexturl = response.json().get("next")

        for item in response.json().get("results", []):
            if item["description"] in sites:
                want = sites[item["description"]]
                if item["url"] != want["url"] or item["metadata"] != want["metadata"]:
                    logger.info(f"Updating {want}")
                    session.put(
                        f"{settings.UPTIME_URL}/v1/uptime/sites/{item['uuid']}/",
                        json=want,
                    )
                del sites[item["description"]]
            else:
                logger.info(f"Disabling {item['description']}")
                session.put(
                    f"{settings.UPTIME_URL}/v1/uptime/sites/{item['uuid']}/",
                    json={"active": False},
                )

    # add missing sites
    for desc, item in sites.items():
        logger.info(f"Adding {item}")
        response = session.post(f"{settings.UPTIME_URL}/v1/uptime/sites/", json=item)
        response.raise_for_status()
