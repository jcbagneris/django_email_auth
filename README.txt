===========================
Email based auth for Django
===========================

`email_auth` is an email based authentication backend for Django_. It allows you to use Django's built-in authentication mechanisms and User model while authenticating User on email address instead of username.

It basically re-uses the original Django auth code, passing it a custom Form to allow for email authentication. Overall application structure is based on the one used by `Django CAS`_, i.e. a custom authentication backend and a middleware to intercept calls to original login views (especially useful if you use the Django admin).

`email_auth` should be compatible with Django 1.3 and 1.4 versions.

`email_auth` is (c) 2009-2012 Jean-Charles Bagneris. See LICENSE for redistribution
information and usual disclaimer.


.. _Django: http://djangoproject.com/
.. _Django Cas: http://code.google.com/p/django-cas/

Installation
============

The easiest and prefered way is to install from PyPI, either through pip or through
easy_install::

	$ pip install django_email_auth

	$ easy_install -U django_email_auth

You can download the sources as well, and install from source::

	$ python setup.py install

Then, reference the middleware and the backend in your `settings.py` project's file. Resulting settings may look like::

	MIDDLEWARE_CLASSES = (
		'django.middleware.gzip.GZipMiddleware',
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'email_auth.middleware.EmailAuthMiddleware',
		'django.middleware.locale.LocaleMiddleware',
		'django.middleware.common.CommonMiddleware',
	)   

	AUTHENTICATION_BACKENDS = (
		'email_auth.backends.EmailBackend',
	)

If you want to use the login and logout templates provided instead of custom ones, make sure that `django.template.loaders.app_directories.load_template_source` is in your TEMPLATE_LOADERS setting and add `email_auth` to your INSTALLED_APPS setting. In addition, these templates are only provided as examples, and require the Django admin app to work, so add it too to your INSTALLED_APPS. For an example::

	TEMPLATE_LOADERS = (
		'django.template.loaders.filesystem.load_template_source',
		'django.template.loaders.app_directories.load_template_source',
	)

	INSTALLED_APPS = (
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.sites',
		'django.contrib.admin',
		'email_auth',
	)

If you subclassed the User model instead of using the `get_profile` mechanism, use the CUSTOM_USER_MODEL setting to indicate the name of your model. `email_auth` would then return an instance of your custom user model upon successful authentication::

	CUSTOM_USER_MODEL = 'coaching.Utilisateur'

If you want to use a custom login view instead of the one provided
(email_auth.views.login), add a LOGIN_URL_MAP settings, pointing to it (thanks
to `Wesley Mason`_ for the patch).

.. _Wesley Mason: http://1stvamp.org/

Finally, make sure that your project sets the required urls to log your users in and out in your urls mappings::

    (r'^login/$', 'email_auth.views.login'),
    (r'^logout/$', 'email_auth.views.logout'),

Templates
=========

Templates for login and logout views are supposed to live in `registration/login.html` and `registration/logged_out.html`. Standard ones are provided with `email_auth`, put the application in your INSTALLED_APPS and use the `django.template.loaders.app_directories.load_template_source` template loader if you want to use those. Otherwise, either provide yours in a `registration` folder in your root template folder, or pass whatever names your templates have to the `template_name` parameter of `login` and `logout` views.

Signals
=======

As a convenience, signals are raised when a user logs in or out successfully::

    user_logged_in = Signal(providing_args=['request',])
    user_logged_out = Signal(providing_args=['request',])

The full login or logout `request` is passed as an arg to the related signal. In addition, the sender of the logged in signal is the logged in User instance, and the sender of the logged out signal is the User instance which just logged out.

Internationalization
====================

`email_auth` uses Django internationalization mechanism. Make sure you have `django.middleware.locale.LocaleMiddleware` in your MIDDLEWARE_CLASSES settings to use it. The locale files for the French language are provided with the application. If you create locale files for other languages, feel free to fork the project and send me a pull request for those to be included in the distribution.

Similar projects
================

Full apps
---------

- https://code.launchpad.net/django-email-auth
- http://pypi.python.org/pypi/django-emailauth/0.1

Related snippets
----------------

- http://www.djangosnippets.org/snippets/74/
- http://www.djangosnippets.org/snippets/1590/
- http://www.micahcarrick.com/django-email-authentication.html

Proposed patch to Django
------------------------

http://code.djangoproject.com/attachment/ticket/8274/authentication_form.diff
