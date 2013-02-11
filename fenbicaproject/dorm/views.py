#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
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
from person.models import Person
from django.db.models import Sum
from dorm.models import Bedchamber, Bed, Boarder, Check, Latelog
from django.contrib.auth.decorators import login_required

REDIRECT_FIELD_NAME = 'next'

@login_required
@render_to("dorm/index.html")
def index(request, template=None):
    return HttpResponseRedirectView("dorm_bedchamber_list")
    #bedchamber_list = Bedchamber.objects.all()
    #years = Bedchamber.objects.dates("dtcreated", "month")
    #return {"bedchamber_list": bedchamber_list, "years": years}, template

@login_required
@render_to("dorm/bedchamber.html")
def bedchamber(request, bedchamber_pk=None, template=None):
    bedchamber = get_object_or_404(Bedchamber, pk=bedchamber_pk)
    return {"bedchamber": bedchamber}, template


@login_required
@render_to("dorm/bedchamber_list.html")
def bedchamber_list(request, template=None):
    q = request.GET.get("q", "")
    page = request.GET.get("page", 1)

    filter = Q()
    if q:
        filter = filter & Q(uuid=q)
    bedchamber_list = Bedchamber.objects.filter(filter)
    years = Bedchamber.objects.dates("dtcreated", "month")

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    print query_part
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(bedchamber_list, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return {
        "bedchamber_list": pages.cur_page.object_list, 
        "years": years,
        "q": q,
        "pages":  pages,
    }, template

@login_required
@render_to("dorm/boarder_list.html")
def boarder_list(request, template=None):
    bedchamber_pk  = request.GET.get("bedchamber_pk", None)
    filter = Q()
    title = ""
    if bedchamber_pk:
        filter = filter & Q(bed__bedchamber=bedchamber_pk)
        title += u"%s 寝室" % bedchamber_pk
    boarder_list = Boarder.objects.filter(filter)

    return {"boarder_list": boarder_list, "title": title}, template

@login_required
@render_to("dorm/check_list.html")
def check_list(request, template=None):
    bedchamber_pk = request.GET.get("bedchamber_pk", None)
    year = request.GET.get("year", None)
    month = request.GET.get("month", None)
    page = request.GET.get("page", 1)

    title = u""
    filter = Q()
    if bedchamber_pk:
        filter = filter & Q(bedchamber__uuid=bedchamber_pk)
        bedchamber = get_object_or_404(Bedchamber, pk=bedchamber_pk)
        title += u" %s 寝室" % unicode(bedchamber)
    if year:
        filter = filter & Q(dtchecked__year=year)
        title += u" %s 年" % unicode(year)
    if month:
        filter = filter & Q(dtchecked__month=month)
        title += u" %s 月份" % unicode(month)
    check_list = Check.objects.filter(filter)


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
        "title": title, 
        "bedchamber_pk": bedchamber_pk, 
        "pages": pages,
    }, template

@login_required
@render_to("dorm/check_summary.html")
def check_summary(request, year=None, month=None, template=None):
    """考核汇总评比"""
    filter = Q()
    if not (year and month):
        try:
            latest_check = Check.objects.latest("dtchecked")
            year = latest_check.dtchecked.year
            month = latest_check.dtchecked.month
        except Check.DoesNotExist,e:
            year = None
            month = None
    if year:
        filter = filter & Q(dtchecked__year=year)
    if month:
        filter = filter & Q(dtchecked__month=month)

    #filter = Q(dtchecked__year=year) & Q(dtchecked__month=month)
    check_list = Check.objects.filter(filter).\
            values("bedchamber", "bedchamber__master__pk", "bedchamber__dtcreated", "bedchamber__master__name").\
            annotate(Sum("sum_ranking")).order_by("-sum_ranking__sum")
    print check_list

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
@render_to("dorm/latelog_list.html")
def latelog_list(request, template=None):
    """住宿生晚归记录"""
    q = request.GET.get("q", "")
    page = request.GET.get("page", 1)

    filter = Q()
    if q:
        filter = filter & Q(uuid=q)
    latelog_list = Latelog.objects.filter(filter)
    years = Latelog.objects.dates("dtcreated", "month")

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    print query_part
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(latelog_list, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return {
        "latelog_list": pages.cur_page.object_list, 
        "years": years,
        "q": q,
        "pages":  pages,
    }, template
