from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('student.views',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^(?P<profileID>\d+)$', "account.views.index", name="profile"),
    #url(r'^view/(?P<profileID>\d+)$', "account.views.view_profile", name="view_profile"),
    #url(r'^edit/(?P<profileID>\d+)$', "account.views.edit_profile", name="edit_profile"),
    #url(r'^add/$', "account.views.add_profile", name="add_profile"),
    #url(r'^edit/myself$', "edit_student_by_myself", name="edit_student_by_myself"),
    url(r'^admin/', "admin_student", name="admin_student"),
    #url(r'^add/', "add_student", name="add_student"),
    url(r'^(?P<student_pk>\d+)/edit/$', "edit_student", name="edit_student"),
    #url(r'^(?P<student_pk>\d+)/delete/$', "delete_student", name="delete_student"),
    url(r'^(?P<student_pk>\d+)/$', "student", name="student"),
    url(r'^archive/(?P<student_pk>\d+)/$', "student_archive", name="student_archive"),
    url(r'^archive/(?P<student_pk>\d+)/print/$', "student_archive_print", name="student_archive_print"),
    url(r'^experience/list/(?P<student_pk>\d+)$', "experience_list",name="student_experience_list"),
    url(r'^experience/(?P<pk>\d+)$', "experience",name="student_experience"),
    url(r'^experience/edit/(?P<pk>\d+)?$', "edit_experience",name="student_edit_experience"),
    url(r'^experience/delete/(?P<pk>\d+)$', "delete_experience",name="student_delete_experience"),
    url(r'^keeper/list/(?P<student_pk>\d+)$', "keeper_list",name="student_keeper_list"),
    url(r'^keeper/(?P<pk>\d+)$', "keeper",name="student_keeper"),
    url(r'^keeper/edit/(?P<pk>\d+)?$', "edit_keeper",name="student_edit_keeper"),
    url(r'^keeper/delete/(?P<pk>\d+)$', "delete_keeper",name="student_delete_keeper"),
    url(r'^family_member/list/(?P<student_pk>\d+)$', "family_member_list",name="student_family_member_list"),
    url(r'^family_member/(?P<pk>\d+)$', "family_member",name="student_family_member"),
    url(r'^family_member/edit/(?P<pk>\d+)?$', "edit_family_member",name="student_edit_family_member"),
    url(r'^family_member/delete/(?P<pk>\d+)$', "delete_family_member",name="student_delete_family_member"),
    url(r'^register/list/(?P<student_pk>\d+)$', "register_list",name="student_register_list"),
    url(r'^register/(?P<pk>\d+)$', "register",name="student_register"),
    url(r'^comment/(?P<pk>\d+)$', "comment",name="student_comment"),
    url(r'^comment/list/(?P<student_pk>\d+)$', "comment_list",name="student_comment_list"),
    url(r'^rewards/(?P<pk>\d+)$', "rewards",name="student_rewards"),
    url(r'^rewards/list/(?P<student_pk>\d+)$', "rewards_list",name="student_rewards_list"),
    url(r'^punishment/(?P<pk>\d+)$', "punishment",name="student_punishment"),
    url(r'^punishment/list/(?P<student_pk>\d+)$', "punishment_list",name="student_punishment_list"),
    #url(r'^enrollment/(?P<pk>\d+)$', "enrollment",name="student_enrollment"),
    #url(r'^enrollment/list/(?P<student_pk>\d+)$', "enrollment_list",name="student_enrollment_list"),
    url(r'^graduate/(?P<pk>\d+)$', "graduate",name="student_graduate"),
    url(r'^graduate/list/(?P<student_pk>\d+)$', "graduate_list",name="student_graduate_list"),
    url(r'^finish_study/(?P<pk>\d+)$', "finish_study",name="student_finish_study"),
    url(r'^finish_study/list/(?P<student_pk>\d+)$', "finish_study_list",name="student_finish_study_list"),
    url(r'^transfer/(?P<pk>\d+)$', "transfer",name="student_transfer"),
    url(r'^transfer/list/(?P<student_pk>\d+)$', "transfer_list",name="student_transfer_list"),
    url(r'^assistance/(?P<pk>\d+)$', "assistance",name="student_assistance"),
    url(r'^assistance/list/(?P<student_pk>\d+)$', "assistance_list",name="student_assistance_list"),
    url(r'^drill/(?P<pk>\d+)$', "drill",name="student_drill"),
    url(r'^drill/list/(?P<student_pk>\d+)$', "drill_list",name="student_drill_list"),
    url(r'^exam/result/list/(?P<student_pk>\d+)$', "exam_result_list",name="student_exam_result_list"),
    url(r'^exam/result/analyse/(?P<student_pk>\d+)$', "exam_result_analyse",name="student_exam_result_analyse"),
    url(r'^classmate/list/(?P<student_pk>\d+)$', "classmate_list",name="student_classmate_list"),
)
