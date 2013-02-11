#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from common.utils import dotdict
from django.db.models import Q
from django.core.paginator import Paginator
from page.models import Scenery, PhoneCategory, Teacher

def scenery_index(request):
    scenery = Scenery.objects.filter(is_published=True).order_by("-display_order")
    return render_to_response("school/scenery_index.xhtml", {
        "scenery": scenery,
    }, context_instance=RequestContext(request))

def service_index(request):
    phone_category = PhoneCategory.objects.all()
    return render_to_response("school/service_index.xhtml", {
        "phone_category": phone_category,
    }, context_instance=RequestContext(request))

def teacher_index(request):
    """师资队伍"""
    teachers = Teacher.objects.filter(is_published=True).order_by("-display_order")
    return render_to_response("school/page_teacher_index.xhtml", {
        "teachers": teachers,
    }, context_instance=RequestContext(request))

def college_enroll_index(request):
    """高考录取榜"""
    from student.models import CollegeEnrollee
    enrollee = CollegeEnrollee.objects.filter(is_approved=True)
    return render_to_response("school/page_college_enroll_index.xhtml", {
        "enrollee": enrollee,
    }, context_instance=RequestContext(request))
