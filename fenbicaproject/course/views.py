#coding: utf-8
import json
import datetime
from collections import defaultdict
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.db.models import get_model
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import F, Count, Q
from person.models import Person
from django.views.decorators.cache import cache_page
from course.models import Course
from utils.django_snippets import render_to, JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
@render_to("course/index.xhtml")
def index(request, template=None):
    try:
        latest_course = Course.objects.latest("teaching_year")
    except:
        return HttpResponse(u"暂时还没有课程可供选择")
    filter = Q(teaching_year = latest_course.teaching_year) & \
             Q(semester = latest_course.semester)
    courses = Course.objects.filter(filter)

    return {
        "courses": courses,
        "latest_course": latest_course,
    }, template


@login_required
@render_to("course/course.html")
def course(request, course_pk, template=None):
    """查看某一课程详情"""
    course = get_object_or_404(Course, pk=course_pk)
    fields = []
    for field in course._meta._fields():
        fields.append(field)
        val = getattr(course, field.name)
        setattr(field, "value", val)
    setattr(course, "fields", fields)

    return {"course": course}, template


@login_required
@render_to("course/add_course.xhtml")
def add_course(request, template=None):
    """添加新开的课程"""
    from course.forms import AddCourseForm
    if request.method == "POST":
        form = AddCourseForm(request.POST)
        if form.is_valid():
            _form = form.save(commit=False)
            _form.teacher = request.user.person.staff
            _form.save()
            form.success = True
    elif request.method == "GET":
        form = AddCourseForm()
    return {"form": form}

@login_required
@render_to("course/my_course.xhtml")
def my_course(request, template=None):
    print request.person
    courses = get_list_or_404(Course, teacher=request.user.person)
    return {"courses": courses}, template


@login_required
@render_to("course/person_course.html")
def person_course(request, person_pk=None, template=None):
    """某人的课程"""
    person = get_object_or_404(Person, pk=person_pk)
    if person.identity == Person.IDENTITY_STAFF:
        course_list = Course.objects.filter(teacher=person)
    elif person.identity == Person.IDENTITY_STUDENT:
        course_list = []
    else:
        course_list = Course.objects.none()

    return {"person": person, "course_list": course_list}, template

@login_required
@render_to("course/timetable.html")
def timetable(request, template=None):
    """老师的课程表"""
    from classgrade.models import Timeno, Class, Timetable
    from staff.models import Staff
    from standard.models import SemesterCode

    teacher_pk = request.GET.get("teacher_pk", None)
    semester_pk = request.GET.get("semester_pk", None)
    learning_year = request.GET.get("learning_year", None)

    teacher = get_object_or_404(Staff, pk=teacher_pk)

    course_list = get_list_or_404(Course, teacher=teacher_pk)
    def semester_timetable(learning_year, semester):
        timeno = Timeno.objects.filter(learning_year=learning_year, semester=semester).order_by("number")
        timetable_ds = []
        for t in timeno:
            tn = {0: t}
            for w in range(1, 8):
                tn[w] = None
            timetable_ds.append(tn)

        try:
            timetable = Timetable.objects.filter(course__teacher=teacher_pk)
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
        for semester in range(1, 3):
            st = semester_timetable(learning_year, semester)
            timetable_ds.append(st)
    else:
        st = semester_timetable(learning_year, semester_pk)
        timetable_ds.append(st)

    return {
        "timetable_ds": timetable_ds, 
        "teacher": teacher, 
        "learning_year": learning_year 
    }, template
