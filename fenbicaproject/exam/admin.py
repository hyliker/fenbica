#coding: utf-8
from django.contrib import admin
from exam.models import *
from exam.forms import ResultForm 

class SubjectInline(admin.TabularInline):
#class SubjectInline(admin.StackedInline):
    model = Subject
    fields = ("grade", "category", "full_score",)
    #can_delete = False
    extra = 1

class ExamAdmin(admin.ModelAdmin):
    date_hierarchy = 'dtstart'
    list_display = ("category", "learning_year", "semester", "exam_type", "dtstart", "dtend")
    list_filter = ("category", "dtstart", "semester", "exam_type")
    list_per_page = 50
    search_fields = ["category", "learning_year", "semester__name", "exam_type__name"]
    inlines = (SubjectInline,)

admin.site.register(Exam, ExamAdmin)

class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "student_gender", "klass", "student_uuid", "subject", "score", "level")
    list_filter = ("level", "subject", "status" )
    list_per_page = 50
    raw_id_fields = ("student", "klass", "subject")
    search_fields = ("student__spell_name", "student__name", "student__abbr_name", "subject__category__name", "score", "level__name") 

    form = ResultForm

    def student_gender(self, obj):
        return obj.student.gender
    student_gender.short_description = "性别"

    def student_uuid(self, obj):
        return obj.student.pk
    student_uuid.short_description = "编号"

    def student_class(self, obj):
        try:
            class_ = obj.student.classes.filter(dtcreated__year=obj.exam_course.exam.learning_year[:4])[0].name
        except Exception,e:
            print e
            class_ = None
        return class_
    student_class.short_description = "班别"

    def save_model(self, request, obj, form, change):
        obj.creator = request.person
        obj.save()

admin.site.register(Result, ResultAdmin)

class SubjectAdmin(admin.ModelAdmin):
    date_hierarchy = "dtstart"
    list_display = ("exam", "grade", "category", "learning_stage", "exam_mode", "full_score")
    list_filter = ("category", "grade", "dtstart", "exam_mode")
    list_per_page = 50
    search_fields = ("exam", "category", "learning_stage", "grade")
admin.site.register(Subject, SubjectAdmin)

class ExamCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
admin.site.register(ExamCategory, ExamCategoryAdmin)

class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
admin.site.register(SubjectCategory, SubjectCategoryAdmin)


class SeatAdmin(admin.ModelAdmin):
    list_display = ("examinee", "klass", "exam", "room", "uuid", "row", "col")
    search_fields = ("examinee__name", "examinee__username", "examinee__spell_name",)
    raw_id_fields = ("room", "examinee")
    def exam(self, obj):
        return obj.room.exam
admin.site.register(Seat, SeatAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ("exam","name", "grade", "seat_num", "col_num", "examiner_list")
    raw_id_fields = ("examiner",)
    list_filter = ("grade", )
    search_fields = ("exam__name", "examiner__name", "examiner__username", "examiner__spell_name")
    def examiner_list(self, obj):
        examiner_list = obj.examiner.all()
        examiner_list_links = [u'<a href="/person/%s">%s</a>' % (m.pk, m.name) for m in examiner_list]
        return u", ".join(examiner_list_links)
    examiner_list.allow_tags = True
    examiner_list.short_description = u"考官名单"

admin.site.register(Room, RoomAdmin)
