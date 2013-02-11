from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('classgrade.views',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^(?P<profileID>\d+)$', "account.views.index", name="profile"),
    #url(r'^(?P<profileID>\d+)$', "account.views.view_profile", name="view_profile"),
    #url(r'^(?P<profileID>\d+)/edit$', "person.views.edit_profile", name="edit_profile"),
    #url(r'^add/$', "account.views.add_profile", name="add_profile"),
    #url(r'^(?P<staff_pk>\d+)/edit/$', "edit_staff", name="edit_staff"),
    #url(r'^(?P<staff_pk>\d+)/delete/$', "delete_staff", name="delete_staff"),
    #url(r'^(?P<staff_pk>\d+)/$', "staff", name="staff"),
    #url(r'^experience/list/(?P<staff_pk>\d+)$', "experience_list",name="staff_experience_list"),
    #url(r'^experience/(?P<pk>\d+)$', "experience",name="staff_experience"),
    #url(r'^diploma/(?P<pk>\d+)$', "diploma",name="staff_diploma"),
    #url(r'^diploma/list/(?P<staff_pk>\d+)$', "diploma_list",name="staff_diploma_list"),
    #url(r'^spouse/(?P<staff_pk>\d+)$', "spouse",name="staff_spouse"), 
    #url(r'^family/(?P<pk>\d+)$', "family",name="staff_family"),
    #url(r'^family/list/(?P<staff_pk>\d+)$', "family_list",name="staff_family_list"),
    #url(r'^workload/list/(?P<staff_pk>\d+)$', "workload_list",name="staff_workload_list"),
    #url(r'^workload/(?P<pk>\d+)$', "workload",name="staff_workload"),
    url(r'^index/$', "index", name="classgrade_index"),
    url(r'^check/index/$', "check_index", name="classgrade_check_index"),
    url(r'^check/(?P<check_pk>\d+)/$', "check", name="classgrade_check"),
    url(r'^check/summary/((?P<year>\d+)/(?P<month>\d+)/)?$', "check_summary", name="classgrade_check_summary"),
    #url(r'^check/summary/details/$', "check_summary_details", name="classgrade_check_summary_details"),
    url(r'^check/list/$', "check_list",name="classgrade_check_list"),
    url(r'^timetable/(?P<klass_pk>\d+)/(?P<semester_pk>\d+)?$', "timetable",name="classgrade_timetable"),
    url(r'^class/(?P<klass_pk>\d+)/$', "klass",name="classgrade_class"),
    url(r'^classmate/list/$', "classmate_list",name="classgrade_classmate_list"),
    url(r'^class/list/((?P<klass_year>\d{4})?/(?P<klass_grade>\d+)?)?$', "klass_list",name="classgrade_class_list"),
    url(r'class/list/person/(?P<person_pk>\d+)/$', 'person_class_list', name="person_class_list"),
    url(r'student/comment/list', 'student_comment_list', name="classgrade_student_comment_list"),
    url(r'student/comment/edit/(?P<classmate_pk>\d+)', 'student_comment_edit', name="classgrade_student_comment_edit"),
)
