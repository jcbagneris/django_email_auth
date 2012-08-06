# -*- encoding: utf-8 -*-
from django.test import TestCase

def test_forms():
    """
    Forms doctests
    >>> from django.conf import settings

    # Ugly, but necessary for testing purposes
    >>> settings.CUSTOM_USER_MODEL = None

    >>> from django.contrib.auth.models import User
    >>> from email_auth.forms import AuthenticationForm
    >>> user = User.objects.create_user("jsmith", "jsmith@example.com", "test123")

    # The user cannot log in with username, even correct

    >>> data = {
    ...     'username': 'jsmith',
    ...     'password': 'test123',
    ... }

    >>> form = AuthenticationForm(None, data)
    >>> form.is_valid()
    False
    >>> form.non_field_errors()
    [u'Please enter a correct email and password. Note that both fields are case-sensitive.']

    # The user submits an invalid email.

    >>> data = {
    ...     'email': 'jsmith',
    ...     'password': 'test123',
    ... }

    >>> form = AuthenticationForm(None, data)
    >>> form.is_valid()
    False
    >>> form.non_field_errors()
    [u'Please enter a correct email and password. Note that both fields are case-sensitive.']

    # The user is inactive.

    >>> data = {
    ...     'email': 'jsmith@example.com',
    ...     'password': 'test123',
    ... }
    >>> user.is_active = False
    >>> user.save()
    >>> form = AuthenticationForm(None, data)
    >>> form.is_valid()
    False
    >>> form.non_field_errors()
    [u'This account is inactive.']

    >>> user.is_active = True
    >>> user.save()

    # The success case

    >>> form = AuthenticationForm(None, data)
    >>> form.is_valid()
    True
    >>> form.non_field_errors()
    []

    """
    pass

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

from email_auth.backends import EmailBackend

class BackendTests(TestCase):
    def test_user_class(self):
        settings.CUSTOM_USER_MODEL = None
        backend = EmailBackend()
        usermodel = backend.user_class
        self.assertEquals(usermodel, User)

        settings.CUSTOM_USER_MODEL = 'myapp.foobar'
        backend = EmailBackend()
        f = lambda x: x.user_class
        self.assertRaises(ImproperlyConfigured, f, backend)

    def test_authenticate(self):
        settings.CUSTOM_USER_MODEL = None
        user = User.objects.create_user("jsmith", "jsmith@example.com", "test123")
        backend = EmailBackend()
        u = backend.authenticate("jsmith@example.com","badpassword")
        self.assertEqual(u, None)
        u = backend.authenticate("jsmith","test123")
        self.assertEqual(u, None)
        u = backend.authenticate("jsmith@example.com","test123")
        self.assertEqual(u, user)

    def test_get_user(self):
        settings.CUSTOM_USER_MODEL = None
        user = User.objects.create_user("jsmith", "jsmith@example.com", "test123")
        user.save()
        backend = EmailBackend()
        u = backend.get_user(user.pk)
        self.assertEqual(u, user)
        u = backend.get_user(0)
        self.assertEqual(u, None)

from django.http import HttpResponse

from email_auth.views import login as email_login

def fakeview(request):
    return HttpResponse("Ok logged in.")

class GeneralTests(TestCase):
    urls= 'email_auth.test_urls'

    def test_login_view(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'registration/login.html')

    def test_admin_access(self):
        response = self.client.get('/admin/')
        self.assertRedirects(response,'/login/?next=%2Fadmin%2F',302,200)

    def test_login_then_logout(self):
        settings.CUSTOM_USER_MODEL = None
        settings.REDIRECT_FIELD_NAME = 'next'
        user = User.objects.create_user("jsmith", "jsmith@example.com", "test123")
        response = self.client.post('/login/?next=%2Flogged_in%2F',
                {'email':'jsmith@example.com', 'password':'test123'})
        self.assertRedirects(response,'/logged_in/',302,200)
        response = self.client.get('/logout/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'registration/logged_out.html')
