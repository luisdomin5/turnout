import reversion
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.functional import cached_property

from common import enums
from common.fields import TurnoutEnumField
from common.utils.models import TimestampModel, UUIDModel
from reporting.models import StatsRefresh

DISCLAIMER_TEMPLATE = "multi_tenant/disclaimer.txt"


@reversion.register()
class Client(UUIDModel, TimestampModel):
    name = models.CharField(max_length=200)
    url = models.URLField(verbose_name="Homepage URL")
    email = models.EmailField(
        verbose_name="Default 'From' Email Address",
        max_length=254,
        null=True,
        default="hello@voteamerica.com",
    )
    privacy_policy = models.URLField(
        verbose_name="Privacy Policy URL", null=True, blank=True
    )
    terms_of_service = models.URLField(
        verbose_name="Terms of Service URL", null=True, blank=True
    )
    sms_enabled = models.BooleanField(
        verbose_name="SMS Program Enabled", default=True, null=True
    )
    sms_checkbox = models.BooleanField(
        verbose_name="SMS Checkbox Enabled", default=True, null=True
    )
    sms_checkbox_default = models.BooleanField(
        verbose_name="SMS Checkbox Checked By Default", default=False, null=True
    )
    sms_disclaimer = models.TextField(
        verbose_name="Custom SMS Disclaimer", blank=True, null=True
    )
    # In order to create this in the admin, we need blank=True
    default_slug = models.ForeignKey(
        "multi_tenant.SubscriberSlug", null=True, on_delete=models.PROTECT, blank=True
    )
    status = TurnoutEnumField(
        enums.SubscriberStatus, default=enums.SubscriberStatus.ACTIVE, null=True
    )

    # Passed to Civis to determine if subscriber's data should be synced to TMC
    sync_tmc = models.BooleanField(
        verbose_name="TMC Sync Enabled", default=False, null=True
    )
    sync_bluelink = models.BooleanField(
        verbose_name="Bluelink Sync Enabled", default=False, null=True
    )

    # Determines if we show our own donate asks when a user is interacting with
    # this client.
    is_first_party = models.BooleanField(default=False)

    has_api_access = models.BooleanField(default=False, null=True)

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
    def transactional_from_email_address(self) -> str:
        if self.is_first_party:
            return self.full_email_address
        clean_name = self.name.replace('"', "'")
        return f'"{clean_name} via VoteAmerica" <{settings.DEFAULT_EMAIL_FROM}>'

    @property
    def stats(self):
        refresh_obj = StatsRefresh.objects.all()[0]

        stats = {
            "last_updated": refresh_obj.last_run,
            "register": 0,
            "verify": 0,
            "absentee": 0,
            "locate": 0,
        }

        for stat in self.subscriberstats_set.all():
            stats[stat.tool.value] = stat.count

        return stats

    @cached_property
    def disclaimer(self):
        return render_to_string(DISCLAIMER_TEMPLATE, {"subscriber": self}).replace(
            "\n", ""
        )

    @cached_property
    def plan(self):
        if hasattr(self, "subscription"):
            return self.subscription.plan
        else:
            # System subscribers -- like VoteAmerica, and the dev Default one,
            # don't have subscriptions.
            return enums.SubscriberPlan.PREMIUM

    def plan_has_data_access(self):
        return self.plan != enums.SubscriberPlan.FREE

    def get_sms_mode(self):
        if not self.sms_enabled:
            return enums.SubscriberSMSOption.NONE
        if not self.sms_checkbox:
            return enums.SubscriberSMSOption.AUTO_OPT_IN
        if self.sms_checkbox_default:
            return enums.SubscriberSMSOption.BOX_CHECKED
        else:
            return enums.SubscriberSMSOption.BOX_UNCHECKED

    def set_sms_mode(self, opt):
        if opt == str(enums.SubscriberSMSOption.NONE):
            self.sms_enabled = False
            self.sms_checkbox = False
            self.sms_checkbox_default = False
        elif opt == str(enums.SubscriberSMSOption.AUTO_OPT_IN):
            self.sms_enabled = True
            self.sms_checkbox = False
            self.sms_checkbox_default = False
        elif opt == str(enums.SubscriberSMSOption.BOX_UNCHECKED):
            self.sms_enabled = True
            self.sms_checkbox = True
            self.sms_checkbox_default = False
        elif opt == str(enums.SubscriberSMSOption.BOX_CHECKED):
            self.sms_enabled = True
            self.sms_checkbox = True
            self.sms_checkbox_default = True


class SubscriberSlug(UUIDModel, TimestampModel):
    subscriber = models.ForeignKey(
        Client, on_delete=models.CASCADE, db_column="partner_id"
    )
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "multi_tenant_partnerslug"

    def __str__(self):
        return self.slug


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
