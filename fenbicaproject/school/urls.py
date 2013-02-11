from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('school.views',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^manage/$', "manage", name="school_manage"),
    url(r'^manage/student/$', "manage_student", name="manage_student"),
    #url(r'^student_experience/(?P<pk>\d+)$', "student_experience",name="student_experience"),
    #url(r'^student_experience/(?P<pk>\d+)$', "student_experience",name="student_experience"),
    #url(r'^student_keeper/(?P<pk>\d+)$', "student_keeper",name="student_keeper"),
    #url(r'^student_family_member/(?P<pk>\d+)$', "student_family_member",name="student_family_member"),
    #url(r'^student_register/(?P<pk>\d+)$', "student_register",name="student_register"),
    #url(r'^student_comment/(?P<pk>\d+)$', "student_comment",name="student_comment"),
    #url(r'^student_rewards/(?P<pk>\d+)$', "student_rewards",name="student_rewards"),
    #url(r'^student_punishment/(?P<pk>\d+)$', "student_punishment",name="student_punishment"),
    #url(r'^student_enrollment/(?P<pk>\d+)$', "student_enrollment",name="student_enrollment"),
    #url(r'^student_graduate/(?P<pk>\d+)$', "student_graduate",name="student_graduate"),
    #url(r'^student_finish_study/(?P<pk>\d+)$', "student_finish_study",name="student_finish_study"),
    #url(r'^student_transfer/(?P<pk>\d+)$', "student_transfer",name="student_transfer"),
    #url(r'^student_assistance/(?P<pk>\d+)$', "student_assistance",name="student_assistance"),
    #url(r'^student_drill/(?P<pk>\d+)$', "student_drill",name="student_drill"),

    url(r'^manage/staff/$', "manage_staff", name="manage_staff"),
    #url(r'^staff_diploma/(?P<pk>\d+)$', "staff_diploma",name="staff_diploma"),
    #url(r'^staff_experience/(?P<pk>\d+)$', "staff_experience",name="staff_experience"),
    #url(r'^staff_spouse/(?P<pk>\d+)$', "staff_spouse",name="staff_spouse"),
    #url(r'^staff_other_family/(?P<pk>\d+)$', "staff_other_family",name="staff_other_family"),
    #url(r'^staff_teaching_workload/(?P<pk>\d+)$', "staff_teaching_workload",name="staff_teaching_workload"),
    #url(r'^staff_teaching/(?P<pk>\d+)$', "staff_teaching",name="staff_teaching"),

    #url(r'^student_comment/(?P<pk>\d+)$', "student_comment",name="student_comment"),
    #url(r'^student_rewards/(?P<pk>\d+)$', "student_rewards",name="student_rewards"),
    #url(r'^student_punishment/(?P<pk>\d+)$', "student_punishment",name="student_punishment"),
    #url(r'^student_enrollment/(?P<pk>\d+)$', "student_enrollment",name="student_enrollment"),
    #url(r'^student_graduate/(?P<pk>\d+)$', "student_graduate",name="student_graduate"),
    #url(r'^student_finish_study/(?P<pk>\d+)$', "student_finish_study",name="student_finish_study"),
    #url(r'^student_transfer/(?P<pk>\d+)$', "student_transfer",name="student_transfer"),
    #url(r'^student_assistance/(?P<pk>\d+)$', "student_assistance",name="student_assistance"),
    #url(r'^student_drill/(?P<pk>\d+)$', "student_drill",name="student_drill"),
    #url(r'^manage/staff/$', "manage_staff", name="manage_staff"),
)
