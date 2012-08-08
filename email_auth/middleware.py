# -*- encoding: utf-8 -*-

from urllib import urlencode

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login
from django.contrib import messages
from django.utils.translation import ugettext as _

from email_auth.views import login as email_login

class EmailAuthMiddleware(object):
    """
    Middleware making sure that any auth request, including from
    the admin, uses the email auth backend.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Forwards any unauthenticated requests to our login url, 
        be it calls to django.contrib.auth.views.login or admin requests.
        """
        if view_func == login:
            return email_login(request, *view_args, **view_kwargs)

        if not view_func.__module__.startswith('django.contrib.admin'):
            return None

        # Now we know for sure the view_func belongs to the admin

        if request.user.is_authenticated():
            if request.user.is_staff:
                return None
            elif settings.LOGIN_REDIRECT_URL:
                message = _(
                    "Sorry, you are not allowed to access to %s" % request.path)
                messages.add_message(request, messages.WARNING, message)
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                error = (
                    _('<h1>Forbidden</h1><p>You do not have staff privileges.</p>'))
                return HttpResponseForbidden(error)

        params = urlencode({REDIRECT_FIELD_NAME: request.get_full_path()})
        url = reverse(email_login)
        url = reverse(getattr(settings, 'LOGIN_URL_MAP', email_login))
        return HttpResponseRedirect(url + '?' + params)
