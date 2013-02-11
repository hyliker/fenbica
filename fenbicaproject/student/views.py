#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.cache import never_cache
from standard.models import LocationCode
from common.utils import dotdict
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from person.models import Person
from student.models import Student
from student.forms import MyStudentForm, EditStudentForm, AddStudentForm, EditSelfStudentForm
from django.contrib.auth.models import User
from django.contrib import messages
from utils.django_snippets import render_to, HttpResponseRedirectView
from student.models import Experience, Keeper, FamilyMember, Register, \
        Comment, Rewards, Punishment, Graduate,\
        FinishStudy, Transfer, Assistance, Drill
from student import forms
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from config.models import SystemSetting
from config.decorators import system_required

REDIRECT_FIELD_NAME = 'next'


@permission_required("student.student")
@render_to("student/details.html")
def student(request, student_pk=None, template=None):
    """查看某人的档案资料库"""
    student = get_object_or_404(Student, pk=student_pk)
    return {"person": student}, template

@permission_required("student.student_archive")
@render_to("student/student_archive.html")
def student_archive(request, student_pk=None, template=None):
    """查看学生的学籍卡"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.student_archive"): 
        return HttpResponseForbidden(u"无权限访问")

    def paddingItem(objects, length=5):
        """数据项不足的， 则补足到length项"""
        objects = [ m for m in objects ]
        minus_number = 5 - len(objects)
        for i in range(minus_number):
            objects.append(None)
        return objects
    family_member_list = paddingItem(student.familymember_set.all(), 5)
    experience_list = paddingItem(student.experience_set.all(), 4)

    try:
        school_name = SystemSetting.objects.get(key="SCHOOL_NAME").value
    except:
        school_name = ""

    return {
        "person": student, 
        "family_member_list": family_member_list,
        "experience_list": experience_list,
        "school_name": school_name,
    }, template

@permission_required("student.student_archive")
def student_archive_print(request, student_pk=None, template=None):
    """生成图片格式的学籍卡的打印稿"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.student_archive"): 
        return HttpResponseForbidden(u"无权限访问")

    def paddingItem(objects, length=5):
        objects = [ m for m in objects ]
        minus_number = 5 - len(objects)
        for i in range(minus_number):
            objects.append(None)
        return objects
    family_member_list = paddingItem(student.familymember_set.all(), 5)
    experience_list = paddingItem(student.experience_set.all(), 4)

    import Image
    import ImageDraw
    import ImageFont
    import cStringIO

    try:
        school_name = SystemSetting.objects.get(key="SCHOOL_NAME").value
    except:
        school_name = ""

    from settings import MEDIA_ROOT
    im = Image.open(MEDIA_ROOT + "img/school/student_archive.png")
    draw = ImageDraw.Draw(im)
    text = student.name
    font = ImageFont.truetype("/usr/share/fonts/apple/LiHeiPro.ttf", 40)


    def fmt_date(dt):
        if dt:
            fmtstr = u"%s年%s月%s日" % (dt.year, dt.month, dt.day)
        else:
            fmtstr = ""
        return fmtstr 

    draw_pos_mapping = [
        ((550, 520), school_name),
        ((1695, 520), u"%s" % student.date_joined.year),
        ((1852, 520), u"%s" % student.date_joined.month),
        ((1956, 520), u"%s" % student.date_joined.day),
        ((618, 687), u"%s" % student.id_no),
        ((600, 780), u"%s" % student.uuid),
        ((1822, 1082), u"%s" % student.telephone),
        ((582, 888), u"%s" % student.name),
        ((1020, 888), u"%s" % student.used_name),
        ((588, 981), u"%s" % student.gender.name),
        ((1035, 981), u"%s" % student.folk.name if student.folk else ""),
        ((1830, 993), u"%s" % student.health.name if student.health else ""),
        ((1830, 800), fmt_date(student.birthday)),
        ((576, 1275), u"%s" % student.residence_address),
        ((1836, 1278), u"%s" % student.postal_code),
        ((1832, 888), u"%s" % student.nationality.name if student.nationality else u"中国"),
        ((585, 1173), u"%s" % student.domicle_location),
        ((578, 2622), fmt_date(student.archive_cancel_date)),
        ((569, 2812), student.archive_administrator.name if student.archive_administrator else ""),
        ((1859, 2902), student.archive_approver.name if student.archive_approver else ""),
        ((565, 1070), str(student.dtrudui) if student.dtrudui else ""),
        ((1012, 1070), str(student.dtrutuan) if student.dtrutuan else ""),
    ]

    #adjust_archive_remark
    step = 50
    student_remark_parts = len(student.archive_remark[:90]) / 30
    for index in range(student_remark_parts):
        pos = (960, 2405+ index * step) 
        item = (pos, student.archive_remark[30 * index : 30 * (index+1)])
        draw_pos_mapping.append(item)
    
    #建卡原因
    if student.archive_create_reason == 1:
        #建卡原因，　新生入学
        draw_pos_mapping.append( ((1766, 700), u"√"))
    elif student.archive_create_reason == 2:
        #建卡原因，　转入
        draw_pos_mapping.append( ((2008, 700), u"√"))

    if student.archive_cancel_reason ==  1:
        draw_pos_mapping.append( ((1220, 2578), u"√"))
    elif student.archive_cancel_reason == 2:
        draw_pos_mapping.append( ((1660, 2578), u"√"))
    elif student.archive_cancel_reason == 3:
        draw_pos_mapping.append( ((1322, 2638), u"√"))
    elif student.archive_cancel_reason == 4:
        draw_pos_mapping.append( ((1938, 2638), u"√"))

    #增加家庭主要成绩条目
    step = 66
    for index, item in enumerate(student.familymember_set.all()):
        name  = (573, 1557 + index * step)
        relation = (780, 1557 + index * step)
        company = (1020, 1557 + index * step)
        telephone = (1838, 1557 + index * step) 
        fm_list = [
            (name, item.name),
            (relation, item.relation.name if item.relation else ""),
            (company, item.company),
            (telephone, item.telephone),
        ]
        draw_pos_mapping.extend(fm_list)

    #增加义务教育经历
    step = 92
    for index, item in enumerate(student.experience_set.all()):
        date = (578, 1990 + index * step)
        school = (1340, 1990 + index * step)
        attestor = (1834, 1990 + index * step) 
        xp_list = [
            (date, u"%s年%s月 至 %s年%s月" % (item.dtstart.year, item.dtstart.month, item.dtend.year, item.dtend.month)),
            (school, item.school_name),
            (attestor, item.attestor),
        ]
        draw_pos_mapping.extend(xp_list)

    for pos, info in draw_pos_mapping:
        draw.text(pos, info, font=font, fill=(0,0,0))

    buf = cStringIO.StringIO()    
    im.save(buf, 'png')    

    return HttpResponse(buf.getvalue(),'image/png') 
    #from common.utils import send_file
    #return send_file(buf, "KK.png")

@system_required("ALLOW_STUDENT_EDIT_PROFILE")
@login_required
@render_to("student/edit_student.html")
def edit_student(request, student_pk=None, template=None):
    """编辑我的基本信息"""
    student = get_object_or_404(Student, pk=student_pk)
    if request.method == "POST":
        if request.FILES.has_key("photo"):
            form = EditSelfStudentForm(request.POST, request.FILES, instance=student)
        else:
            form = EditSelfStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, u"嘿，你已经保存了你刚才编辑的个人基本信息")
            return HttpResponseRedirectView("student.views.student", student_pk=student_pk)
        else:
            messages.error(request, u"嘿，填写有错，请更正表单红色标记的错误后，再保存")
    else:
        form = EditSelfStudentForm(instance=student)
    return {"form": form}, template


@permission_required("student.add_student")
def add_student(request):
    """添加学生基本档案"""
    form = AddStudentForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data["name"]
        spell_name = form.cleaned_data.get("spell_name", None)
        print spell_name, bool(spell_name)
        if not spell_name:
            from tools import hzpy
            spell_name = hzpy.hz2py(name)
        try:
            max_samename_num = User.objects.filter(username__regex=r'^%s[0-9]+$' % spell_name).\
                    values_list("username", flat=True).order_by("-username")[0].split(spell_name)[-1]
        except IndexError,e:
            new_username = spell_name
        else:
            new_username_suffix = int(max_samename_num) + 1
            new_username =  "%s%d" % (spell_name, new_username_suffix)
        email = "%s@pingni.com" % new_username

        print "new_username", new_username
        print "spell_name", spell_name

        #TODO 创建之前，验证是不是录入同一个人了，通过身份证与编号惟一性来检验
        new_user = User.objects.create_user(new_username, email, password="dir")

        #同一个单位组织人可以添加本单位教职工情况
        _form = form.save(commit=False)
        _form.user = new_user
        _form.spell_name = spell_name
        _form.identity_group = request.user.person.identity_group
        _form.identity = "School.Student"
        _form.school = request.user.person.get_identity_group()
        _form.save()
        #save many-to-many
        form.save_m2m()

        print new_user
        print name, new_username
    return render_to_response("school/add_student.xhtml", {
        "form": form,
    }, context_instance=RequestContext(request))

@permission_required("student.delete_student")
def delete_student(request, student_pk):
    try:
        student = Student.objects.get(pk=student_pk)
        student.delete()
    except Exception,e:
        print e
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@permission_required("student.admin_student")
def admin_student(request):
    person = Person.objects.get(pk=request.user.pk)
    try:
        school = person.get_identity_group()
    except e:
        school = None
        print e

    filter = Q(school=school) & Q(identity="School.student")
    q = request.GET.get("q", "")
    if q:
        filter = filter & \
                 Q(name__icontains=q) |\
                 Q(spell_name__icontains=q) |\
                 Q(id_no__icontains=q) | \
                 Q(uuid__icontains=q) | \
                 Q(spell_name__icontains=q) |\
                 Q(user__username__icontains=q)
    students = Student.objects.filter(filter).order_by("-user__id")

    #搜索分页结合
    page = request.REQUEST.get("page", 1)
    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qs in query_part:
        if not qs.startswith("page="):
            new_query_parts.append(qs)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(students, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("school/admin_student.xhtml", {
        "students": pages.cur_page.object_list,
        "q": q,
        "pages":  pages,
    }, context_instance=RequestContext(request))


@login_required
@render_to("student/experience_list.html")
def experience_list(request, student_pk=None, template=None):
    """显示学生简历列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.experience_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        experience_list = get_list_or_404(Experience, student=student_pk)
    except:
        experience_list = None
    return {"person": student, "experience_list": experience_list}


@login_required
@render_to("student/experience.html")
def experience(request, pk=None, template=None):
    """学生简历条目"""
    experience = get_object_or_404(Experience, pk=pk)
    return {"experience": experience, "person": experience.student}, template

@login_required
@render_to("student/keeper_list.html")
def keeper_list(request, student_pk=None, template=None):
    """学生监护人列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.keeper_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        keeper_list = get_list_or_404(Keeper, student=student_pk)
    except:
        keeper_list = None
    return {"person": student, "keeper_list": keeper_list}, template

@login_required
@render_to("student/keeper.html")
def keeper(request, pk=None, template=None):
    """学生监护人条目"""
    keeper = get_object_or_404(Keeper, pk=pk)
    return {"keeper": keeper, "person": keeper.student}, template

@login_required
@render_to('student/family_member_list.html')
def family_member_list(request, student_pk=None, template=None):
    """学生家庭成员列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.family_member_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        family_member_list = get_list_or_404(FamilyMember, student=student_pk)
    except:
        family_member_list = None
    return {"person": student, "family_member_list": family_member_list}

@login_required
@render_to('student/family_member.html')
def family_member(request, pk=None, template=None):
    """学生家庭成员条目"""
    family_member = get_object_or_404(FamilyMember, pk=pk)
    return {"family_member": family_member, "person": family_member.student}, template

@login_required
@render_to('student/register_list.html')
def register_list(request, student_pk=None, template=None):
    """学生注册信息列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.register_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        register_list = get_list_or_404(Register, student=student_pk)
    except:
        register_list = None
    return {"person": student, "register_list": register_list}


@login_required
@render_to('student/register.html')
def register(request, pk=None, template=None):
    """学生注册信息条目"""
    register = get_object_or_404(Register, pk=pk)
    return {"register": register, "person": register.student}, template

@login_required
@render_to('student/comment_list.html')
def comment_list(request, student_pk=None, template=None):
    """学生考评信息列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.comment_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        comment_list = get_list_or_404(Comment, student=student_pk)
    except:
        comment_list = None
    return {"person": student, "comment_list": comment_list}

@login_required
@render_to('student/comment.html')
def comment(request, pk=None, template=None):
    """学生考评信息条目"""
    comment = get_object_or_404(Comment, pk=pk)
    return {"comment": comment, "person": comment.student}, template

@login_required
@render_to('student/rewards_list.html')
def rewards_list(request, student_pk=None, template=None):
    """学生奖励信息列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.rewards_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        rewards_list = get_list_or_404(Rewards, student=student_pk)
    except:
        rewards_list = None
    return {"person": student, "rewards_list": rewards_list}

@login_required
@render_to('student/rewards.html')
def rewards(request, pk=None, template=None):
    """学生奖励信息条目"""
    rewards = get_object_or_404(Rewards, pk=pk)
    return {"rewards": rewards, "person": rewards.student}, template

@login_required
@render_to('student/punishment_list.html')
def punishment_list(request, student_pk=None, template=None):
    """学生处分信息列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.punishment_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        punishment_list = get_list_or_404(Punishment, student=student_pk)
    except:
        punishment_list = None
    return {"person": student, "punishment_list": punishment_list}

@login_required
@render_to('student/punishment.html')
def punishment(request, pk=None, template=None):
    """学生处分信息条目"""
    punishment = get_object_or_404(Punishment, pk=pk)
    return {"punishment": punishment, "person": punishment.student}, template

#@render_to('student/enrollment_list.html')
#def enrollment_list(request, student_pk=None, template=None):
    #student = get_object_or_404(Student, pk=student_pk)
    #try:
        #enrollment_list = get_list_or_404(Enrollment, student=student_pk)
    #except:
        #enrollment_list = None
    #return {"person": student, "enrollment_list": enrollment_list}

#@render_to('student/enrollment.html')
#def enrollment(request, pk=None, template=None):
    #enrollment = get_object_or_404(Enrollment, pk=pk)
    #return {"enrollment": enrollment, "person": enrollment.student}, template

@login_required
@render_to('student/graduate_list.html')
def graduate_list(request, student_pk=None, template=None):
    """学生毕业信息列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.graduate_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        graduate_list = get_list_or_404(Graduate, student=student_pk)
    except:
        graduate_list = None
    return {"person": student, "graduate_list": graduate_list}

@login_required
@render_to('student/graduate.html')
def graduate(request, pk=None, template=None):
    """学生毕业信息条目"""
    graduate = get_object_or_404(Graduate, pk=pk)
    return {"graduate": graduate, "person": graduate.student}, template

@login_required
@render_to('student/finish_study_list.html')
def finish_study_list(request, student_pk=None, template=None):
    """学生结业信息列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.finish_study_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        finish_study_list = get_list_or_404(FinishStudy, student=student_pk)
    except:
        finish_study_list = None
    return {"person": student, "finish_study_list": finish_study_list}

@login_required
@render_to('student/finish_study.html')
def finish_study(request, pk=None, template=None):
    """学生结业信息条目"""
    finish_study = get_object_or_404(FinishStudy, pk=pk)
    return {"finish_study": finish_study, "person": finish_study.student}, template

@login_required
@render_to('student/transfer_list.html')
def transfer_list(request, student_pk=None, template=None):
    """学生学籍异动信息列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.transfer_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        transfer_list = get_list_or_404(Transfer, student=student_pk)
    except:
        transfer_list = None
    return {"person": student, "transfer_list": transfer_list}

@login_required
@render_to('student/transfer.html')
def transfer(request, pk=None, template=None):
    """学生学籍异动信息条目"""
    transfer = get_object_or_404(Transfer, pk=pk)
    return {"transfer": transfer, "person": transfer.student}, template

@login_required
@render_to('student/assistance_list.html')
def assistance_list(request, student_pk=None, template=None):
    """学生贫困補助信息列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.assistance_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        assistance_list = get_list_or_404(Assistance, student=student_pk)
    except:
        assistance_list = None
    return {"person": student, "assistance_list": assistance_list}

@login_required
@render_to('student/assistance.html')
def assistance(request, pk=None, template=None):
    """学生贫困補助信息条目"""
    assistance = get_object_or_404(Assistance, pk=pk)
    return {"assistance": assistance, "person": assistance.student}, template

@login_required
@render_to('student/drill_list.html')
def drill_list(request, student_pk=None, template=None):
    """学生军训信息列表"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.drill_list"):
        return HttpResponseForbidden(u"无权限")
    try:
        drill_list = get_list_or_404(Drill, student=student_pk)
    except:
        drill_list = None
    return {"person": student, "drill_list": drill_list}

@login_required
@render_to('student/drill.html')
def drill(request, pk=None, template=None):
    """学生军训信息条目"""
    drill = get_object_or_404(Drill, pk=pk)
    return {"drill": drill, "person": drill.student}, template


@login_required
@render_to("student/exam_result_list.html")
def exam_result_list(request, student_pk=None, template=None):
    """查看某个人的考试信息"""
    from exam.models import Result, Exam
    from exam import misc

    person = get_object_or_404(Person, pk=student_pk)
    if person.pk != request.user.pk and not request.user.has_perm("student.exam_result_list"):
        return HttpResponseForbidden(u"无权限")

    exam_pk = request.GET.get("exam_pk", None)
    if exam_pk is None:
        #如果没有指定， 则显示最近参加的一次考试
        try:
            latest_result = Result.objects.filter(student=person).select_related("subject", "subject__exam").latest("subject__exam__dtstart")
        except Result.DoesNotExist,e:
            exam = None
        else:
            exam = latest_result.subject.exam
    else:
        exam = get_object_or_404(Exam, pk=exam_pk)

    result_list = Result.objects.filter(student=person, subject__exam=exam)

    exam_pk_list = Result.objects.filter(student=person).values_list("subject__exam", flat=True).annotate()
    exam_list = Exam.objects.filter(pk__in=exam_pk_list)

    try:
        r = result_list[0]
        #print dir(r), type(r), r.class_ranking
    except IndexError, e:
        return {
            "result_list": result_list,
            "exam_list": exam_list,
            "exam": exam,
            "person": person,
        }, template


    def sum_score(result_list):
        """计算总分项"""
        total = {}
        score = sum([r.score for r in result_list if r.score is not None])
        full_score = sum([r.subject.full_score for r in result_list])

        class_sum_score_ranking = misc.class_sum_score_ranking(exam, result_list[0].klass.pk)
        grade_sum_score_ranking = misc.grade_sum_score_ranking(exam, result_list[0].klass.grade)
        #assert False, result_list
        #assert False, grade_sum_score_ranking

        level = misc.calc_score_level(full_score, score)
        total = {
            "score": score,
            "full_score": full_score,
            "level": level,
            "class_ranking": class_sum_score_ranking[person.pk].ranking,
            "grade_ranking": grade_sum_score_ranking[person.pk],
        }
        setattr(result_list, "total", total)
    sum_score(result_list)

    print result_list

    return {
        "result_list": result_list,
        "exam_list": exam_list,
        "exam": exam,
        "person": person,
    }, template

@login_required
@render_to("student/exam_result_analyse.html")
def exam_result_analyse(request, student_pk, template=None):
    """某个学生的考试成绩汇总分析"""
    person = get_object_or_404(Person, pk=student_pk)
    if person.pk != request.user.pk and not request.user.has_perm("student.exam_result_analyse"):
        return HttpResponseForbidden(u"无权限")

    return {
        "person": person,
    }, template

@system_required("ALLOW_STUDENT_EDIT_PROFILE")
@login_required
@render_to("student/edit_experience.html")
def edit_experience(request, pk=None, template=None):
    u"""编辑自己的简历"""
    if pk:
        experience = get_object_or_404(Experience, pk=pk)
        if experience.student_id != request.user.pk:
            return HttpResponseForbidden(u"你没有权限编辑别人的简历")
    else:
        experience = Experience(student=request.user.person.student)

    form = forms.EditExperienceForm(request.POST or None, instance=experience)
    if form.is_valid():
        new_experience = form.save()
        redirect_url = reverse("student_experience_list", args=[new_experience.student_id])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@system_required("ALLOW_STUDENT_EDIT_PROFILE")
@login_required
@render_to("student/edit_keeper.html")
def edit_keeper(request, pk=None, template=None):
    if pk:
        keeper = get_object_or_404(Keeper, pk=pk)
        if keeper.student_id != request.user.pk:
            return HttpResponseForbidden(u"你没有权限编辑别人的简历")
    else:
        keeper = Keeper(student=request.user.person.student)

    form = forms.EditKeeperForm(request.POST or None, instance=keeper)
    if form.is_valid():
        new_keeper = form.save()
        redirect_url = reverse("student_keeper_list", args=[new_keeper.student_id])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@system_required("ALLOW_STUDENT_EDIT_PROFILE")
@login_required
@render_to("student/edit_family_member.html")
def edit_family_member(request, pk=None, template=None):
    if pk:
        family_member = get_object_or_404(FamilyMember, pk=pk)
        if family_member.student_id != request.user.pk:
            return HttpResponseForbidden(u"你没有权限编辑别人的简历")
    else:
        family_member = FamilyMember(student=request.user.person.student)

    form = forms.EditFamilyMemberForm(request.POST or None, instance=family_member)
    if form.is_valid():
        new_family_member = form.save()
        redirect_url = reverse("student_family_member_list", args=[new_family_member.student_id])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@system_required("ALLOW_STUDENT_EDIT_PROFILE")
@login_required
def delete_experience(request, pk=None):
    """删除简历条目"""
    experience = get_object_or_404(Experience, pk=pk)
    if experience.student_id == request.user.pk:
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

@system_required("ALLOW_STUDENT_EDIT_PROFILE")
@login_required
def delete_keeper(request, pk=None):
    """删除简历条目"""
    keeper = get_object_or_404(Keeper, pk=pk)
    if keeper.student_id == request.user.pk:
        keeper.delete()
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

@system_required("ALLOW_STUDENT_EDIT_PROFILE")
@login_required
def delete_family_member(request, pk=None):
    """删除简历条目"""
    family_member = get_object_or_404(FamilyMember, pk=pk)
    if family_member.student_id == request.user.pk:
        family_member.delete()
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
@render_to("student/classmate_list.html")
def classmate_list(request, student_pk):
    """学生就读班级记录"""
    student = get_object_or_404(Student, pk=student_pk)
    if student.pk != request.user.pk and not request.user.has_perm("student.classmate_list"):
        return HttpResponseForbidden(u"无权限")

    classmate_list = student.classmate_set.all()
    return {"person": student, "classmate_list": classmate_list}
