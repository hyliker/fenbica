#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import never_cache
from standard.models import LocationCode
from common.utils import dotdict
from django.db.models import Q
from django.core.paginator import Paginator
from person.models import Person
from utils.django_snippets import render_to, HttpResponseRedirectView
from django.contrib.auth.decorators import login_required
from person.forms import EditSelfPersonForm
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from config.models import SystemSetting

REDIRECT_FIELD_NAME = 'next'

# Create your views here.

def settings(request):
    """设置主页"""
    redirect_url =  reverse("password_change")
    return HttpResponseRedirect(redirect_url)

def index(request,profileID):
    """首页"""
    return render_to_response("person/index.html", {
        "site": u"PingNi.com",
        "profileID": profileID,
    }, context_instance=RequestContext(request))

@login_required
@render_to("person/details.html")
def person(request, person_pk=None, template=None):
    """查看某人的档案资料库"""
    person = get_object_or_404(Person, pk=person_pk)
    if not request.user.has_perm("student.can_view"):
        if request.user.pk != person.pk:
            return HttpResponseForbidden(u"无权限")

    if person.identity == person.IDENTITY_STAFF:
        person = person.staff
        template = "staff/details.html"
    elif person.identity == person.IDENTITY_STUDENT:
        person = person.student
        template = "student/details.html"
    return  {"person": person}, template


@login_required
@render_to("person/edit_person.html")
def edit_person(request, person_pk, template=None):
    """编辑自己的档案信息"""
    #try:
        #cfg = SystemSetting.objects.get(key="ALLOW_EDIT_PERSON_PROFILE_BY_MYSELF")
        #if not cfg.value.lower() in ["yes", "1"]:
            #return HttpResponseForbidden("暂不允许编辑自己的档案信息")
    #except Exception,e:
        #pass

    person = get_object_or_404(Person, pk=person_pk)
    if request.person != person:
        return HttpResponseForbidden(u"没有权限编辑别人的档案信息")

    if request.method == "GET":
        if person.identity == person.IDENTITY_STAFF:
            from staff.views import edit_staff
            return edit_staff(request, person_pk)
        elif person.identity == person.IDENTITY_STUDENT:
            from student.views import edit_student
            return edit_student(request, person_pk)
        else:
            form = EditSelfPersonForm(instance=person)

    elif request.method == "POST":
        if request.FILES.has_key("photo"):
            form = EditSelfPersonForm(request.POST, request.FILES, instance=person)
        else:
            form = EditSelfPersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, u"嘿，你已经保存了你刚才编辑的个人基本信息")
            return HttpResponseRedirectView("person.views.person", person_pk=person_pk)
        else:
            messages.error(request, u"嘿，填写有错，请更正表单红色标记的错误后，再保存")
    else:
        form = EditSelfPersonForm(instance=person)
    return {"form": form}, template


@login_required
def edit_staff(request, profileID):
    from staff.forms import MyStaffForm
    from staff.models import Staff
    return render_to_response("school/edit_staff.xhtml", {
        "site": u"PingNi.com",
        "form": MyStaffForm(instance = Staff.objects.get(pk=profileID))
    }, context_instance=RequestContext(request))


@login_required
def edit_profile(request, profileID):
    context = request.GET.get("context", "index")
    person = Person.objects.get(pk=profileID)
    if person.identity == "School.Staff":
        from staff.views import edit_staff_by_myself
        return edit_staff_by_myself(request, profileID)

        #from staff.forms import MyStaffForm
        #from staff.models import Staff
        #return render_to_response("school/edit_staff.xhtml", {
            #"site": u"PingNi.com",
            #"form": MyStaffForm(instance = Staff.objects.get(pk=profileID))
        #}, context_instance=RequestContext(request))
    elif person.identity == "School.Student":
        from student.forms import StudentForm
        return render_to_response("school/edit_student.xhtml", {
            "site": u"PingNi.com",
            "form": StudentForm() 
        }, context_instance=RequestContext(request))

    return render_to_response("person/view_profile.html", {
        "site": u"PingNi.com",
        "profileID": profileID,
    }, context_instance=RequestContext(request))

@login_required
def add_profile(request):
    """添加基本档案"""
    from staff.forms import AddStaffForm
    form = AddStaffForm()
    return render_to_response("school/add_staff.xhtml", {
        "site": u"PingNi.com",
        "form": form,
    }, context_instance=RequestContext(request))

from django.views.generic.create_update import create_object

@login_required
def new_person(request):
    """新增一个普通用户帐号"""
    from article.models import Article
    from article.forms import EditArticleForm
    return create_object(request, 
                         model=Article, 
                         form_class=EditArticleForm, 
                         template_name='base/form.html', 
                         extra_context={"form_title": Article.__doc__},
                         post_save_redirect="..")
    #return create_object(request, 
                         #model=Person, 
                         #form_class=EditSelfPersonForm,
                         #template_name='base/form.html', 
                         #extra_context={"form_title": Person.__doc__},
                         #post_save_redirect="..")
