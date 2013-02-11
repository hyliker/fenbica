from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('course.views',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^index/$', "index"),
    (r'^my/$', "my_course"),
    (r'^add/$', "add_course"),
    url(r'^(?P<course_pk>\d+)/$', "course", name="course_course"),
    url(r'^person/(?P<person_pk>\d+)/$', "person_course", name="course_person_course"),
    url(r'^timetable/', 'timetable', name="course_timetable"),
    #url(r'^manage/student/$', "manage_student", name="manage_student"),
    #url(r'^student_experience/(?P<pk>\d+)$', "student_experience",name="student_experience"),
    #url(r'^student_experience/(?P<pk>\d+)$', "student_experience",name="student_experience"),
)
