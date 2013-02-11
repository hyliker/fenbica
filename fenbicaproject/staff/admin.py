#coding: utf-8
from django.contrib import admin
from staff.models import *
from treebeard.admin import TreeAdmin
from staff.forms import StaffForm
#from profile.forms import StudentProfileAdminForm

class StaffAdmin(admin.ModelAdmin):
    date_hierarchy = "dtenroll"
    list_display = ("name", "gender", "uuid", "id_no", "birthday", "diploma", "dtenroll", )
    list_filter = ("gender", "diploma", "is_leaved" )
    list_per_page = 50
    raw_id_fields = ("post", "nationality", "born_place", "native_place", "folk")
    search_fields = ("name", "spell_name", "username", "uuid", "id_no")
    form = StaffForm

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get("password", None)
        if not change:
            if password is None:
                obj.set_unusable_password()
            else:
                obj.set_password(password)
        obj.save()

admin.site.register(Staff, StaffAdmin)

class DiplomaAdmin(admin.ModelAdmin):
    date_hierarchy = "date_enrollment"
    list_display = ("staff", "diploma", "major", "date_enrollment", "learning_mode", "learning_way", "learning_year", "graduate_school", "degree")
    list_filter = ("diploma", "degree")
    search_fields = ("staff__name", )

admin.site.register(Diploma, DiplomaAdmin)

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("staff", "dtstart", "dtend", "enterprise", "cadre_post", "technical_post", "attestor")
    list_filter = ("cadre_post", "technical_post",)
    search_fields = ("staff__name", )

admin.site.register(Experience, ExperienceAdmin)

class SpouseAdmin(admin.ModelAdmin):
    list_display = ("staff", "name", "gender", "birthday", "folk", "domicle_location", "politics", "diploma", "degree", "enterprise", "telephone", "family_members_number", "foster_number")
    list_filter = ("politics", )
    search_fields = ("staff__name", "name")

admin.site.register(Spouse, SpouseAdmin)

class FamilyAdmin(admin.ModelAdmin):
    list_display = ("staff", "relation", "name", "telephone", "enterprise", "marriage", "colony")
    list_filter = ("politics", "relation" )
    search_fields = ("staff__name", "name")

admin.site.register(Family, FamilyAdmin)

class WorkloadAdmin(admin.ModelAdmin):
    date_hierarchy = "dtstart"
    list_display = ("staff", "type", "workload", "dtstart", "dtend")
    list_filter = ("type",)
    search_fields  = ("staff__name", "content", "comment")

admin.site.register(Workload, WorkloadAdmin)

class TeachingAdmin(admin.ModelAdmin):
    list_display = ("staff", "dtstart", "dtend", "period", "learning_stage", "role", "teached_number")
    list_filter = ("learning_stage", "role")
    search_fields = ("staff__name", )
    raw_id_fields = ("staff", "course", "classes" )

admin.site.register(Teaching, TeachingAdmin)

class PostAdmin(TreeAdmin):
    search_fields = ("name",)

admin.site.register(Post, PostAdmin)
