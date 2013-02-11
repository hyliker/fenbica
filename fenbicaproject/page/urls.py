from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('page.views',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^scenery/index$', "scenery_index", name="page_scenery_index"),
    url(r'^service/index$', "service_index", name="page_service_index"),
    url(r'^teacher/index$', "teacher_index", name="page_teacher_index"),
    url(r'^college_enroll/index$', "college_enroll_index", name="college_enroll_index"),
)
