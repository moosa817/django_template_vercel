from guest_user.views import ConvertFormView
from ..forms import ProfileCreationForm
from ..models import UserProfile
from django.conf import settings as django_settings
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, get_user_model, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.module_loading import import_string
from django.views.generic import FormView, TemplateView
from django.shortcuts import render
from django.conf import settings
from guest_user.exceptions import NotGuestError
from guest_user.functions import get_guest_model, is_guest_user
from guest_user.mixins import GuestUserRequiredMixin


class CustomConvertFormView(GuestUserRequiredMixin, ConvertFormView):
    anonymous_url = "/login/"
    registered_url = "/"
    template_name = 'base/convert_guest.html'

    def get_success_url(self):
        return 'guest_user_convert_success'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ProfileForm = ProfileCreationForm()
        context.update(
            {self.redirect_field_name: self.get_redirect_url(), 'ProfileForm': ProfileCreationForm})
        return context

    def form_valid(self, form):
        """Security check complete. Log the user in."""

        GuestModel = get_guest_model()

        profileForm = ProfileCreationForm(self.request.POST)
        if profileForm.is_valid():
            try:
                GuestModel.objects.convert(form)
            except NotGuestError:
                # Redirect if it's already a regular user.
                pass
            else:
                # Authenticate the user with standard backend.

                user = User.objects.get(
                    username=self.request.POST.get('username'))
                profile = UserProfile.objects.create(
                    username=user,
                    email=self.request.POST.get('email').lower(),
                )
                login(self.request, authenticate(
                    self.request, **form.get_credentials()))

                return redirect(self.get_success_url())

        context = super().get_context_data()
        context['ProfileForm'] = profileForm

        return render(self.request, template_name=self.template_name, context=context)


custom_convert_form = CustomConvertFormView.as_view()
