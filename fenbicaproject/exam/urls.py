#coding: utf-8
from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('exam.views',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^studentexam/index/$', "exam_index", name="exam_index"),
    url(r'^result/add/$', "add_result", name="exam_add_result"),
    url(r'^result/add/by_room/$', "add_result_by_room", name="exam_add_result_by_room"),
    url(r'^studentexam/add/by_school$', "add_studentexam_by_school", name="add_studentexam_by_school"),
    #url(r'^view/studentexam/(?P<profileID>\d+)/$', "view_studentexam", name="view_studentexam"),
    url(r'^view/studentexamresult/(?P<profileID>\d+)/$', "view_studentexamresult", name="view_studentexamresult"),
    #url(r'^view/studentexam/(?P<profileID>\d+)/$', "view_studentexam_by_myself", name="student_exam_result"),
    #url(r'^view/studentexam/(?P<profileID>\d+)/$', "view_studentexam_by_myself", name="view_student_exam_name"),
    url(r'^add/studentexamresult/by_school$', "add_studentexamresult_by_school", name="add_studentexamresult_by_school"),

    url(r'^studentexamsubject/add$', "add_studentexamsubject", name="add_studentexamsubject"),
    url(r'^manage/$', "manage_exam", name="exam_manage_exam"),
    url(r'^studentexam/(?P<exam_pk>\d+)/edit$', "edit_studentexam", name="edit_studentexam"),
    url(r'^studentexamsubject/(?P<exam_subject_pk>\d+)/edit$', "edit_studentexamsubject", name="edit_studentexamsubject"),
    url(r'^studentexam/(?P<exam_pk>\d+)/delete$', "delete_studentexam", name="delete_studentexam"),
    url(r'^studentexamsubject/(?P<exam_subject_pk>\d+)/delete$', "delete_studentexamsubject", name="delete_studentexamsubject"),

    url(r'^studentexamsubject/manage$', "manage_studentexamsubject", name="manage_studentexamsubject"),

    url(r'^add/studentexamresult/by_class/step1$', "add_studentexamresult_by_class_step1", name="add_studentexamresult_by_class_step1"),
    url(r'^add/studentexamresult/by_class/step2/exam_subject-(?P<exam_subject_pk>\d+)$', "add_studentexamresult_by_class_step2", name="add_studentexamresult_by_class_step2"),
    url(r'^add/studentexamresult/by_class/step3/exam_subject-(?P<exam_subject_pk>\d+)/class-(?P<class_pk>\d+)$', "add_studentexamresult_by_class_step3", name="add_studentexamresult_by_class_step3"),
    #url(r'^import/studentexamresult/by_school/$', "import_studentexamresult_by_school", name="import_studentexamresult_by_school"),
    url(r'^result/import/$', "import_result", name="exam_import_result"),
    url(r'^result/import/by_room$', "import_result_by_room", name="import_result_by_room"),
    url(r'^export/studentexamresult/by_class/exam_subject-(?P<exam_subject_pk>\d+)/class-(?P<class_pk>\d+)$', "export_studentexamresult_by_class", name="export_studentexamresult_by_class"),
    url(r'^export/result/by_room_subject/$', "export_result_by_room_subject", name="exam_export_result_by_room_subject"),

    url(r'^analysis_class/(exam-(?P<exam_pk>\d+))?$', "analysis_class", name="analysis_class"),
    url(r'^class/analyse/$', "analyse_class", name="exam_analyse_class"),
    #url(r'^analysis_class_subject/(?P<exam_pk>\d+)?$', "analysis_class_subject", name="analysis_class_subject"),
    url(r'^subject/analyse/$', "analyse_subject", name="exam_analyse_subject"),
    #url(r'^analysis_subject/(?P<exam_pk>\d+)?$', "analysis_subject", name="analysis_subject"),
    url(r'^grade/analyse/$', "analyse_grade", name="exam_analyse_grade"),
    #url(r'^analysis_grade_subject/(?P<exam_pk>\d+)?$', "analysis_grade_subject", name="analysis_grade_subject"),
    url(r'^student/analyse$', "analyse_student", name="exam_analyse_student"),
    #url(r'^analysis_class_student/(?P<exam_pk>\d+),(?P<class_pk>\d+)$', "analysis_class_student", name="analysis_class_student"),
    url(r'^analysis_grade_student/(?P<exam_pk>\d+),(?P<grade_pk>\d+)$', "analysis_grade_student", name="analysis_grade_student"),
    #url(r'^analysis/class-(?P<class_pk>\d+)/exam-(?P<exam_pk>\d+)$', "analysis_class", name="analysis_class"),
    #url(r'^analysis_class_step2/exam-(?P<exam_pk>\d+)/class-(?P<class_pk>\d+)$', "analysis_class", name="analysis_class_step2"),
    url(r'^class_subject/(?P<exam_pk>\d+),(?P<class_pk>\d+)$', "class_subject", name="class_subject"),
    #url(r'^grade_subject/(?P<subject_pk>\d+)$', "grade_subject", name="grade_subject"),
    url(r'^grade/subject/(?P<subject_pk>\d+)$', "grade_subject", name="exam_grade_subject"),
    url(r'^room_seat_arrange/$', "room_seat_arrange", name="exam_room_seat_arrange"),
    url(r'^room_seat/$', "room_seat", name="exam_room_seat"),
    url(r'^room/list/$', "room_list", name="exam_room_list"),
    url(r'^class/seat/list/$', "class_seat_list", name="exam_class_seat_list"),
    url(r'^class/seat/$', "class_seat", name="exam_class_seat"),
    url(r'^export/class/seat/$', "export_class_seat", name="exam_export_class_seat"),
    url(r'^room/(?P<pk>\d+)/$', "room", name="exam_room"),
    url(r'^seat/list/export/$', "export_seat_list", name="exam_export_seat_list"),
    url(r'^subject/list/$', "subject_list", name="exam_subject_list"),
    url(r'^subject/(?P<pk>\d+)/$', "subject", name="exam_subject"),
    url(r'^subject/ranking/(?P<subject_pk>\d+)$', "subject_ranking", name="exam_subject_ranking"),

    url(r'^chart/subject/analyse/(?P<subject_pk>\d+)$', "chart_subject_analyse",name="exam_chart_subject_analyse"),
    url(r'^chart/exam/analyse/(?P<exam_pk>\d+)$', "chart_exam_analyse",name="exam_chart_exam_analyse"),
)

urlpatterns += patterns('exam.jsviews',
    url(r'^get_exam_subjects_by_exam/(?P<exam_pk>\d+)$', "get_exam_subjects_by_exam", name="get_exam_subjects_by_exam"),
    url(r'^get_exam_subject_classgrade/$', "get_exam_subject_classgrade", name="get_exam_subject_classgrade"),
    url(r'^get_exam_subject_students/$', "get_exam_subject_students", name="get_exam_subject_students"),
    url(r'^get_exam_grade_list/(?P<exam_pk>\d+)$', "get_exam_grade_list", name="exam_get_exam_grade_list"),
    url(r'^get_exam_room_list/(?P<exam_pk>\d+)/$', "get_exam_room_list", name="exam_get_exam_room_list"),
    url(r'^get_exam_room_list_by_subject/(?P<subject_pk>\d+)/$', "get_exam_room_list_by_subject", name="exam_get_exam_room_list_by_subject"),
    url(r'^get_seat_list_by_room/(?P<room_pk>\d+)/$', "get_seat_list_by_room", name="exam_get_seat_list_by_room"),
    url(r'^chart/student/analyse/(?P<student_pk>\d+)$', "chart_student_analyse",name="exam_chart_student_analyse"),
    url(r'^chart/data/subject/analyse/(?P<subject_pk>\d+)$', "chart_data_subject_analyse",name="exam_chart_data_subject_analyse"),
    url(r'^chart/data/exam/analyse/(?P<exam_pk>\d+)$', "chart_data_exam_analyse",name="exam_chart_data_exam_analyse"),
    url(r'^chart/data/subject/class/analyse/(?P<subject_pk>\d+)$', "chart_data_subject_class_analyse",name="exam_chart_data_subject_class_analyse"),
)
