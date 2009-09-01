# -*- encoding: utf-8 -*-
"""
Email authentication backend
As users are searched on email, indexing the user table
on email in the db might be a good idea.
"""

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class EmailBackend(ModelBackend):
    """
    Authenticate user against email,password credentials
    The user class might be :
    - django.contrib.auth.models.User (default)
    - a custom User class inheriting from django.contrib.auth.models.User
    A custom User class is declared through CUSTOM_USER_MODEL setting :
    CUSTOM_USER_MODEL = 'yourapp.YourCustomUser' 
    """
    def authenticate(self, email=None, password=None):
        try:
            user = self.user_class.objects.get(email=email)
        except self.user_class.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            try:
                user_model = settings.CUSTOM_USER_MODEL
                self._user_class = get_model(*user_model.split('.', 2))
                if not self._user_class:
                    raise ImproperlyConfigured(
                            _('Could not get custom user model %s') % user_model)
                return self._user_class
            except AttributeError:
                return User
        return self._user_class

