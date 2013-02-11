from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('staff.views',
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
    url(r'^add/$', "add_staff", name="add_staff"),
    url(r'^admin/$', "admin_staff", name="admin_staff"),
    #url(r'^edit/myself$', "edit_staff_by_myself", name="edit_staff_by_myself"),
    url(r'^(?P<staff_pk>\d+)/edit/$', "edit_staff", name="edit_staff"),
    #url(r'^(?P<staff_pk>\d+)/delete/$', "delete_staff", name="delete_staff"),
    url(r'^(?P<staff_pk>\d+)/$', "staff", name="staff"),
    url(r'^experience/list/(?P<staff_pk>\d+)$', "experience_list",name="staff_experience_list"),
    url(r'^experience/edit/(?P<pk>\d+)?$', "edit_experience",name="staff_edit_experience"),
    url(r'^experience/(?P<pk>\d+)$', "experience",name="staff_experience"),
    url(r'^experience/delete/(?P<pk>\d+)$', "delete_experience",name="staff_delete_experience"),
    url(r'^diploma/(?P<pk>\d+)$', "diploma",name="staff_diploma"),
    url(r'^diploma/list/(?P<staff_pk>\d+)$', "diploma_list",name="staff_diploma_list"),
    url(r'^diploma/edit/(?P<pk>\d+)?$', "edit_diploma",name="staff_edit_diploma"),
    url(r'^diploma/delete/(?P<pk>\d+)$', "delete_diploma",name="staff_delete_diploma"),
    url(r'^spouse/(?P<staff_pk>\d+)$', "spouse",name="staff_spouse"), 
    url(r'^spouse/edit/(?P<pk>\d+)?$', "edit_spouse",name="staff_edit_spouse"), 
    url(r'^family/(?P<pk>\d+)$', "family",name="staff_family"),
    url(r'^family/edit/(?P<pk>\d+)?$', "edit_family",name="staff_edit_family"),
    url(r'^family/list/(?P<staff_pk>\d+)$', "family_list",name="staff_family_list"),
    url(r'^family/delete/(?P<pk>\d+)$', "delete_family",name="staff_delete_family"),
    url(r'^workload/list/(?P<staff_pk>\d+)$', "workload_list",name="staff_workload_list"),
    url(r'^workload/(?P<pk>\d+)$', "workload",name="staff_workload"),
    url(r'^workload/edit/(?P<pk>\d+)?$', "edit_workload",name="staff_edit_workload"),
    url(r'^workload/delete/(?P<pk>\d+)$', "delete_workload",name="staff_delete_workload"),
    url(r'^teaching/(?P<pk>\d+)$', "teaching",name="staff_teaching"),
    url(r'^teaching/list/(?P<staff_pk>\d+)$', "teaching_list",name="staff_teaching_list"),
    url(r'^teaching/edit/(?P<pk>\d+)?$', "edit_teaching",name="staff_edit_teaching"),
    url(r'^teaching/delete/(?P<pk>\d+)$', "delete_teaching",name="staff_delete_teaching"),
    url(r'^course/list/(?P<staff_pk>\d+)$', "course_list",name="staff_course_list"),
    url(r'^course/classgrade/list/(?P<staff_pk>\d+)$', "course_classgrade_list",name="staff_course_classgrade_list"),
    url(r'^add/$', "add_staff", name="add_staff"),
)
