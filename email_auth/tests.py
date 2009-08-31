# -*- encoding: utf-8 -*-

"""
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

