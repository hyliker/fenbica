#coding: utf-8
from django.contrib import admin
from page.models import *

def student_gender(self, obj):
    return obj.student.gender.name
student_gender.short_description = u"性别"

class SceneryAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "dtcreated", "is_published", "display_order")

class PhoneCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")

class PhoneAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "category", "display_order")
    list_filter = ("category",)
    search_fields = ("name", "phone")

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("staff", "staff_gender", "title", "introduction")
    search_fields = ("staff", "title")

    def staff_gender(self, obj):
        return obj.staff.gender.name
    staff_gender.short_description = u"性别"

#class CollegeEnrolleeLevelAdmin(admin.ModelAdmin):
    #list_display = ('name', 'priority')

#class CollegeEnrolleeAdmin(admin.ModelAdmin):
    #date_hierarchy = "dtenrolled"
    #list_display = ("uuid", "student", "level", "student_gender", "college", "major", "dtenrolled", "priority", "is_approved")
    #search_fields = ("uuid", "student__name", "college")
    #raw_id_fields = ("student",)

    #student_gender = student_gender

    #def student_gender(self, obj):
        #return obj.student.gender.name
    #student_gender.short_description = u"性别"

#以下动态增加绑定Admin
scope = locals()
for key in scope.keys():
    if key.endswith("Admin") and key is not "Admin":
        admin_model = scope[key]
        model = scope[key[:-5]]
        admin.site.register(model, admin_model)

