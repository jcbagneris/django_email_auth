# -*- encoding: utf-8 -*-

import datetime
from urllib import quote

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import iri_to_uri
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site
from django.template import RequestContext

from forms import AuthForm

def login(request, template_name='registration/login.html'):
    """
    Displays the login form and handles the email-based login action.
    Adapted from django.contrib.auth.views.login
    Sets a "remember me" cookie.
    """
    redirect_to = request.REQUEST.get('next', '')
    if request.method == "POST":
        form = AuthForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            response = HttpResponse()
            # traiter cookie "remember me"
            if form.cleaned_data['remember']:
                cookie_data = encodestring('%s:%s' % 
                    (form.cleaned_data['username'], 
                    form.cleaned_data['password']))
                max_age = 30*24*60*60
                expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
                response.set_cookie('eMaster', 
                        cookie_data, max_age=max_age, expires=expires)
            else:
                # effacer le cookie s'il existe
                response.delete_cookie('eMaster')
            # retourner à la vue appelante
            if redirect_to:
                response.status_code = 302
                response['Location'] = iri_to_uri(redirect_to)
                return response
            else:
                response.status_code = 302
                response['Location'] = settings.LOGIN_REDIRECT_URL
                return response
    else:
        # recup login cookie s'il existe
        if 'eMaster' in request.COOKIES:
            cookie_data = decodestring(request.COOKIES['eMaster'])
            try:
                l,p = cookie_data.split(':')
            except ValueError:
                l,p = (None,None)
            form = AuthForm(request, 
                    {'username': l, 'password': p, 'remember': True})
        else:
            form = AuthForm(request)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_to_response(template_name, {
        'form': form,
        'next': redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))
login = never_cache(login)

def logout(request):
    """
    View: deletes visitor from session, displays farewell message.
    """
    from django.contrib.auth.views import logout
    return logout(request)
logout = never_cache(logout)
