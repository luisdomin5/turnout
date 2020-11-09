import math

import reversion
from django.contrib.postgres.fields import JSONField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from action.mixin_models import ActionModel
from common import enums
from common.fields import TurnoutEnumField
from common.utils.models import (
    SearchableModel,
    TimestampModel,
    TrackingModel,
    UUIDModel,
)
from common.validators import zip_validator
from multi_tenant.mixins_models import SubscriberModel


class BallotRequest(
    ActionModel,
    SubscriberModel,
    TrackingModel,
    SearchableModel("email", "last_name", "first_name"),  # type: ignore
    UUIDModel,
    TimestampModel,
):
    first_name = models.TextField(null=True)
    middle_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True)
    suffix = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(null=True)
    phone = PhoneNumberField(null=True, blank=True, db_index=True)
    address1 = models.TextField(null=True)
    address2 = models.TextField(null=True, blank=True)
    city = models.TextField(null=True)
    state = models.ForeignKey(
        "election.State",
        on_delete=models.PROTECT,
        related_name="absentee_primary",
        null=True,
    )
    zipcode = models.TextField(null=True, validators=[zip_validator])
    deliverable = models.BooleanField(null=True)

    mailing_address1 = models.TextField(null=True, blank=True)
    mailing_address2 = models.TextField(null=True, blank=True)
    mailing_city = models.TextField(null=True, blank=True)
    mailing_state = models.ForeignKey(
        "election.State",
        on_delete=models.PROTECT,
        related_name="absentee_mailing",
        null=True,
    )
    mailing_zipcode = models.TextField(
        null=True, validators=[zip_validator], blank=True
    )
    mailing_deliverable = models.BooleanField(null=True)

    request_mailing_address1 = models.TextField(null=True, blank=True)
    request_mailing_address2 = models.TextField(null=True, blank=True)
    request_mailing_city = models.TextField(null=True, blank=True)
    request_mailing_state = models.ForeignKey(
        "election.State",
        on_delete=models.PROTECT,
        related_name="absentee_request_mailing",
        null=True,
    )
    request_mailing_zipcode = models.TextField(
        null=True, validators=[zip_validator], blank=True
    )
    request_mailing_deliverable = models.BooleanField(null=True)

    us_citizen = models.BooleanField(null=True, default=False)
    sms_opt_in = models.BooleanField(null=True, default=False)

    state_fields = JSONField(null=True)

    status = TurnoutEnumField(
        enums.TurnoutActionStatus, default=enums.TurnoutActionStatus.PENDING, null=True,
    )

    region = models.ForeignKey("official.Region", null=True, on_delete=models.SET_NULL)

    result_item = models.ForeignKey(
        "storage.StorageItem", null=True, on_delete=models.SET_NULL
    )
    result_item_mail = models.ForeignKey(
        "storage.StorageItem",
        null=True,
        on_delete=models.SET_NULL,
        related_name="absentee_mail",
    )

    signature = models.ForeignKey(
        "storage.SecureUploadItem", null=True, on_delete=models.SET_NULL
    )

    submit_date = models.DateField(null=True)

    esign_method = TurnoutEnumField(enums.SubmissionType, null=True)

    referring_tool = TurnoutEnumField(enums.ToolName, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Absentee - {self.first_name} {self.last_name}, {self.state.pk}".strip()

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


@reversion.register()
class LeoContactOverride(TimestampModel):
    region = models.OneToOneField(
        "official.Region", on_delete=models.CASCADE, primary_key=True
    )
    submission_method = TurnoutEnumField(enums.SubmissionType, null=True)
    email = models.EmailField(null=True)
    phone = PhoneNumberField(null=True)
    fax = PhoneNumberField(null=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["region__state__code", "region__name"]


class RegionOVBMLink(TimestampModel):
    region = models.OneToOneField(
        "official.Region", on_delete=models.CASCADE, primary_key=True
    )
    url = models.URLField()

    class Meta:
        ordering = ["region__state__code", "region__name"]


class RegionEsignMethod(models.Model):
    region = models.OneToOneField(
        "official.Region",
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_name="esign",
    )

    state = models.ForeignKey("election.State", on_delete=models.DO_NOTHING)

    has_override = models.BooleanField()
    submission_method = TurnoutEnumField(enums.SubmissionType)

    class Meta:
        managed = False
        ordering = ["state_id", "region__name"]


class StateDashboardData(models.Model):
    state = models.OneToOneField(
        "election.State",
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_name="absentee_dashboard_data",
    )

    has_statewide_link = models.BooleanField()
    num_region_links = models.IntegerField()
    fax_allowed = models.BooleanField()
    email_allowed = models.BooleanField()
    num_regions = models.IntegerField()
    num_regions_email = models.IntegerField()
    num_regions_fax = models.IntegerField()
    num_regions_self_print = models.IntegerField()
    num_regions_with_override = models.IntegerField()

    def region_coverage_percentage(self):
        return "%.1d%%" % (
            math.floor(
                (self.num_regions_email + self.num_regions_fax) / self.num_regions * 100
            )
        )

    class Meta:
        managed = False
        ordering = ["state_id"]


class EsignSubmitStats(models.Model):
    region = models.OneToOneField(
        "official.Region",
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_name="esign_stats",
    )

    state = models.ForeignKey("election.State", on_delete=models.DO_NOTHING)

    emails_sent_7d = models.IntegerField()
    faxes_sent_7d = models.IntegerField()
    forms_sent_7d = models.IntegerField()
    emails_sent_1d = models.IntegerField()
    faxes_sent_1d = models.IntegerField()
    forms_sent_1d = models.IntegerField()

    class Meta:
        managed = False
        ordering = ["state_id", "region__name"]
