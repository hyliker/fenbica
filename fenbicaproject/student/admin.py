#coding: utf-8
from django.contrib import admin
from student.models import *
from student.forms import StudentForm
#from exam.models import *

def student_gender(self, obj):
    return obj.student.gender.name
student_gender.short_description = u"性别"

#class ExamResultAdminInline(admin.TabularInline):
    #model = ExamResult

class StudentAdmin(admin.ModelAdmin):
    date_hierarchy = "birthday"
    list_display = ("name", "uuid", "id_no", "gender", "birthday", "dtenroll", "dtmodify", "student_profile")
    list_filter = ("gender", "archive_create_reason", "enrollment_type", "dtenroll", "student_type", "is_active", "is_leaved"  )
    list_per_page = 50
    exclude = ("identity", )
    form = StudentForm
    search_fields = ("name", "spell_name", "username", "uuid", "id_no")
    raw_id_fields = ("nationality", "born_place", "native_place", "folk", "archive_administrator", "original_area" )
    readonly_fields = ("archive_approver", "latest_classgrade") 
    #inlines = [ExamResultAdminInline]
    #readonly_fields = ("user", "identity")
    fieldsets = (
        (u"基本信息", {
            "fields": (
                ("name", "used_name"),
                ("gender", "id_no", "birthday"), 
                ("spell_name", "abbr_name"),
                ("first_name", "last_name"),
                "uuid", ("domicle_location", "domicle_type"), 
                ("dtrudui", "dtrutuan"),
                ("postal_address", "postal_code"),
                ("residence_address", "telephone"),
                ("folk", "nationality", "born_place", "native_place"),
                ("politics","diploma", "marriage"),
                ("emigrant", "health", "blood_type"),
                ("is_floating", "is_singleton", "religion"),
                )
        }),
        (u"个人信息", {
            "classes": ("collapse", ),
            "fields": (
                "photo", "homepage", "interest", "fortes",
            )
        }),
        (u"学校信息", {
            #"classes": ("collapse", )
            #"description": u"学校相关的信息",
            "fields": (
                ("dtenroll", "enrollment_type", "student_type",),
                ("original_school_name", "original_school_code"), 
                ("original_area", "source_type", "attendance_type", "graduate_score",),
                ("archive_cancel_date", "archive_cancel_reason"),
                ("archive_approver", "archive_administrator",),
                ("is_leaved", "latest_classgrade", "archive_create_reason"),
                ("archive_remark",)
            )
        }),
        (u"帐号信息", {
            "classes": ("collapse", ),
            "fields": (
                ("username", "password"),
                ("email","is_active"),
                ("last_login", "date_joined"),
                "groups", "user_permissions",
              )
        }),
    )

    def student_profile(self, obj):
        from django.core import urlresolvers
        change_url = urlresolvers.reverse('admin:student_student_change', args=(obj.student.pk,))
        return '''<a href="%s" target="_blank">查看</a> / 
                  <a href="%s" target="_blank">编辑</a>''' %  (obj.student.get_absolute_url(), change_url)
    student_profile.allow_tags = True
    student_profile.short_description = u"学生档案"

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get("password", None)
        if not change:
            if password is None:
                obj.set_unusable_password()
            else:
                obj.set_password(password)
        obj.save()

class ExperienceAdmin(admin.ModelAdmin):
    date_hierarchy = "dtstart"
    list_display = ("student", "dtstart", "dtend", "school_name", "duty", "attestor",) 
    search_fields = ("student__name", "school_name", "duty", "attestor", "remark")
    raw_id_fields = ("student",)

class KeeperAdmin(admin.ModelAdmin):
    list_display = ("student", "name", "relation", "telephone", "postal_address", "postal_code", "email" )
    list_filter = ("relation",)
    search_fields = ("student__name",)
    raw_id_fields = ("student", "relation")

class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ("student", "name", "relation", "company", "folk", "marriage", "telephone", "emigrant")
    list_filter = ("relation",)
    search_fields = ("student__name", "company")
    raw_id_fields = ("student", "relation", "folk", "emigrant")

class RegisterAdmin(admin.ModelAdmin):
    date_hierarchy = "actual_date" 
    list_display = ("student", "learning_stage", "learning_year", "semester", "grade", "classgrade", "status")
    list_filter = ("learning_stage", "semester", "grade")
    search_fields = ("student__name",) 
    raw_id_fields = ("student", "classgrade")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("student", "learning_stage", "learning_year", "semester", "grade", "teacher", "comment")
    list_filter = ("learning_stage", "grade", "semester")
    search_fields = ("student__name", "teacher__name", "comment")
    raw_id_fields = ("student",)

    def save_model(self, request, obj, form, change):
        obj.teacher = request.person.staff
        obj.save()

class RewardsAdmin(admin.ModelAdmin):
    list_display = ("student", "name", "level","type", "money", "file_no", "date", "bureau")
    list_filter = ("name", "level", "type")
    search_fields = ("student__name", "causation")
    raw_id_fields = ("student",)

class PunishmentAdmin(admin.ModelAdmin):
    list_display = ("student", "student_gender", "student_uuid", "name", "date", "file_no", "repeal_date", "repeal_file_no")
    list_filter = ("name", )
    search_fields = ("student__name", "causation",)
    raw_id_fields = ("student",)

    def student_gender(self, obj):
        return obj.student.gender
    student_gender.short_description = "性别"

    def student_uuid(self, obj):
        return obj.student.pk
    student_uuid.short_description = "编号"

#class EnrollmentAdmin(admin.ModelAdmin):
    ##list_display = ("student", "original_school_name", "date", "type", "graduate_score")
    #date_hierarchy = "date"
    #list_display = ("student", "original_area", "original_school_name", "date", "graduate_score", )
    #search_fields = ("studen__name", "orginal_school_name")
    #list_filter = ("type", "attendance_type", "original_student")
    #list_per_page = 25
    #raw_id_fields = ("student", "original_area")

class GraduateAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ("student", "direction", "date", "comment")  
    list_filter = ("direction",)
    search_fields = ("student__name", "comment")
    raw_id_fields = ("student",)

class TransferAdmin(admin.ModelAdmin):
    list_display = ("student", "type", "date", "auditing_date", "original_school_name", "target_school_code", "status" )
    list_filter = ("status", "type", )
    search_fields = ("student__name", "result")
    raw_id_fields = ("student",)

class AssistanceAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ("student", "learning_stage", "learning_year", "grade", "semester", "date", "amount", "implementator")
    list_filter = ("learning_stage", "semester", "grade")
    search_fields = ("student__name", "implementator__name", "reason")
    raw_id_fields = ("student",)

class FinishStudyAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "education_result")
    list_filter = ("education_result",)
    search_fields = ("student__name", "causation")
    raw_id_fields = ("student",)

class DrillAdmin(admin.ModelAdmin):
    date_hierarchy = "dtstart"
    list_display = ("student", "dtstart", "dtend", "troops", "result")
    search_fields = ("student__name","student__uuid")
    raw_id_fields = ("student",)

class AttendanceAdmin(admin.ModelAdmin):
    date_hierarchy = "dtchecked"
    list_display = ("student", "classgrade", "event", "dtchecked", "checker", "creator")
    list_filter = ("event", "result", "dtchecked")
    raw_id_fields = ("student", "classgrade", "checker")

    def save_model(self, request, obj, form, change):
        if obj.checker is None:
            obj.checker = request.person
        obj.creator = request.person
        obj.save()

class AttendanceResultAdmin(admin.ModelAdmin):
    list_display = ("name", "score",)

class CollegeEnrolleeLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')

class CollegeEnrolleeAdmin(admin.ModelAdmin):
    date_hierarchy = "dtenrolled"
    list_display = ("uuid", "student", "level", "student_gender", "college", "major", "dtenrolled", "priority", "is_approved")
    search_fields = ("uuid", "student__name", "college")
    raw_id_fields = ("student",)

    student_gender = student_gender

class ZhongKaoEnrolleeAdmin(admin.ModelAdmin):
    date_hierarchy = "dtenrolled"
    list_display = ("uuid", "student", "student_gender", "school", "dtenrolled", "priority", "is_approved")
    search_fields = ("uuid", "student__name", "school")
    raw_id_fields = ("student",)

    student_gender = student_gender


#admin.site.register(Experience, ExperienceAdmin)

#以下动态增加绑定Admin
scope = locals()
for key in scope.keys():
    if key.endswith("Admin") and key is not "Admin":
        admin_model = scope[key]
        model = scope[key[:-5]]
        admin.site.register(model, admin_model)
