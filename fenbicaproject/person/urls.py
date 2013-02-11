from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('person.views',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^(?P<person_pk>\d+)?/$', "person", name="person"),
    url(r'^(?P<person_pk>\d+)/edit/$', "edit_person", name="edit_person"),
    url(r'^add/$', "add_profile", name="add_profile"),
    url(r'^new/$', "new_person", name="new_person"),
)
urlpatterns += patterns('',
    url(r'^password/change/$', 'django.contrib.auth.views.password_change', {"template_name": "person/password_change.html"},  name="password_change"),
    url(r'^password/change/done/$', 'django.contrib.auth.views.password_change_done', {"template_name": "person/password_change_done.html"},  name="password_change_done"),
)
