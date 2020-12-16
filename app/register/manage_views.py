from django.views.generic import DetailView, ListView

from action.mixin_manage_views import ActionListViewMixin
from common.utils.uuid_slug_mixin import UUIDSlugMixin
from multi_tenant.mixins_manage_views import (
    SubscriberDataViewMixin,
    SubscriberGenericViewMixin,
)

from .models import Registration


class RegistrationListView(
    SubscriberGenericViewMixin, SubscriberDataViewMixin, ActionListViewMixin, ListView,
):
    model = Registration
    context_object_name = "registrations"
    template_name = "register/manage/registration_list.html"


class RegistrationDetailView(
    SubscriberGenericViewMixin, SubscriberDataViewMixin, UUIDSlugMixin, DetailView,
):
    model = Registration
    context_object_name = "registration"
    template_name = "register/manage/registration_detail.html"
    slug_field = "uuid"
