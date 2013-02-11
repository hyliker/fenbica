#coding: utf-8
from django.contrib import admin
from school.models import *
from treebeard.admin import TreeAdmin

#class ClassAdmin(admin.ModelAdmin):
    #list_display = ("grade", "class_no", "name", "type", "dtcreated", "honorary_title", "master", "monitor", "classroom" )
    #list_filter = ("type", "grade")
    #search_fields = ("master__name", "honorary_title", "name", "classroom__name")
    #list_per_page = 25

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "remark")
    search_fields = ("name",)

admin.site.register(Classroom, ClassroomAdmin)

class SubjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subject, SubjectAdmin)

class OfficeAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "abbr", "master")
    search_fields = ("name", "abbr", "master")

admin.site.register(Office, OfficeAdmin)

class BuildingAdmin(admin.ModelAdmin):
    date_hierarchy = "dtcreated"
    list_display = ("uuid", "name", "dtcreated", "property_usage", "school_unit_level", "category", "structrue", "floor_number")
    list_filter = ("category", "status",)
    search_fields = ("uuid", "name",)

admin.site.register(Building, BuildingAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ("uuid", "building", "name", "floor", "usage", "teaching_use_property", "building_area", "using_area")
    list_filter = ("building", "teaching_use_property", "usage")
    search_fields = ("uuid", "name")

admin.site.register(Room, RoomAdmin)


class FacilityAdmin(admin.ModelAdmin):
    date_hierarchy = "dtcreated"
    list_display = ("uuid", "name", "dtcreated", "fee", "usage_status")
    list_filter = ("usage_status",)
    search_fields = ("uuid", "name")

admin.site.register(Facility, FacilityAdmin)

class DepartmentAdmin(TreeAdmin):
    list_display = ("name", "hod",)
    raw_id_fields = ("hod",)

admin.site.register(Department, DepartmentAdmin)

class DepartmentMemberAdmin(admin.ModelAdmin):
    list_display = ("department", "person", "dtstart", "dtend")
    raw_id_fields = ("department", "person" )

admin.site.register(DepartmentMember, DepartmentMemberAdmin)

class PositionAdmin(TreeAdmin):
    list_display = ("title", "description", "status")

admin.site.register(Position, PositionAdmin)
