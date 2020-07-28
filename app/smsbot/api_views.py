import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from common.analytics import statsd
from common.enums import MessageDirectionType
from smsbot.models import Number, SMSMessage

"""
Twilio's advanced opt-in should be configured with these messages:

-- Opt-out --
Default keywords: stop
Extra keywords:

  You will no longer receive messages from VoteAmerica. Goodbye! Reply HELP for help, JOIN to join.

-- Opt-in --
Default keywords: start, unstop
Extra keywords: join, yes

  Welcome back!

(Twilio will send this *only* if they previously opted-out.)
(The bot will send more instructions below)

-- Help --
Default keywords: help

  Reply YES to receive VoteAmerica Election Alerts.
  Msg & Data Rates May Apply. 4 msgs/month.
  Reply HELP for help, STOP to cancel.

"""


def proxy_twilio_request(request, target):
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    sig = validator.compute_signature(target, request.data)
    response = requests.post(
        target, headers={"X-Twilio-Signature": sig}, data=request.data,
    )
    statsd.increment("turnout.smsbot.proxy_twilio_webhook")
    return HttpResponse(
        response.text,
        status=response.status_code,
        content_type=response.headers["content-type"],
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def twilio(request):
    number = request.data.get("From", None)
    body = request.data.get("Body", "")
    if not number:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    if settings.TWILIO_ENDPOINT_IS_HTTPS:
        url = "https://"
    else:
        url = "http://"
    url += request.META["HTTP_HOST"] + request.get_full_path()
    if not validator.validate(
        url, request.data, request.headers.get("X-Twilio-Signature", ""),
    ):
        return HttpResponse("Bad twilio signature", status=status.HTTP_403_FORBIDDEN)

    try:
        n = Number.objects.get(phone=number)
    except ObjectDoesNotExist:
        n = None

    SMSMessage.objects.create(
        phone=number, direction=MessageDirectionType.IN, message=body,
    )

    cmd = body.lower().strip()
    if cmd in ["help"]:
        # Twilio advanced opt-in will always respond here.
        reply = None
    elif cmd in ["join"]:
        # Twilio advanced opt-in will respond here *if* they previously opted out.
        # We'll send an additional message either way.
        if n and n.opt_in_time:
            reply = (
                "You have already signed up for VoteAmerica Election Alerts. "
                "Reply HELP for help, STOP to cancel."
            )
        else:
            reply = (
                "Reply YES to join VoteAmerica and receive Election Alerts. "
                "Msg & Data rates may apply. 4 msgs/month. "
                "Reply HELP for help, STOP to cancel."
            )
    elif cmd in ["yes"]:
        if n and n.opt_in_time:
            reply = (
                "You have already signed up for VoteAmerica Election Alerts. "
                "Reply HELP for help, STOP to cancel."
            )
        else:
            reply = (
                "Thanks for joining VoteAmerica Election Alerts! "
                "Msg & Data rates may apply. 4 msgs/month. "
                "Reply HELP for help, STOP to cancel."
            )
            if not n:
                n = Number(phone=number)
            n.opt_in_time = timezone.now()
            n.opt_out_time = None
            n.save()
    elif cmd in ["stop"]:
        # Twilio advanced opt-in will always respond here.
        reply = None
        if not n:
            n = Number(phone=number)
        n.opt_out_time = timezone.now()
        n.opt_in_time = None
        n.save()
    else:
        if n and n.opt_in_time:
            reply = (
                "Hi, I am the VoteAmerica chat bot. Nice to hear from you again!\n"
                "HELP for help, STOP to cancel."
            )
        elif n and n.opt_out_time:
            # Twilio won't let them see this, but we can try anyway in case we are
            # out of sync with twilio's blacklist.
            reply = (
                "Hi, I am the VoteAmerica chat bot. "
                "You have previously opted-out of our Election Alerts list. "
                "Reply HELP for help, JOIN to join."
            )
        else:
            # We got a random message from an unknown number.
            reply = (
                "Hi, I am the VoteAmerica chat bot. "
                "Reply YES to join VoteAmerica and receive Election Alerts. "
                "Msg & Data rates may apply. 4 msgs/month. "
                "Reply HELP for help, STOP to cancel."
            )

    if settings.TWILIO_PROXY_TO:
        return proxy_twilio_request(request, settings.TWILIO_PROXY_TO)

    statsd.increment("turnout.smsbot.twilio_webhook")
    if reply:
        SMSMessage.objects.create(
            phone=number, direction=MessageDirectionType.OUT, message=reply,
        )

    resp = MessagingResponse()
    if reply:
        resp.message(reply)
    return HttpResponse(str(resp))
