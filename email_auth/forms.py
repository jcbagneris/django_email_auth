# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm as OriginalAuthForm
from django.utils.translation import ugettext_lazy as _

class AuthenticationForm(OriginalAuthForm):
    """
    Form for authenticating users on email/password credentials.
    The difference with the original Form from contrib.auth.forms
    is the use of the email field instead of username.
    See doctests in the tests.py module.
    """
    # username has to be there to override required field from orig auth form
    username = forms.CharField(required=False)
    email = forms.EmailField(label=_("Email"), max_length=75)
    remember = forms.BooleanField( label=_("Remember me on this computer"), 
            required=False)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Please enter a correct email and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        else:
            raise forms.ValidationError(
                _("Please enter a correct email and password. Note that both fields are case-sensitive."))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(
                    _("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data

