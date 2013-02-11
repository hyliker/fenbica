#coding: utf-8
from django.contrib import admin
from course.models import *

class CourseAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "english_name", "grade", "semester", "teaching_year", "exam_mode", "teaching_mode", "total_period", "teacher" )
    list_filter = ("name", "teaching_year", "grade")
    search_fields = ("name", "teaching__name", "english_name")
    raw_id_fields = ("teacher", )

class StudentCourseAdmin(admin.ModelAdmin):
    date_hierarchy = "dtstart"
    list_display = ("student", "course", "dtstart", "dtend")
    search_fields = ("student__name", "course__name")
    raw_id_fields = ("student", "course")



#admin.site.register(StudentExperience, StudentExperienceAdmin)

#以下动态增加绑定Admin
scope = locals()
for key in scope.keys():
    if key.endswith("Admin") and key is not "Admin":
        admin_model = scope[key]
        model = scope[key[:-5]]
        admin.site.register(model, admin_model)
