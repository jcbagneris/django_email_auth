# -*- encoding: utf-8 -*-

"""
These are for testing purposes only.
"""

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'email_auth.views.login'),
    (r'^logout/$', 'email_auth.views.logout'),
    (r'^logged_in/$','email_auth.tests.fakeview'),
)

