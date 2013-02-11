#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.cache import never_cache
from standard.models import LocationCode
from common.utils import dotdict
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from person.models import Person
from staff.models import Staff, Experience, Diploma, Spouse, Family, Workload, Teaching
from staff.forms import MyStaffForm, EditStaffForm, EditSelfStaffForm
from django.contrib.auth.models import User
from utils.django_snippets import render_to, HttpResponseRedirectView
from staff import forms
from config.decorators import system_required

from django.contrib.auth.decorators import login_required, permission_required

REDIRECT_FIELD_NAME = 'next'

@login_required
@render_to("staff/details.html")
def staff(request, staff_pk=None, template=None):
    """查看某人的档案资料库"""
    staff = get_object_or_404(Staff, pk=staff_pk)
    return {"person": staff}, template


@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
@render_to("staff/edit_staff.html")
def edit_staff(request, staff_pk=None, template=None):
    """编辑我的基本信息"""
    staff = get_object_or_404(Staff, pk=staff_pk)
    if request.method == "POST":
        if request.FILES.has_key("photo"):
            form = EditSelfStaffForm(request.POST, request.FILES, instance=staff)
        else:
            form = EditSelfStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, u"嘿，你已经保存了你刚才编辑的个人基本信息")
            return HttpResponseRedirectView("staff.views.staff", staff_pk=staff_pk)
        else:
            messages.error(request, u"嘿，填写有错，请更正表单红色标记的错误后，再保存")
    else:
        form = EditSelfStaffForm(instance=staff)
    return {"form": form}, template

@permission_required("staff.add_staff")
def add_staff(request):
    """添加基本档案"""
    from staff.forms import AddStaffForm
    form = AddStaffForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data["name"]
        from tools import hzpy
        username = hzpy.hz2py(name)
        #same_username_list = User.objects.filter(username__startswith=username).values_list("username", flat=True)
        #new_number_suffix = 2
        #for n in same_username_list:
            #name_suffix = n.split(username)[-1]
            #if name_suffix.isdigit() and int(name_suffix) >= new_number_suffix:
                #new_number_suffix = int(name_suffix) + 1
        try:
            max_samename_num = User.objects.filter(username__regex=r'^%s[0-9]+$' % username).\
                    values_list("username", flat=True).order_by("-username")[0].split(username)[-1]
        except IndexError,e:
            new_username_suffix = 2
        else:
            new_username_suffix = int(max_samename_num) + 1

        new_username =  "%s%d" % (username, new_username_suffix)
        email = "%s@pingni.com" % new_username
        #TODO 创建之前，验证是不是录入同一个人了，通过身份证与编号惟一性来检验
        new_user = User.objects.create_user(new_username, email, password="dir")

        #同一个单位组织人可以添加本单位教职工情况
        _form = form.save(commit=False)
        _form.user = new_user
        _form.identity_group = request.user.person.identity_group
        _form.identity = "School.Staff"
        _form.school = request.user.person.get_identity_group()
        _form.save()

        print new_user
        print name, new_username
        #_form = form.save(commit=False)
    return render_to_response("school/add_staff.xhtml", {
        "form": form,
    }, context_instance=RequestContext(request))

@permission_required("staff.admin_staff")
def admin_staff(request):
    person = Person.objects.get(pk=request.user.pk)
    try:
        school = person.get_identity_group()
    except e:
        school = None
        print e

    filter = Q(school=school) & Q(identity="School.Staff")
    q = request.GET.get("q", "")
    if q:
        filter = filter & \
                 Q(name__icontains=q) |\
                 Q(spell_name__icontains=q) |\
                 Q(id_no__icontains=q) | \
                 Q(uuid__icontains=q) | \
                 Q(spell_name__icontains=q) |\
                 Q(user__username__icontains=q)
    staffs = Staff.objects.filter(filter)

    #搜索分页结合
    page = request.REQUEST.get("page", 1)
    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qs in query_part:
        if not qs.startswith("page="):
            new_query_parts.append(qs)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(staffs, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("school/admin_staff.xhtml", {
        "staffs": pages.cur_page.object_list,
        "q": q,
        "pages":  pages,
    }, context_instance=RequestContext(request))

#def edit_staff(request, staff_pk):
    #"""编辑某人基本信息"""

    #try:
        #staff = Staff.objects.get(pk=staff_pk)
    #except:
        #staff = None
    #form = EditStaffForm(request.POST or None, instance=staff)
    #if form.is_valid():
        #form.save()
        #form.success = True
        ##return HttpResponse("form saved")
        ##return HttpResponseRedirect("/")
    #return render_to_response("school/edit_staff.xhtml", {
        #"site": u"PingNi.com",
        #"form": form,
    #}, context_instance=RequestContext(request))

@permission_required("staff.delete_staff")
def delete_staff(request, staff_pk):
    try:
        staff = Staff.objects.get(pk=staff_pk)
        staff.delete()
    except Exception,e:
        print e
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@login_required
@render_to('staff/experience_list.html')
def experience_list(request, staff_pk=None, template=None):
    staff = get_object_or_404(Staff, pk=staff_pk)
    if staff.pk != request.user.pk and not request.user.has_perm("staff.experience_list"):
        return HttpResponseForbidden(u"没权限访问")

    try:
        experience_list = get_list_or_404(Experience, staff=staff_pk)
    except:
        experience_list = None
    return {"person": staff, "experience_list": experience_list}

@login_required
@render_to('staff/experience.html')
def experience(request, pk=None, template=None):
    experience = get_object_or_404(Experience, pk=pk)
    if experience.staff.pk != request.user.pk and not request.user.has_perm("staff.experience_list"):
        return HttpResponseForbidden(u"没权限访问")
    return {"experience": experience, "person": experience.staff}, template

@login_required
@render_to('staff/diploma_list.html')
def diploma_list(request, staff_pk=None, template=None):
    staff = get_object_or_404(Staff, pk=staff_pk)
    if staff.pk != request.user.pk and not request.user.has_perm("staff.diploma_list"):
        return HttpResponseForbidden(u"没权限访问")

    try:
        diploma_list = get_list_or_404(Diploma, staff=staff_pk)
    except:
        diploma_list = None
    return {"person": staff, "diploma_list": diploma_list}

@login_required
@render_to('staff/diploma.html')
def diploma(request, pk=None, template=None):
    diploma = get_object_or_404(Diploma, pk=pk)
    if diploma.staff.pk != request.user.pk and not request.user.has_perm("staff.diploma"):
        return HttpResponseForbidden(u"没权限访问")
    return {"diploma": diploma, "person": diploma.staff}, template

@login_required
@render_to('staff/spouse.html')
def spouse(request, staff_pk=None, template=None):
    staff = get_object_or_404(Staff, pk=staff_pk)
    if staff.pk != request.user.pk and not request.user.has_perm("staff.experience"):
        return HttpResponseForbidden(u"没权限访问")

    spouse, created = Spouse.objects.get_or_create(pk=staff_pk)
    return {"spouse": spouse, "person": staff}, template

@login_required
@render_to('staff/family_list.html')
def family_list(request, staff_pk=None, template=None):
    staff = get_object_or_404(Staff, pk=staff_pk)
    if staff.pk != request.user.pk and not request.user.has_perm("staff.family_list"):
        return HttpResponseForbidden(u"没权限访问")
    try:
        family_list = get_list_or_404(Family, staff=staff_pk)
    except:
        family_list = None
    return {"person": staff, "family_list": family_list}

@login_required
@render_to('staff/family.html')
def family(request, pk=None, template=None):
    family = get_object_or_404(Family, pk=pk)
    if family.staff.pk != request.user.pk and not request.user.has_perm("staff.family"):
        return HttpResponseForbidden(u"没权限访问")
    return {"family": family, "person": family.staff}, template

@login_required
@render_to('staff/workload_list.html')
def workload_list(request, staff_pk=None, template=None):
    staff = get_object_or_404(Staff, pk=staff_pk)
    if staff.pk != request.user.pk and not request.user.has_perm("staff.workload_list"):
        return HttpResponseForbidden(u"没权限访问")
    try:
        workload_list = get_list_or_404(Workload, staff=staff_pk)
    except:
        workload_list = None
    return {"person": staff, "workload_list": workload_list}

@login_required
@render_to('staff/workload.html')
def workload(request, pk=None, template=None):
    workload = get_object_or_404(Workload, pk=pk)
    if workload.staff.pk != request.user.pk and not request.user.has_perm("staff.workload"):
        return HttpResponseForbidden(u"没权限访问")
    return {"workload": workload, "person": workload.staff}, template

@login_required
@render_to('staff/teaching_list.html')
def teaching_list(request, staff_pk=None, template=None):
    staff = get_object_or_404(Staff, pk=staff_pk)
    if staff.pk != request.user.pk and not request.user.has_perm("staff.teaching_list"):
        return HttpResponseForbidden(u"没权限访问")
    try:
        teaching_list = get_list_or_404(Teaching, staff=staff_pk)
    except:
        teaching_list = None
    return {"person": staff, "teaching_list": teaching_list}

@login_required
@render_to('staff/teaching.html')
def teaching(request, pk=None, template=None):
    teaching = get_object_or_404(Teaching, pk=pk)
    if teaching.staff.pk != request.user.pk and not request.user.has_perm("staff.teaching"):
        return HttpResponseForbidden(u"没权限访问")
    return {"teaching": teaching, "person": teaching.staff}, template

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
@render_to("staff/edit_experience.html")
def edit_experience(request, pk=None, template=None):
    if pk:
        experience = get_object_or_404(Experience, pk=pk)
        if experience.staff_id != request.user.pk:
            return HttpResponseForbidden(u"你没有权限编辑别人的简历")
    else:
        experience = Experience(staff=request.user.person.staff)

    form = forms.EditExperienceForm(request.POST or None, instance=experience)
    if form.is_valid():
        new_experience = form.save()
        redirect_url = reverse("staff_experience_list", args=[new_experience.staff_id])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
@render_to("staff/edit_diploma.html")
def edit_diploma(request, pk=None, template=None):
    if pk:
        diploma = get_object_or_404(Diploma, pk=pk)
        if diploma.staff_id != request.user.pk:
            return HttpResponseForbidden(u"你没有权限编辑别人的简历")
    else:
        diploma = Diploma(staff=request.user.person.staff)

    form = forms.EditDiplomaForm(request.POST or None, instance=diploma)
    if form.is_valid():
        new_diploma = form.save()
        redirect_url = reverse("staff_diploma_list", args=[new_diploma.staff_id])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
@render_to("staff/edit_spouse.html")
def edit_spouse(request, pk=None, template=None):
    if pk:
        spouse, created = Spouse.objects.get_or_create(pk=pk)
        if spouse.staff_id != request.user.pk:
            return HttpResponseForbidden(u"你没有权限编辑别人的简历")
    else:
        spouse = Spouse(staff=request.user.person.staff)

    form = forms.EditSpouseForm(request.POST or None, instance=spouse)
    if form.is_valid():
        new_spouse = form.save()
        redirect_url = reverse("staff_spouse", args=[new_spouse.staff_id])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
@render_to("staff/edit_family.html")
def edit_family(request, pk=None, template=None):
    if pk:
        family = get_object_or_404(Family, pk=pk)
        if family.staff_id != request.user.pk:
            return HttpResponseForbidden(u"你没有权限编辑别人的简历")
    else:
        family = Family(staff=request.user.person.staff)

    form = forms.EditFamilyForm(request.POST or None, instance=family)
    if form.is_valid():
        new_family = form.save()
        redirect_url = reverse("staff_family_list", args=[new_family.staff_id])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
@render_to("staff/edit_workload.html")
def edit_workload(request, pk=None, template=None):
    if pk:
        workload = get_object_or_404(Workload, pk=pk)
        if workload.staff_id != request.user.pk:
            return HttpResponseForbidden(u"你没有权限编辑别人的简历")
    else:
        workload = Workload(staff=request.user.person.staff)

    form = forms.EditWorkloadForm(request.POST or None, instance=workload)
    if form.is_valid():
        new_workload = form.save()
        redirect_url = reverse("staff_workload_list", args=[new_workload.staff_id])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
@render_to("staff/edit_teaching.html")
def edit_teaching(request, pk=None, template=None):
    if pk:
        teaching = get_object_or_404(Teaching, pk=pk)
        if teaching.staff_id != request.user.pk:
            return HttpResponseForbidden(u"你没有权限编辑别人的简历")
    else:
        teaching = Teaching(staff=request.user.person.staff)

    form = forms.EditTeachingForm(request.POST or None, instance=teaching)
    if form.is_valid():
        new_teaching = form.save()
        redirect_url = reverse("staff_teaching_list", args=[new_teaching.staff_id])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
def delete_experience(request, pk=None):
    """删除简历条目"""
    experience = get_object_or_404(Experience, pk=pk)
    if experience.staff_id == request.user.pk:
        experience.delete()
        deleted = True
    else:
        deleted = False

    if request.is_ajax():
        json_res = json.dumps({
            "success": deleted,
            "data": pk,
        })
        return HttpResponse(json_res)
    else:
        redirect_url = request.META.get("HTTP_REFERER", "/")
        return HttpResponseRedirect(redirect_url)

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
def delete_diploma(request, pk=None):
    """删除简历条目"""
    diploma = get_object_or_404(Diploma, pk=pk)
    if diploma.staff_id == request.user.pk:
        diploma.delete()
        deleted = True
    else:
        deleted = False

    if request.is_ajax():
        json_res = json.dumps({
            "success": deleted,
            "data": pk,
        })
        return HttpResponse(json_res)
    else:
        redirect_url = request.META.get("HTTP_REFERER", "/")
        return HttpResponseRedirect(redirect_url)

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
def delete_family(request, pk=None):
    """删除其他家人条目"""
    family = get_object_or_404(Family, pk=pk)
    if family.staff_id == request.user.pk:
        family.delete()
        deleted = True
    else:
        deleted = False

    if request.is_ajax():
        json_res = json.dumps({
            "success": deleted,
            "data": pk,
        })
        return HttpResponse(json_res)
    else:
        redirect_url = request.META.get("HTTP_REFERER", "/")
        return HttpResponseRedirect(redirect_url)

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
def delete_workload(request, pk=None):
    """删除教学工作量条目"""
    workload = get_object_or_404(Workload, pk=pk)
    if workload.staff_id == request.user.pk:
        workload.delete()
        deleted = True
    else:
        deleted = False

    if request.is_ajax():
        json_res = json.dumps({
            "success": deleted,
            "data": pk,
        })
        return HttpResponse(json_res)
    else:
        redirect_url = request.META.get("HTTP_REFERER", "/")
        return HttpResponseRedirect(redirect_url)

@system_required("ALLOW_STAFF_EDIT_PROFILE")
@login_required
def delete_teaching(request, pk=None):
    """删除任课条目"""
    teaching = get_object_or_404(Teaching, pk=pk)
    if teaching.staff_id == request.user.pk:
        teaching.delete()
        deleted = True
    else:
        deleted = False

    if request.is_ajax():
        json_res = json.dumps({
            "success": deleted,
            "data": pk,
        })
        return HttpResponse(json_res)
    else:
        redirect_url = request.META.get("HTTP_REFERER", "/")
        return HttpResponseRedirect(redirect_url)


@login_required
@render_to("staff/course_list.html")
def course_list(request, staff_pk, template=None):
    """开设课程"""
    staff = get_object_or_404(Staff, pk=staff_pk)
    course_list = staff.course_set.all()
    return {"person": staff, "course_list": course_list}, template

@login_required
@render_to("staff/course_classgrade_list.html")
def course_classgrade_list(request, staff_pk, template=None):
    """班级课程"""
    staff = get_object_or_404(Staff, pk=staff_pk)
    course_list = staff.course_set.all()
    return {"person": staff, "course_list": course_list}, template
