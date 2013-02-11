from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('dorm.views',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^index/$', "index", name="dorm_index"),
    url(r'^bedchamber/list/$', "bedchamber_list", name="dorm_bedchamber_list"),
    url(r'^bedchamber/(?P<bedchamber_pk>\d+)/$', "bedchamber", name="dorm_bedchamber"),
    url(r'^boarder/list/$', "boarder_list", name="dorm_boarder_list"),
    url(r'^check/list/$', "check_list", name="dorm_check_list"),
    url(r'^latelog/list/$', "latelog_list", name="dorm_latelog_list"),
    url(r'^check/summary/$', "check_summary", name="dorm_check_summary"),
)
