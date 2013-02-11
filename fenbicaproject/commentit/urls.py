# coding: utf-8
from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('commentit.views',
    url(r'^add/$', 'add_comment', name="commentit_add_comment"),
)
