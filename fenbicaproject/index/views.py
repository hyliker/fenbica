#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from standard.models import LocationCode
from common.utils import dotdict
from django.db.models import Q
from django.core.paginator import Paginator
from person.models import Person
from django.contrib.auth.decorators import login_required
from django.contrib import messages

REDIRECT_FIELD_NAME = 'next'

# Create your views here.

def my(request):
    """根据权限来显示个人功能导航页面"""
    return render_to_response("index/my.xhtml", {
        "site": u"PingNi.com",
    }, context_instance=RequestContext(request))

def desktop(request):
    """根据权限来显示个人功能导航页面"""
    return HttpResponseRedirect("/person/" + str(request.user.pk))
    return render_to_response("index/desktop.xhtml", {
        "site": u"PingNi.com",
    }, context_instance=RequestContext(request))

def index(request):
    """首页"""
    return render_to_response("index/index.html", {
    }, context_instance=RequestContext(request))

    #if not request.user.is_authenticated():
        #return HttpResponseRedirect("/login")
    #else:
        #return HttpResponseRedirect("/person/" + str(request.user.pk))
        #return HttpResponseRedirect("/my")
    #return render_to_response("index/index.html", {
        #"site": u"PingNi.com",
    #}, context_instance=RequestContext(request))

@never_cache
def login(request, template_name = "index/login.html", redirect_to="/", tpl_vars=dotdict()):
    """登录页面"""
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    next_page = request.REQUEST.get("next", "/desktop/")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me", None)

        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)

        if user is not None:
            #if user.is_active and user.person.identity != user.person.IDENTITY_STUDENT:
            if user.is_active:
                from django.contrib.auth import login
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return HttpResponseRedirect(next_page)
            else:
                print "your account has been disabled!"
        else:
            tpl_vars.error = u"登录帐号或密码错误，请重试"
    return render_to_response(template_name, tpl_vars, context_instance=RequestContext(request))

def logout(request, next_page=None, template_name='index/logout.html', redirect_field_name=REDIRECT_FIELD_NAME):
    "退出系统"
    from django.contrib.auth import logout
    logout(request)
    if next_page is None:
        redirect_to = request.REQUEST.get(redirect_field_name, '')
        if redirect_to:
            return HttpResponseRedirect(redirect_to)
        else:
            return HttpResponseRedirect("/")
            return render_to_response(template_name, {
                'title': "退出",
            }, context_instance=RequestContext(request))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

@login_required
def search(request):
    """搜索页面"""
    if not request.user.is_authenticated():
        messages.error(request, u"只有登陆的用户才有搜索用户")

    context = request.GET.get("context")
    q = request.GET.get("q","")
    page = request.GET.get("page", 1)
    filters = request.GET.get("filters", "").split(",")

    import time
    qstart = time.time()
    if context == "article":
        from article.views import search
        return search(request)
    if context == "person":
        filter = Q(name__icontains=q) | \
                 Q(username__icontains=q) |\
                 Q(abbr_name__icontains=q) |\
                 Q(uuid__icontains=q) |\
                 Q(spell_name__icontains=q)
        if "Staff" in filters and "Student" not in filters:
            filter = filter & Q(identity=Person.IDENTITY_STAFF)
        if "Student" in filters and "Staff" not in filters:
            filter = filter & Q(identity=Person.IDENTITY_STUDENT)
        if "Male" in filters and "Female" not in filters:
            filter = filter & Q(gender=Person.GENDER_MALE)
        if "Female" in filters and "Male" not in filters:
            filter = filter & Q(gender=Person.GENDER_FEMALE)
        #persons = Person.objects.filter(Q(name__icontains=p) | Q(spell_name__icontains=p))
        persons = Person.objects.filter(filter)
        
        search_result = []
        for r in persons:
            search_result.append(r)
    qend = time.time()
    qtime = qend - qstart
    
    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    print query_part
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(search_result, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    
    return render_to_response("index/search.html", {
        "site": u"搜索",
        "search_result": pages.cur_page.object_list,
        "q": q,
        "qtime": qtime,
        "pages":  pages,
        "filters": filters,
    }, context_instance=RequestContext(request))

def manage(request):
    """根据不同人的身份显示不同的管理模块"""

    identity = request.user.person.identity
    if identity.startswith("School"):
        #调用学校的管理模块
        return HttpResponseRedirect("/school/manage")
    elif identity.startswith("Bureau"):
        #调用教育局的管理模块
        pass
    elif identity.startswith("Public"):
        pass

    context = request.GET.get("context")
    return render_to_response("school/manage.html", {
        "site": u"搜索",
    }, context_instance=RequestContext(request))
