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
#from student.models import StudentGraduate

REDIRECT_FIELD_NAME = 'next'

# Create your views here.

def index(request,profileID):
    """首页"""
    return render_to_response("profile/index.html", {
        "site": u"PingNi.com",
        "profileID": profileID,
    }, context_instance=RequestContext(request))

def view_profile(request, profileID):
    """查看某人的档案资料库"""
    context = request.GET.get("context", "index")
    return HttpResponse("OK")
    person = Person.objects.get(pk=profileID)
    if context == "Profile":
        return render_to_response("profile/view_other_profile.html", {
            "site": u"PingNi.com",
            "profileID": profileID,
            "profile": person,
        }, context_instance=RequestContext(request))
    elif person.identity == "School.Student":
        return HttpResponse("School.Student")
        return render_to_response("profile/view_other_student.html", {
            "site": u"PingNi.com",
            "profileID": profileID,
            "profile": person,
        }, context_instance=RequestContext(request))


    return render_to_response("profile/view_profile.html", {
        "site": u"PingNi.com",
        "profileID": profileID,
    }, context_instance=RequestContext(request))

def manage(request):
    """学校的管理模块"""
    return render_to_response("school/manage.html", {
        "site": u"搜索",
    }, context_instance=RequestContext(request))

def manage_student(request):
    """管理学生的基本信息模块"""
    p = request.REQUEST.get("p","")
    page = request.REQUEST.get("page", 1)

    person = request.user.person

    query = (Q(identity="School.Student") & \
            Q(identity_group=person.identity_group)) & \
            (Q(name__icontains=p) | \
            Q(id_no__icontains=p) | \
            Q(uuid__icontains=p) | \
            Q(spell_name__icontains=p))

    persons = Person.objects.filter(query)


    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for q in query_part:
        if not q.startswith("page="):
            new_query_parts.append(q)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(persons, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("school/manage_student.html", {
        "site": u"搜索",
        "persons": pages.cur_page.object_list,
        "pages":  pages,
        "p": p,
    }, context_instance=RequestContext(request))
    return HttpResponse("manage_student")

def student_experience(request, pk):
    """学生简历操作"""
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk) 
    if action == "view":
        return render_to_response("school/view_student_experience.html", {
            "site": u"PingNi.com",
            "person": person,
            "experience": person.student.studentexperience_set.all().order_by("-dtend", "-dtstart"),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse("StudentExperience" + str(pk) + action)

def student_keeper(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_student_keeper.html", {
            "site": "Pingni.com",
            "person": person,
            "keeper": person.student.studentkeeper_set.all(),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_family_member(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_student_family_member.html", {
            "site": "Pingni.com",
            "person": person,
            "family_member": person.student.studentfamilymember_set.all(),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_register(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_student_register.html", {
            "site": "Pingni.com",
            "person": person,
            "register": person.student.studentregister_set.all(),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_comment(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_student_comment.html", {
            "site": "Pingni.com",
            "person": person,
            "comment": person.student.studentcomment_set.all(),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_rewards(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_student_rewards.html", {
            "site": "Pingni.com",
            "person": person,
            "rewards": person.student.studentrewards_set.all().order_by("-date"),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_punishment(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_student_punishment.html", {
            "site": "Pingni.com",
            "person": person,
            "punishment": person.student.studentpunishment_set.all().order_by("-date"),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_enrollment(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)

    try:
        enrollment = person.student.studentenrollment
    except:
        enrollment = None
    
    if action == "view":
        return render_to_response("school/view_student_enrollment.html", {
            "site": "Pingni.com",
            "person": person,
            "enrollment": enrollment,
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_graduate(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        try:
            graduate = person.student.studentgraduate
        except:
            graduate = None
        return render_to_response("school/view_student_graduate.html", {
            "site": "Pingni.com",
            "person": person,
            "graduate": graduate,
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_finish_study(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        try:
            finish_study = person.student.studentfinishstudy
        except:
            finish_study = None
        return render_to_response("school/view_student_finish_study.html", {
            "site": "Pingni.com",
            "person": person,
            "finish_study": finish_study ,
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_transfer(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_student_transfer.html", {
            "site": "Pingni.com",
            "person": person,
            "transfer": person.student.studenttransfer_set.all().order_by("-date", "-pk"),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_assistance(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_student_assistance.html", {
            "site": "Pingni.com",
            "person": person,
            "assistance": person.student.studentassistance_set.all().order_by("-date", "-pk"),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def student_drill(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_student_drill.html", {
            "site": "Pingni.com",
            "person": person,
            "drill": person.student.studentdrill_set.all().order_by("-dtstart", "-pk"),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def manage_staff(request):
    """管理教职工的基本信息模块"""
    p = request.REQUEST.get("p","")
    page = request.REQUEST.get("page", 1)

    person = request.user.person

    query = (Q(identity="School.Staff") & 
            Q(identity_group=person.identity_group)) & \
            (Q(name__icontains=p) | \
            Q(id_no__icontains=p) | \
            Q(uuid__icontains=p) | \
            Q(spell_name__icontains=p))

    persons = Person.objects.filter(query)


    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for q in query_part:
        if not q.startswith("page="):
            new_query_parts.append(q)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(persons, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("school/manage_staff.html", {
        "site": u"搜索",
        "persons": pages.cur_page.object_list,
        "pages":  pages,
        "p": p,
    }, context_instance=RequestContext(request))
    return HttpResponse("manage_staff")

def staff_diploma(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_staff_diploma.html", {
            "site": "Pingni.com",
            "person": person,
            "diploma": person.staff.staffdiploma_set.all().order_by("-date_enrollment", "-pk"),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def staff_experience(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_staff_experience.html", {
            "site": "Pingni.com",
            "person": person,
            "experience": person.staff.staffexperience_set.all().order_by("-dtstart", "-pk"),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def staff_spouse(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)

    try:
        spouse = person.staff.staffspouse
    except:
        spouse = None
    
    if action == "view":
        return render_to_response("school/view_staff_spouse.html", {
            "site": "Pingni.com",
            "person": person,
            "spouse": spouse,
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def staff_other_family(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_staff_other_family.html", {
            "site": "Pingni.com",
            "person": person,
            "other_family": person.staff.staffotherfamily_set.all(),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def staff_teaching_workload(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_staff_teaching_workload.html", {
            "site": "Pingni.com",
            "person": person,
            "teaching_workload": person.staff.staffteachingworkload_set.all(),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)

def staff_teaching(request, pk):
    action = request.GET.get("action", "view")
    person = Person.objects.get(pk=pk)
    
    if action == "view":
        return render_to_response("school/view_staff_teaching.html", {
            "site": "Pingni.com",
            "person": person,
            "teaching": person.staff.staffteaching_set.all(),
        }, context_instance=RequestContext(request))
    else:
        return HttpResponse(pk)
