import uuid

import tsvector_field
from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class UUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta(object):
        abstract = True


class TrackingModel(models.Model):
    embed_url = models.TextField(null=True, blank=True)
    utm_campaign = models.TextField(null=True, blank=True)
    utm_source = models.TextField(null=True, blank=True)
    utm_medium = models.TextField(null=True, blank=True)
    utm_term = models.TextField(null=True, blank=True)
    utm_content = models.TextField(null=True, blank=True)
    session_id = models.UUIDField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)

    # Fields needed for ActionNetwork email and SMS integration
    email_referrer = models.TextField(null=True, blank=True)
    mobile_referrer = models.TextField(null=True, blank=True)

    def action_was_embedded(self) -> bool:
        return not self.embed_url.lower().startswith("https://www.voteamerica.com")

    class Meta(object):
        abstract = True


def SearchableModel(*args):
    fields = [tsvector_field.WeightedColumn(name, "A") for name in args]

    class SearchBase(models.Model):
        search = tsvector_field.SearchVectorField(fields, "english")

        class Meta(object):
            abstract = True

    return SearchBase
