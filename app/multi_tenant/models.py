import reversion
from django.core.cache import cache
from django.db import models
from django.template.loader import render_to_string
from django.utils.functional import cached_property

from common import enums
from common.fields import TurnoutEnumField
from common.utils.models import TimestampModel, UUIDModel

DISCLAIMER_TEMPLATE = "multi_tenant/disclaimer.txt"


@reversion.register()
class Client(UUIDModel, TimestampModel):
    name = models.CharField(max_length=200)
    url = models.URLField()
    email = models.EmailField(
        max_length=254, null=True, default="turnout@localhost.local"
    )
    privacy_policy = models.URLField(null=True, blank=True)
    terms_of_service = models.URLField(null=True, blank=True)
    sms_enabled = models.BooleanField(default=True, null=True)
    sms_checkbox = models.BooleanField(default=True, null=True)
    sms_checkbox_default = models.BooleanField(default=False, null=True)
    sms_disclaimer = models.TextField(blank=True, null=True)
    # In order to create this in the admin, we need blank=True
    default_slug = models.ForeignKey(
        "multi_tenant.SubscriberSlug", null=True, on_delete=models.PROTECT, blank=True
    )

    # Passed to Civis to determine if subscriber's data should be synced to TMC
    sync_tmc = models.BooleanField(default=False, null=True)
    sync_bluelink = models.BooleanField(default=False, null=True)

    # Determines if we show our own donate asks when a user is interacting with
    # this client.
    is_first_party = models.BooleanField(default=False)

    active = models.BooleanField(null=True)
    active_subscription = models.ForeignKey(
        "multi_tenant.SubscriptionInterval", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return self.name

    @cached_property
    def slug(self):
        return self.default_slug.slug

    @property
    def full_email_address(self) -> str:
        clean_name = self.name.replace('"', "'")
        return f'"{clean_name}" <{self.email}>'

    @property
    def stats(self):
        # NOTE: callers should be able to cope with getting an empty dict here
        return cache.get(f"client.stats/{self.uuid}") or {}

    @cached_property
    def disclaimer(self):
        return render_to_string(DISCLAIMER_TEMPLATE, {"subscriber": self}).replace(
            "\n", ""
        )


class SubscriberSlug(UUIDModel, TimestampModel):
    subscriber = models.ForeignKey(
        Client, on_delete=models.CASCADE, db_column="partner_id"
    )
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "multi_tenant_partnerslug"

    def __str__(self):
        return self.slug


class SubscriptionInterval(UUIDModel, TimestampModel):
    subscriber = models.ForeignKey(Client, on_delete=models.CASCADE)
    begin = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)


class Association(UUIDModel, TimestampModel):
    client = models.ForeignKey("multi_tenant.Client", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)


class InviteAssociation(UUIDModel, TimestampModel):
    client = models.ForeignKey("multi_tenant.Client", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.Invite", on_delete=models.CASCADE)


class SubscriberIntegrationProperty(UUIDModel, TimestampModel):
    subscriber = models.ForeignKey(Client, on_delete=models.CASCADE,)
    external_tool = TurnoutEnumField(enums.ExternalToolType, null=True)
    name = models.TextField(null=True)
    value = models.TextField(null=True)

    class Meta:
        ordering = ["-created_at"]


class SubscriberLead(UUIDModel, TimestampModel):
    name = models.CharField(max_length=200)
    url = models.URLField()
    email = models.EmailField(max_length=254, null=True)
    slug = models.CharField(max_length=40, null=True)

    is_c3 = models.BooleanField(null=True)

    status = TurnoutEnumField(enums.SubscriberLeadStatus, null=True)

    subscriber = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    stripe_customer_id = models.TextField(null=True)

    class Meta:
        ordering = ["-created_at"]
