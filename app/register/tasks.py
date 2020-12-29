from celery import shared_task
from django.conf import settings

from common.analytics import statsd
from common.enums import EventType, TurnoutActionStatus
from mailer.retry import EMAIL_RETRY_PROPS


# DEPRECATED.
# TODO: Delete this -- leaving it in for now so in-flight tasks don't fail
# during the deploy.
@shared_task
@statsd.timed("turnout.register.process_registration_submission")
def process_registration_submission(
    registration_pk: str, state_id_number: str, is_18_or_over: bool
) -> None:
    from .models import Registration
    from .generateform import process_registration

    registration = Registration.objects.select_related().get(pk=registration_pk)
    process_registration(registration, state_id_number, is_18_or_over)


@shared_task(**EMAIL_RETRY_PROPS)
@statsd.timed("turnout.register.send_registration_notification")
def send_registration_notification(registration_pk: str) -> None:
    from .models import Registration
    from .notification import trigger_notification

    registration = Registration.objects.select_related().get(pk=registration_pk)
    registration.status = TurnoutActionStatus.PDF_SENT
    registration.save(update_fields=["status"])
    if registration.result_item_mail:
        registration.action.track_event(EventType.FINISH_LOB)

        # nag them in a few minutes
        send_print_and_forward_confirm_nag.apply_async(
            (registration.uuid,), countdown=settings.REGISTER_LOB_CONFIRM_NAG_SECONDS
        )
    else:
        registration.action.track_event(EventType.FINISH_SELF_PRINT)

    trigger_notification(registration)


@shared_task(**EMAIL_RETRY_PROPS)
@statsd.timed("turnout.register.send_registration_state_confirmation")
def send_registration_state_confirmation(registration_pk: str) -> None:
    from .models import Registration
    from .notification import trigger_state_confirmation

    registration = Registration.objects.select_related().get(pk=registration_pk)
    trigger_state_confirmation(registration)


@shared_task(**EMAIL_RETRY_PROPS)
@statsd.timed("turnout.register.send_registration_reminder")
def send_registration_reminder(registration_pk: str) -> None:
    from .models import Registration
    from .notification import trigger_reminder

    registration = Registration.objects.select_related().get(pk=registration_pk)

    if registration.result_item_mail:
        event_type = EventType.FINISH_LOB_CONFIRM
    else:
        event_type = EventType.DOWNLOAD
    if registration.action.event_set.filter(event_type=event_type).exists():
        return

    trigger_reminder(registration)


@shared_task(**EMAIL_RETRY_PROPS)
@statsd.timed("turnout.register.send_print_and_forward_nag")
def send_print_and_forward_confirm_nag(registration_pk: str) -> None:
    from smsbot.tasks import send_welcome_sms
    from .models import Registration
    from .notification import trigger_print_and_forward_confirm_nag

    registration = Registration.objects.select_related().get(pk=registration_pk)
    send_welcome_sms(str(registration.phone), "register")
    if registration.action.event_set.filter(
        event_type=EventType.FINISH_LOB_CONFIRM
    ).exists():
        return
    trigger_print_and_forward_confirm_nag(registration)


@shared_task(queue="high-pri", **EMAIL_RETRY_PROPS)
@statsd.timed("turnout.register.external_tool_upsell")
def external_tool_upsell(registration_pk: str) -> None:
    from .models import Registration
    from .notification import trigger_external_tool_upsell
    from smsbot.tasks import send_welcome_sms

    registration = Registration.objects.select_related().get(pk=registration_pk)
    send_welcome_sms(str(registration.phone), "register")
    trigger_external_tool_upsell(registration)


@shared_task(**EMAIL_RETRY_PROPS)
@statsd.timed("turnout.register.print_and_forward_mailed")
def send_print_and_forward_mailed(registration_pk: str, action_pk: str = None) -> None:
    from .models import Registration
    from .notification import trigger_print_and_forward_mailed
    from smsbot.tasks import send_welcome_sms

    registration = Registration.objects.select_related().get(pk=registration_pk)
    send_welcome_sms(str(registration.phone), "register")
    trigger_print_and_forward_mailed(registration)


@shared_task(**EMAIL_RETRY_PROPS)
@statsd.timed("turnout.register.print_and_forward_returned")
def send_print_and_forward_returned(
    registration_pk: str, action_pk: str = None
) -> None:
    from .models import Registration
    from .notification import trigger_print_and_forward_returned
    from smsbot.tasks import send_welcome_sms

    registration = Registration.objects.select_related().get(pk=registration_pk)
    send_welcome_sms(str(registration.phone), "register")
    trigger_print_and_forward_returned(registration)


@shared_task(**EMAIL_RETRY_PROPS)
@statsd.timed("turnout.register.mail_chase")
def send_mail_chase(registration_pk: str, action_pk: str = None) -> None:
    from .models import Registration
    from .notification import trigger_mail_chase
    from smsbot.tasks import send_welcome_sms

    registration = Registration.objects.select_related().get(pk=registration_pk)
    send_welcome_sms(str(registration.phone), "register")
    trigger_mail_chase(registration)


@shared_task()
@statsd.timed("turnout.register.publish_pa_counties")
def publish_pa_counties() -> None:
    from .pa import sync_counties_to_s3

    sync_counties_to_s3()
