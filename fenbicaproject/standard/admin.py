#coding: utf-8
from django.contrib import admin
from standard.models import *
#from profile.forms import StudentProfileAdminForm

class LocationCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "pinyin", "code", "letter_code", "remark")
    search_fields = ["name", "pinyin", "code", "letter_code", "remark"]
    list_per_page = 50

class GenderCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "remark")
    ordering = ("code",)

class FolkCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

class RelationCodeAdmin(admin.ModelAdmin):
    pass

class PoliticsCodeAdmin(admin.ModelAdmin):
    pass

class MarriageCodeAdmin(admin.ModelAdmin):
    pass

class HealthCodeAdmin(admin.ModelAdmin):
    pass

class LocationTypeCodeAdmin(admin.ModelAdmin):
    pass

class LocationEconCodeAdmin(admin.ModelAdmin):
    pass

class SchoolHostCodeAdmin(admin.ModelAdmin):
    pass

class SchoolTypeCodeAdmin(admin.ModelAdmin):
    pass

class StudentTypeCodeAdmin(admin.ModelAdmin):
    pass

class ClassTypeCodeAdmin(admin.ModelAdmin):
    pass

class BloodTypeCodeAdmin(admin.ModelAdmin):
    pass

class EmigrantCodeAdmin(admin.ModelAdmin):
    pass

class ExamModeCodeAdmin(admin.ModelAdmin):
    pass

class ExamTypeCodeAdmin(admin.ModelAdmin):
    pass

class RewardsTypeCodeAdmin(admin.ModelAdmin):
    pass

class RewardsLevelCodeAdmin(admin.ModelAdmin):
    pass

class PunishmentNameCodeAdmin(admin.ModelAdmin):
    pass

class EnrollmentTypeCodeAdmin(admin.ModelAdmin):
    pass

class SourceTypeCodeAdmin(admin.ModelAdmin):
    pass

class AttendanceTypeCodeAdmin(admin.ModelAdmin):
    pass

class EducationResultCodeAdmin(admin.ModelAdmin):
    pass

class TransferTypeCodeAdmin(admin.ModelAdmin):
    pass

class LevelScoreCodeAdmin(admin.ModelAdmin):
    pass

class FloatingCodeAdmin(admin.ModelAdmin):
    pass

class SingletonCodeAdmin(admin.ModelAdmin):
    pass

class LocationFolkCodeAdmin(admin.ModelAdmin):
    pass

class RegisterStatusCodeAdmin(admin.ModelAdmin):
    pass

class TransferStatusCodeAdmin(admin.ModelAdmin):
    pass

class PostOccupationCodeAdmin(admin.ModelAdmin):
    pass

class NationalityCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

class DomicleTypeCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

class DiplomaCodeAdmin(admin.ModelAdmin):
    pass

class DegreeCodeAdmin(admin.ModelAdmin):
    pass

class OccupationCodeAdmin(admin.ModelAdmin):
    pass

class TeachingTypeCodeAdmin(admin.ModelAdmin):
    pass

class TeachingRoleCodeAdmin(admin.ModelAdmin):
    pass

class GradeCodeAdmin(admin.ModelAdmin):
    pass

class LearningStageCodeAdmin(admin.ModelAdmin):
    pass

class SemesterCodeAdmin(admin.ModelAdmin):
    pass


#admin.site.register(StudentExperience, StudentExperienceAdmin)

#以下动态增加绑定Admin
scope = locals()
for key in scope.keys():
    if key.endswith("Admin") and key is not "Admin":
        admin_model = scope[key]
        model = scope[key[:-5]]
        admin.site.register(model, admin_model)
