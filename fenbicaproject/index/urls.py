from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),
    (r'^/', 'index.view.index'),
    (r'^register/$', 'index.view.register'),
)
