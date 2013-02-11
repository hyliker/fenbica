#coding: utf-8
from django.contrib import admin
from dorm.models import *
from student.models import Student
from django.http import HttpResponse, HttpResponseRedirect

class BuildingAdmin(admin.ModelAdmin):

    list_display = ("uuid", "name", "bedchamber_number", "floor_number", "master_list")
    list_per_page = 50
    search_fields = ["name"]
    raw_id_fields = ("masters",)

    def master_list(self, obj):
        master_list = obj.masters.all()
        master_list_links = [u'<a href="/person/%s">%s</a>' % (m.pk, m.name) for m in master_list]
        return u", ".join(master_list_links)
    master_list.allow_tags = True
    master_list.short_description = u"管理员名单"

class BedchamberAdmin(admin.ModelAdmin):
    list_display = ("uuid", "dtcreated", "building", "telephone", "capacity", "living_number", "is_active")
    raw_id_fields = ("master",)

class BedAdmin(admin.ModelAdmin):
    list_display = ("bedchamber", "uuid", "dtcreated", "is_used" )
    raw_id_fields = ("bedchamber",)

class BoarderAdmin(admin.ModelAdmin):
    list_display = ("student", "student_name", "student_gender", "bed", "dtstart", "dtend")
    search_fields = ("student__name", "student__user__username", "student__uuid")
    raw_id_fields = ("student", "bed")

    def student_name(self, obj):
        return obj.student.pk
    student_name.short_description = u"编号"

    def student_gender(self, obj):
        return obj.student.gender
    student_gender.short_description = u"性别"

    #def view_student(self, obj):
        #return u'<a href="/staff/view/%d">学生详情</a>' % (obj.student.pk)
    #view_student.short_description = u"学生详情"


class CheckAdmin(admin.ModelAdmin):
    date_hierarchy = "dtchecked"
    list_display = ("bedchamber", "dtchecked", "thing_ranking", "bed_ranking", "health_ranking", "infrastructure_ranking", "absence_ranking", "discipline_ranking", "sum_ranking" )
    list_filter = ("dtchecked",)
    search_fields = ("bedchamber__uuid",)
    raw_id_fields = ("bedchamber", "checker")

    def save_model(self, request, obj, form, change):
        if obj.checker is None:
            obj.checker = request.person
        obj.creator = request.person
        obj.save()

class LatelogAdmin(admin.ModelAdmin):
    date_hierarchy = "dtlogged"
    list_display = ("boarder", "dtlogged", "reason", "dtcreated", "creator")
    list_filter = ("dtlogged", )
    search_fields = ("boarder",)
    raw_id_fields = ("boarder",)

    def save_model(self, request, obj, form, change):
        obj.creator = request.person
        obj.save()

#以下动态增加绑定Admin
scope = locals()
for key in scope.keys():
    if key.endswith("Admin") and key is not "Admin":
        admin_model = scope[key]
        model = scope[key[:-5]]
        admin.site.register(model, admin_model)
