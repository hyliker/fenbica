#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.views.decorators.cache import never_cache
from standard.models import LocationCode
from common.utils import dotdict
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from utils.django_snippets import render_to, HttpResponseRedirectView
from classgrade.models import Class, Timeno, Classmate, Check
from standard.models import SemesterCode, GradeCode
from person.models import Person
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

REDIRECT_FIELD_NAME = 'next'

@login_required
@render_to("classgrade/timetable.html")
def timetable(request, klass_pk=None, semester_pk=None, template=None):
    """班级课程表"""
    klass = get_object_or_404(Class, pk=klass_pk)
    def semester_timetable(klass, semester):
        timeno = Timeno.objects.filter(learning_year=klass.learning_year, semester=semester).order_by("number")
        timetable_ds = []
        for t in timeno:
            tn = {0: t}
            for w in range(1, 8):
                tn[w] = None
            timetable_ds.append(tn)

        try:
            timetable = klass.timetable_set.all()
        except:
            timetable = []
        for t in timetable:
            timeno = t.timeno.number -1
            try:
                timetable_ds[timeno][t.week] = t
            except Exception, e:
                print e
        return timetable_ds

    timetable_ds = []
    if semester_pk is None:
        print "semester"
        for semester in range(1, 3):
            st = semester_timetable(klass, semester)
            timetable_ds.append(st)
    else:
        st = semester_timetable(klass, semester_pk)
        timetable_ds.append(st)

    return {"timetable_ds": timetable_ds, "klass": klass, "semester": semester_pk}, template

#@render_to("classgrade/index.html")
def index(request, template=None):
    return redirect("/classgrade/class/list/")
    #return HttpResponseRedirectView("classgrade.views.klass_list")
    #klasses = Class.objects.all()
    #klass_years = Class.objects.dates("dtcreated", "year")
    #print "years", klass_years
    #return {"klasses": klasses, "klass_years": klass_years}, template


@login_required
@render_to("classgrade/class.html")
def klass(request, klass_pk=None, template=None):
    klass = get_object_or_404(Class, pk=klass_pk)
    return {"klass": klass}, template

@login_required
@render_to("classgrade/class_list.html")
def klass_list(request, klass_year=None, klass_grade=None, template=None):
    """年级班级列表"""
    klass_years = [ str(d.year) for d in Class.objects.dates("dtcreated", "year")]
    klass_years.sort(reverse=True)
    if klass_year is None:
        latest_class = Class.objects.latest("dtcreated")
        klass_year = latest_class.dtcreated.year
    if klass_grade:
        klasses = get_list_or_404(Class, dtcreated__year=klass_year, grade=klass_grade)
    else:
        klasses = get_list_or_404(Class, dtcreated__year=klass_year)
    grades = Class.objects.values("grade_id", "grade__name").annotate()
    return {
        "klasses": klasses, 
        "klass_years": klass_years, 
        "klass_year": klass_year,
        "grades": grades,
        "klass_grade": klass_grade,
    }, template

@login_required
@render_to("classgrade/my_timetable.html")
def my_timetable(request, template=None):
    return {}, template


@login_required
@render_to("classgrade/classmate_list.html")
def classmate_list(request, template=None):
    klass_pk = request.GET.get("klass_pk", None)
    grade_pk = request.GET.get("grade_pk", None)
    year = request.GET.get("year", None)
    filter = Q()
    title = ""
    if klass_pk:
        filter = filter & Q(klass=klass_pk)
        klass = get_object_or_404(Class, pk=klass_pk)
        title = klass
    elif grade_pk and year:
        filter = filter & Q(klass__grade=grade_pk) & Q(klass__dtcreated__year=year)
        grade = get_object_or_404(GradeCode, pk=grade_pk)
        title = u"%s 年度 %s" % (year ,grade.name)
    classmate_list = Classmate.objects.filter(filter)
    return {
        "classmate_list": classmate_list,
        "title": title,
        "klass_pk": klass_pk,
    }, template


@login_required
@render_to("classgrade/person_class_list.html")
def person_class_list(request, person_pk=None, template=None):
    person = get_object_or_404(Person, pk=person_pk)
    if person.identity == Person.IDENTITY_STUDENT:
        class_list = person.student.classes.all().order_by("-dtcreated")
    elif person.identity == Person.IDENTITY_STAFF:
        class_list = person.staff.class_set.all()
    else:
        class_list = []
    return {"class_list": class_list}, template

@login_required
@render_to("classgrade/check_index.html")
def check_index(request, template=None):
    page = request.GET.get("page", 1)
    q = request.GET.get("q", "")

    if not q:
        filter = Q()
    else:
        filter = Q(klass__uuid=q) | \
                 Q(klass__name__icontains=q) | \
                 Q(klass__master__username__icontains=q)  | \
                 Q(klass__master__name__icontains=q)  | \
                 Q(klass__master__uuid__icontains=q)  | \
                 Q(checker__name__icontains=q)  | \
                 Q(checker__username__icontains=q)  | \
                 Q(checker__uuid__icontains=q)

    #check_list = Check.objects.filter(filter).extra(
        #{"ranking": 'early_morning_ranking + morning_ranking + afternoon_ranking + evening_ranking + \
                     #student_attendance_ranking + school_uniform_ranking +  \
                     #classroom_order_ranking + hairstyle_finery_ranking + smoke_drink_ranking + \
                     #game_ranking + classroom_discipline_ranking + home_visiting_ranking + other_ranking '
        #} 
    #).order_by("-dtchecked", "-ranking")

    check_list = Check.objects.filter(filter).order_by("-dtchecked", "-sum_ranking")

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    print query_part
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(check_list, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return {
        "check_list": pages.cur_page.object_list,
        "pages":  pages,
        "q": q,
    }, template

@login_required
@render_to("classgrade/check.html")
def check(request, check_pk=None, template=None):
    check = get_object_or_404(Check, pk=check_pk)
    return {"check": check}, template

@login_required
@render_to("classgrade/check_list.html")
def check_list(request, template=None):
    klass_pk = request.GET.get("klass_pk", None)
    year = request.GET.get("year", None)
    month = request.GET.get("month", None)

    title = u""
    filter = Q()
    if klass_pk:
        filter = filter & Q(klass__uuid=klass_pk)
        klass = get_object_or_404(Class, pk=klass_pk)
        title += unicode(klass)
    if year:
        filter = filter & Q(dtchecked__year=year)
        title += u" %s 年" % unicode(year)
    if month:
        filter = filter & Q(dtchecked__month=month)
        title += u" %s 月份" % unicode(month)
    check_list = Check.objects.filter(filter)
    return {"check_list": check_list, "title": title, "klass_pk": klass_pk}, template


@login_required
@render_to("classgrade/check_summary.html")
def check_summary(request, year=None, month=None, template=None):
    """考核汇总评比"""
    filter = Q()
    if not (year and month):
        try:
            latest_check = Check.objects.latest("dtchecked")
            year = latest_check.dtchecked.year
            month = latest_check.dtchecked.month
        except Check.DoesNotExist,e:
            pass
    if year:
        filter = filter & Q(dtchecked__year=year)
    if month:
        filter = filter & Q(dtchecked__month=month)
            #filter = Q(dtchecked__year=year) & Q(dtchecked__month=month)
    check_list = Check.objects.filter(filter).\
            values("klass", "klass__name", "klass__master__name", "klass__master__pk").\
            annotate(Sum("sum_ranking")).order_by("-sum_ranking__sum")

    #以下增加并列排名信息
    if check_list:
        pre_check = check_list[0]
        pre_check["ranking"] = 1
        for k,v in enumerate(check_list):
            if v["sum_ranking__sum"] == pre_check["sum_ranking__sum"]:
                v["ranking"] = pre_check["ranking"]
            else:
                v["ranking"] = k + 1
            pre_check = v

    return {"check_list": check_list, "year": year, "month": month }, template

@login_required
@render_to("classgrade/student_comment_list.html")
def student_comment_list(request, template=None):
    """学生学期评语"""
    try:
        class_list = Class.objects.filter(master=request.person.staff)
        classmate_list = class_list[0].classmate_set.all()
    except Exception, e:
        return HttpResponseForbidden(u"暂无相关信息")

    return {
        "class_list": class_list,
        "classmate_list": classmate_list,
    }, template


@login_required
@render_to("classgrade/student_comment_edit.html")
def student_comment_edit(request, classmate_pk=None, template=None):
    from student.forms import CommentByMasterForm
    from student.models import Comment, Student
    from standard.models import GradeCode

    pk = request.POST.get("pk", None)
    classmate = get_object_or_404(Classmate, pk=classmate_pk)
    semester = request.GET.get("semester", 1)
    if pk:
        comment = get_object_or_404(Comment, pk=pk)
    else:
        comment = Comment(learning_year=classmate.klass.learning_year, semester_id=semester)

    form = CommentByMasterForm(request.POST or None, instance=comment)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.student = get_object_or_404(Student, pk=request.POST.get("student"))
        comment.teacher = request.person.staff
        comment.grade = classmate.klass.grade
        comment.save()
        #redirect_url = reverse("student_family_member_list", args=[new_family_member.student_id])
        #return HttpResponseRedirect(redirect_url)
    return {
        "form": form,
        "classmate": classmate,
    }, template
