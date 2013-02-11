#coding: utf-8
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from classgrade.models import *
from classgrade.forms import *

class ClassmateInline(admin.TabularInline):
    model = Classmate 
    #can_delete = False
    extra = 0
    form = ClassmateInlineForm
    raw_id_fields = ("student", "klass")

#class CourseInline(admin.TabularInline):
    #model = Course
    #extra = 0
    #form = CourseInlineForm
    #raw_id_fields = ("klass", "course")

class ClassAdmin(admin.ModelAdmin):
    date_hierarchy = "dtcreated"
    list_display = ("uuid", "grade", "name", "dtcreated", "master", "monitor", "student_number", "type" )
    list_filter = ("grade", "type")
    search_fields = ("uuid", "master__name", "name",)
    list_per_page = 25
    raw_id_fields = ("master", "monitor", "classroom")
    #inlines = (CourseInline, ClassmateInline, )
    inlines = (ClassmateInline, )
    list_select_related = True
    actions = ['arrange_class']
    #prepopulated_fields = {"uuid": ("dtcreated", "grade")}
    #inlines = (CourseInline, )

    #fieldsets = (
        #(u"基本信息", {
            #"fields": (
                #("grade", "name", "dtcreated"),
                #("master", "monitor", "type"),
            #)
        #}),
    #)
    def arrange_class(self, request, queryset):
        selected_class = queryset.values_list("pk", flat=True)
        from django.core.urlresolvers import reverse
        next_url = u"%s?ids=%s" % (reverse("classgrade_class_arrange"), ",".join([str(s) for s in selected_class]))
        return HttpResponseRedirect(next_url)
    arrange_class.short_description = u'班级升级编排'

admin.site.register(Class, ClassAdmin)

#class CourseAdmin(admin.ModelAdmin):
    #date_hierarchy = "dtstart"
    #list_display = ("klass", "course", )
    #search_fields = ("klass__uuid", "course__uuid")
    #raw_id_fields = ("klass", "course")
#admin.site.register(Course, CourseAdmin)

class CheckAdmin(admin.ModelAdmin):
    date_hierarchy = "dtchecked"
    list_display = ("klass", "klass__teacher", "dtchecked", "sum_ranking", "checker")
    search_fields = ("klass__master__name", "klass__master__username", "klass__master__spell_name", "klass__uuid")
    list_filter = ("dtchecked",)
    raw_id_fields = ("klass",)

    #fieldsets = (
        #(u"班级", {
            #"fields": (("klass", "dtchecked", "checker"),)
        #}),
        #(u"考勤", {
            #"fields": (("early_moring_ranking", "morning_ranking", "afternoon_ranking", "evening_ranking"),)
        #}),
        #(u"其他", {
            #"fields": (("student_attendance_ranking", "school_uniform_ranking", "classroom_order_ranking", "hairstyle_finery_ranking"), 
                       #("smoke_drink_ranking", "game_ranking", "classroom_discipline_ranking", "home_visiting_ranking"))
        #}),
    #)

    def klass__teacher(self, obj):
        return obj.klass.master
    klass__teacher.short_description = u"班主任"

    def save_model(self, request, obj, form, change):
        if obj.checker is None:
            obj.checker = request.person
        obj.creator = request.person
        obj.save()

admin.site.register(Check, CheckAdmin)

class ClassmateAdmin(admin.ModelAdmin):
    date_hierarchy = "dtstart"
    list_display = ("student","student_gender", "student_uuid", "klass", "uuid", "dtstart", "dtend", "student_profile")
    search_fields = ("student__username", "student__name", "student__uuid", "klass__uuid")
    raw_id_fields = ("student", "klass")
    list_display_links = ("uuid", "student")
    list_filter = ("dtstart", "dtend")
    #readonly_fields = ("uuid",)
    form = ClassmateForm
    actions = ['make_published']

    def student_gender(self, obj):
        return obj.student.gender
    student_gender.short_description = "性别"
    student_gender.admin_order_field = 'student__gender'

    def student_uuid(self, obj):
        return obj.student.uuid
    student_uuid.short_description = "编号"
    student_uuid.admin_order_field = 'student__uuid'

    def student_profile(self, obj):
        from django.core import urlresolvers
        change_url = urlresolvers.reverse('admin:student_student_change', args=(obj.student.pk,))
        return '''<a href="%s" target="_blank">查看</a> / 
                  <a href="%s" target="_blank">编辑</a>''' %  (obj.student.get_absolute_url(), change_url)
    student_profile.allow_tags = True
    student_profile.short_description = u"学生档案"

    def make_published(self, request, queryset):
        #queryset.update(status='p')
        return HttpResponse("OK")
    make_published.short_description = u'班级调整'


    #def save_model(self, request, obj, form, change):
        #if not change: #created 
            #from django.db.models import Max
            #max_uuid = Classmate.objects.filter(klass=obj.klass_id).aggregate(Max("uuid")).get("uuid__max")
            #if max_uuid is None:
                #new_uuid = u"%s%s" % (obj.klass_id, "001") 
            #else:
                #new_uuid = str(int(max_uuid + 1))
            #obj.uuid = new_uuid
        #obj.save()

admin.site.register(Classmate, ClassmateAdmin)

class LeaderAdmin(admin.ModelAdmin):
    date_hierarchy = "dtstart"
    list_display = ("klass", "student", "person_gender", "duty", "dtstart", "dtend")
    search_fields = ("klass__uuid", "student__username", "student__name", "student__uuid")
    list_filter = ("duty", "dtstart")
    raw_id_fields = ("klass", "student",)

    def person_gender(self, obj):
        return obj.student.gender
    person_gender.short_description = u"性别"

admin.site.register(Leader, LeaderAdmin)

class TimenoAdmin(admin.ModelAdmin):
    list_display = ("learning_year", "semester", "number", "dtstart", "dtend")

admin.site.register(Timeno, TimenoAdmin)

class TimetableAdmin(admin.ModelAdmin):
    list_filter = ("week", "timeno")
    raw_id_fields = ("klass", "timeno", "course")

admin.site.register(Timetable, TimetableAdmin)
