#coding: utf-8
import operator
import json
import datetime
from collections import defaultdict
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from person.models import Person
from exam.forms import ExamForm, SubjectForm, EditExamForm, AddExamForm, AddSubjectForm
from django.db.models import get_model
from django.core.paginator import Paginator
from student.models import Student
from exam.models import Subject, Exam, Result
from classgrade.models import Class
from decimal import Decimal
from pyExcelerator import parse_xls
from django.db import IntegrityError
from standard.models import GradeCode
from exam import misc
from django.db.models import Sum, Avg, Count, StdDev, Max, Min, Q
from django.core.urlresolvers import reverse
from utils.django_snippets import render_to, HttpResponseRedirectView
from django.db.models import Count
from classgrade.models import Classmate 
from exam.models import *
from standard.models import *
from django.contrib.auth.decorators import permission_required, login_required

# Create your views here.

@login_required
def exam_index(request):
    return HttpResponseRedirect(reverse("exam_subject_list"))
    #exams = Exam.objects.all()
    #return render_to_response("school/exam_index.xhtml", {
        #"site": u"PingNi.com",
        #"exams": exams,
    #}, context_instance=RequestContext(request))

@login_required
def add_studentexam_by_school(request):
    """由学校来增加学生在校考试信息"""
    person = Person.objects.get(pk=request.user.pk)

    form = AddExamForm(request.POST or None)
    if form.is_valid():
        _form = form.save(commit=False)
        _form.school = request.user.person.get_identity_group()
        _form.save()
        form.success = True

    return render_to_response("school/add_studentexam.xhtml", {
        "site": u"PingNi.com",
        "form": form,
    }, context_instance=RequestContext(request))

@login_required
def add_studentexamresult_by_myself(request):
    """由学生自己来提交成绩結果"""
    pass

@login_required
def add_studentexam_by_bureau(request):
    """由教育局来增加学生考试信息，如由县发起的考试"""
    return HttpResponse("add_student_exam_by_bureau")

@login_required
def view_studentexam_by_school(request):
    """列出考试信息列表"""
    return HttpResponse("view_studentexam_by_school")

@permission_required("exam.view_studentexamresult")
@login_required
def view_studentexamresult(request, profileID):
    """查看某个人的考试信息"""
    #person = Person.objects.get(pk=request.user.pk)
    person = Person.objects.get(pk=profileID)
    try:
        exam_result = Result.objects.filter(student=person)
        exams_annotate = exam_result.values("subject__exam", "subject__grade").annotate()
        exam_pks = [e["subject__exam"] for e in exams_annotate]
        exams = Exam.objects.filter(pk__in=exam_pks)
        exam_grade_mapping = dict([(m["subject__exam"], m["subject__grade"]) for m in exams_annotate])
        print exam_grade_mapping
    except:
        exam_result = None
    for exam in exams:
        exam_subjects = exam.subject_set.filter(grade=exam_grade_mapping[exam.pk])
        sum_score = 0
        for subject in exam_subjects:
            try:
                c_result = subject.result_set.filter(student=person)[0]
                sum_score = c_result.score + sum_score
            except:
                c_result = None
            setattr(subject, "result", c_result)
        setattr(exam, "exam_subjects", exam_subjects )
        exam_grade = exam_subjects[0].grade
        setattr(exam, "grade", exam_grade)
        setattr(exam, "sum_score", sum_score)
    #exams = [exams[0], exams[0]]
    #print exam_result
    return render_to_response("exam/view_student_exam_result.xhtml", {
        "site": u"PingNi.com",
        "person": person,
        "exams": exams,
        "exam_result": exam_result,
    }, context_instance=RequestContext(request))

@permission_required("exam.add_result")
@csrf_exempt
@render_to("exam/add_result.html")
def add_result(request, template=None):
    """批量增加学生某一科目的成绩"""
    if request.method == "GET":
        exams = Exam.objects.all()
        try:
            current_exam = exams[0]
            exam_subjects = current_exam.subject_set.all()
            exam_classes = Class.objects.filter(dtcreated__year=current_exam.learning_year[:4])
        except:
            return HttpResponse("unready")

    elif request.method == "POST":
        exam_subject_pk = request.POST.get("exam_subject_pk", None)
        klass_pk = request.POST.get("klass_pk", None)
        #print request.POST
        for k in request.POST:
            if k.startswith("student_pk_"):
                student_pk = k.rsplit("_")[-1]
                try:
                    score = Decimal(request.POST.get(k))
                except Exception, e:
                    score = None
                try:
                    result = Result.objects.get(student=student_pk, subject = exam_subject_pk)
                    result.score = score
                except Exception, e:
                    try:
                        result = Result(
                            student_id = student_pk,
                            klass_id = klass_pk,
                            subject_id = exam_subject_pk,
                            score = score,
                            level = None,
                            creator = request.person,
                        )
                        result.save()
                    except Exception, e:
                        print "Exception", e
                result.save()
        res = {
            "success": True,
        }
        return HttpResponse(json.dumps(res))

    return {
        "exams": exams,
        "exam_subjects": exam_subjects,
        "exam_classes": exam_classes,
    }, template

@permission_required("exam.add_studentexamresult_by_class_step1")
def add_studentexamresult_by_class_step1(request):
    """按班级录入学生考试成绩結果,第一步"""
    from exam.models import Subject
    exams = Exam.objects.all()
    from account.models import Person
    person = Person.objects.get(pk=request.user.pk)
    if person.identity == "School.Student":
        school = person.student.school
    elif person.identity == "School.Staff":
        school = person.staff.school

    exam_subjects = Subject.objects.filter(exam__school=school)

    p = request.REQUEST.get("p","")
    page = request.REQUEST.get("page", 1)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for q in query_part:
        if not q.startswith("page="):
            new_query_parts.append(q)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(exam_subjects, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("school/add_student_exam_result_by_class_step1.xhtml", {
        "site": u"PingNi.com",
        "pages":  pages,
        "exams": exams,
        "exam_subjects": pages.cur_page.object_list,
        "exam_subjects": exam_subjects,
    }, context_instance=RequestContext(request))

@permission_required("exam.add_studentexamresult_by_class_step2")
def add_studentexamresult_by_class_step2(request, exam_subject_pk):
    """第二步， 选择班级"""

    exam_subject = Subject.objects.get(pk=exam_subject_pk)
    classes = Class.objects.filter(grade=exam_subject.grade)

    p = request.REQUEST.get("p","")
    page = request.REQUEST.get("page", 1)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for q in query_part:
        if not q.startswith("page="):
            new_query_parts.append(q)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(classes, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("school/add_student_exam_result_by_class_step2.xhtml", {
        "site": u"PingNi.com",
        "pages":  pages,
        "classes": pages.cur_page.object_list,
        "exam_subject": exam_subject,
    }, context_instance=RequestContext(request))

@permission_required("exam.export_studentexamresult_by_class")
def export_studentexamresult_by_class(request, exam_subject_pk, class_pk):
    """导出exam_subject_pk这次考试，class_pk这个班的成绩录入表格"""
    exam_subject = Subject.objects.get(pk=exam_subject_pk)
    klass = Class.objects.get(pk=class_pk)
    students = klass.classmate_set.all()

    student_results = Result.objects.filter(subject=exam_subject_pk, student__in=students.values_list("student_id", flat=True)).values_list("student", "score")
    student_results_dict = dict(student_results)

    from pyExcelerator import Workbook, Font, XFStyle, Alignment
    wb = Workbook()
    ws = wb.add_sheet(u"考试成绩录入")
    t_font, al, t_style, style = Font(), Alignment(), XFStyle(), XFStyle()
    t_font.bold = True
    t_font.height = 18*0x14
    t_style.font = t_font
    al.horz = Alignment.HORZ_CENTER
    style.alignment = al

    ws.write(0, 0, u"考试课程编号")
    ws.write(0, 1, exam_subject.pk)
    title = u"%(learning_year_verbose_name)s %(semester)s %(grade)s %(subject)s " \
            % {"learning_year_verbose_name": exam_subject.exam.learning_year_verbose_name,
               "semester": exam_subject.exam.semester,
               "grade": exam_subject.grade,
               "subject": exam_subject.category.name}
    ws.write_merge(1, 1, 0, 3, title, t_style)
    ws.write_merge(2, 2, 0, 3, u"备注：上面的标题不要改动，否则无法正确导入成绩到系统中，请按以下格式录入成绩")
    for k, v in enumerate([u"班别", u"班学号", u"姓名", u"分数成绩"]):
        ws.write(3, k, v)
    for row, item in enumerate(students):
        score = student_results_dict.get(item.student.pk, "")
        score = "" if score is None else str(score)

        row = row + 4
        ws.write(row, 0, klass.uuid, style)
        ws.write(row, 1, item.uuid, style)
        ws.write(row, 2, item.student.name, style)
        ws.write(row, 3, score, style)
    import tempfile
    tmpxls = tempfile.SpooledTemporaryFile()
    wb.save(tmpxls)
    tmpxls.seek(0)
    from utils.utils import send_file
    filename = u"%(learning_year_verbose_name)s_%(semester)s_%(name)s_%(grade)s_%(klass)s_%(subject)s.xls" \
            % {"learning_year_verbose_name": exam_subject.exam.learning_year_verbose_name,
               "semester": exam_subject.exam.semester,
               "grade": exam_subject.grade,
               "klass": klass.name,
               "name": exam_subject.exam.category.name,
               "subject": exam_subject.category.name}
    return send_file(request, tmpxls, filename)

@permission_required("exam.export_result_by_room_subject")
def export_result_by_room_subject(request):
    """导出某考科目的某个考试室的成绩录入表格"""
    subject_pk = request.GET.get("subject_pk", None)
    room_pk = request.GET.get("room_pk", None)

    subject = Subject.objects.get(pk=subject_pk)
    room = Room.objects.get(pk=room_pk)
    seat_list = room.seat_set.all()
    student_list = seat_list.values_list("examinee", flat=True)

    student_results = Result.objects.filter(subject=subject, student__in=student_list).values_list("student", "score")
    student_results_dict = dict(student_results)

    print student_results_dict

    from pyExcelerator import Workbook, Font, XFStyle, Alignment
    wb = Workbook()
    ws = wb.add_sheet(u"考试成绩录入")
    t_font, al, t_style, style = Font(), Alignment(), XFStyle(), XFStyle()
    t_font.bold = True
    t_font.height = 18*0x14
    t_style.font = t_font
    al.horz = Alignment.HORZ_CENTER
    style.alignment = al

    ws.write(0, 0, u"考试课程编号")
    ws.write(0, 1, subject.pk)
    title = u"%(learning_year_verbose_name)s %(semester)s %(grade)s %(subject)s %(room)s " \
            % {"learning_year_verbose_name": subject.exam.learning_year_verbose_name,
               "semester": subject.exam.semester,
               "grade": subject.grade,
               "room": room.name,
               "subject": subject.category.name}

    ws.write_merge(1, 1, 0, 3, title, t_style)
    ws.write_merge(2, 2, 0, 3, u"备注：上面的标题不要改动，否则无法正确导入成绩到系统中，请按以下格式录入成绩")
    for k, v in enumerate([u"班别", u"学号", u"姓名", u"座号", u"分数成绩"]):
        ws.write(3, k, v)

    seat_list = list(seat_list)
    seat_list.sort(key=lambda s: int(s.uuid))
    for row, item in enumerate(seat_list):
        score = str(student_results_dict.get(item.examinee_id, "") or "")
        row = row + 4
        ws.write(row, 0, item.klass.uuid, style)
        ws.write(row, 1, item.classmate.uuid, style)
        ws.write(row, 2, item.examinee.name, style)
        ws.write(row, 3, item.uuid, style)
        ws.write(row, 4, score, style)

    import tempfile
    tmpxls = tempfile.SpooledTemporaryFile()
    wb.save(tmpxls)
    tmpxls.seek(0)
    from utils.utils import send_file

    filename = u"%(learning_year_verbose_name)s_%(semester)s_%(name)s_%(grade)s_%(subject)s_%(room)s.xls" \
            % {"learning_year_verbose_name": subject.exam.learning_year_verbose_name,
               "semester": subject.exam.semester,
               "grade": subject.grade,
               "room": room.name,
               "name": subject.exam.category.name,
               "subject": subject.category.name}
    return send_file(request, tmpxls, filename)

@permission_required("exam.add_studentexamresult_by_class_step3")
def add_studentexamresult_by_class_step3(request, exam_subject_pk, class_pk):
    if request.method == "GET":
        exam_subject = Subject.objects.get(pk=exam_subject_pk)
        class_ = Class.objects.get(pk=class_pk)
        students = class_.student_set.all().order_by("name")
        student_exam_result = Result.objects.filter(exam_subject=exam_subject_pk, student__in=students).order_by("student__gender")

        exam_students = []
        exam_students_pks = []
        for s in student_exam_result:
            student = students.get(pk=s.student.pk)
            setattr(student, "score", s.score)
            exam_students.append(student)
            exam_students_pks.append(s.student.pk)

        for s in students:
            if s.pk not in exam_students_pks:
                setattr(s, "score", 0)
                exam_students.append(s)

        action = request.GET.get("action", "initial")
        if action == "initial":
            exam_students.sort(key=lambda d:d.student.name, reverse=True)
        elif action == "save":
            exam_students.sort(key=lambda d:d.score, reverse=True)

        return render_to_response("school/add_student_exam_result_by_class_step3.xhtml", {
            "site": u"PingNi.com",
            "exam_subject": exam_subject,
            "students": exam_students,
            "class": class_,
            "action": action,
        }, context_instance=RequestContext(request))
    elif request.method == "POST":
        #print request.POST
        for k in request.POST:
            if k.startswith("student_pk_"):
                student_pk = k.rsplit("_")[-1]
                try:
                    score = Decimal(request.POST.get(k))
                except:
                    score = None
                try:
                    result = Result.objects.get(student=student_pk, exam_subject = exam_subject_pk)
                    result.score = score
                except:
                    result = Result(
                        student_id = student_pk,
                        exam_subject_id = exam_subject_pk,
                        score = score,
                        level = None
                    )
                result.save()
        return HttpResponseRedirect(request.path + "?action=save")

@permission_required("exam.add_studentexamresult_by_school")
def add_studentexamresult_by_school(request):
    """按班录入学生的考试成绩"""

    from exam.models import Exam, Subject
    from school.models import Subject
    exams = Exam.objects.all()
    latest_exam = Exam.objects.all().order_by("dtexamed")[0]
    latest_exam_subjects = Subject.objects.filter(exam=latest_exam).order_by("-grade")
    subjects = Subject.objects.all()

    classes = Class.objects.all()

    def classes_wrap(classes):
        _classes = {}
        for m in classes:
            g = m.grade.code
            _classes.setdefault(g, []).append(m)
            if _classes.get(g):
                _classes[g].append(m)
            else:
                _classes[g] = [m]
        order_by = sorted(_classes.keys(), reverse=True)
        sorted_classes = [_classes[m] for m in order_by]
        return sorted_classes

    def exam_subjects_wrap(student_exam_subject):
        exam_subjects = {}
        for m in student_exam_subject:
            g = m.grade.code
            if exam_subjects.get(g):
                exam_subjects[g].append(m)
            else:
                exam_subjects[g] = [m]
        #return exam_subjects
        order_by = sorted(exam_subjects.keys(), reverse=True)
        sorted_exam_subjects = [exam_subjects[m] for m in order_by]
        return sorted_exam_subjects
    exam_subjects = exam_subjects_wrap(latest_exam_subjects)
    classes = classes_wrap(classes)
    #print classes
    #print exam_subjects
    return render_to_response("school/add_student_exam_result_by_school.xhtml", {
        "site": u"PingNi.com",
        "exams": exams,
        "classes": classes,
        "subjects": subjects,
        "exam_subjects": exam_subjects, 
    }, context_instance=RequestContext(request))

@permission_required("exam.import_result_by_room")
@render_to("exam/import_result_by_room.html")
def import_result_by_room(request, template=None):
    """由考室名单导入成绩"""
    if request.method == "GET":
        return {}, template
    elif request.method == "POST":
        if request.FILES:
            file_uploaded = request.FILES["file"]
            sheet = parse_xls(file_uploaded)[0][1]
            rows = max([r[0] for r in sheet])
            cols = max([c[1] for c in sheet])
            title = sheet.get((1, 0), None)
            exam_subject_pk = sheet.get((0, 1), None)
            #print exam_subject_pk
            #print rows, cols
            imported_result = []
            success_import_count = 0
            failure_import_count = 0
            for r in range(4, rows+1):
                klass = sheet.get((r, 0), None) #班级
                uuid = sheet.get((r, 1), None) #学号
                name = sheet.get((r, 2), None) #姓名
                score = sheet.get((r, 4), None) #分数成绩
                try:
                    #student = Student.objects.get(pk=uuid)
                    klass = Class.objects.get(uuid=klass)
                    classmate = Classmate.objects.get(uuid=uuid)
                    student = classmate.student
                    exam_subject = Subject.objects.get(pk=exam_subject_pk)
                    result = Result(
                        student = student,
                        klass = klass,
                        subject = exam_subject,
                        score = Decimal(score),
                        creator = request.person,
                    )
                    result.save()
                except IntegrityError,e:
                    result  = Result.objects.get(student=student, subject=exam_subject)
                    result.score = Decimal(score)
                    result.klass_id = klass
                    result.save()
                    level = result.level
                    is_imported = True
                except:
                    is_imported = False
                    level = None
                finally:
                    if is_imported:
                        success_import_count = success_import_count + 1
                    else:
                        failure_import_count = failure_import_count + 1
                    imported_result.append({
                        "is_imported": is_imported,
                        "class": klass, 
                        "uuid": uuid, 
                        "name": name, 
                        "score": score,
                        "level": level,
                    })
        return {
            "import_result": imported_result,
            "action": "import",
            "title": title,
            "success_import_count": success_import_count,
            "failure_import_count": failure_import_count,
        }, template

@permission_required("exam.import_result_by_class")
@render_to("exam/import_result_by_class.html")
def import_result_by_class(request, template=None):
    """按自然班名单导入成绩, excel格式"""
    if request.method == "GET":
        return {}, template
    elif request.method == "POST":
        if request.FILES:
            file_uploaded = request.FILES["file"]
            sheet = parse_xls(file_uploaded)[0][1]
            rows = max([r[0] for r in sheet])
            cols = max([c[1] for c in sheet])
            title = sheet.get((1, 0), None)
            exam_subject_pk = sheet.get((0, 1), None)
            #print exam_subject_pk
            #print rows, cols
            imported_result = []
            success_import_count = 0
            failure_import_count = 0
            for r in range(4, rows+1):
                klass = sheet.get((r, 0), None) #班级
                uuid = sheet.get((r, 1), None) #学号
                name = sheet.get((r, 2), None) #姓名
                score = sheet.get((r, 3), None) #分数成绩
                try:
                    #student = Student.objects.get(pk=uuid)
                    classmate = Classmate.objects.get(uuid=uuid)
                    student = classmate.student
                    exam_subject = Subject.objects.get(pk=exam_subject_pk)
                    result = Result(
                        student = student,
                        subject = exam_subject,
                        klass_id = klass,
                        score = Decimal(score),
                        creator = request.person,
                    )
                    result.save()
                    print result
                    level = result.level
                    is_imported = True
                except IntegrityError,e:
                    try:
                        s = Result.objects.get(student__classmate=uuid, subject=exam_subject_pk)
                        s.score = Decimal(score)
                        s.save()
                        level = result.level
                        is_imported = True
                    except Exception, e:
                        print e
                except:
                    is_imported = False
                    level = None
                finally:
                    if is_imported:
                        success_import_count = success_import_count + 1
                    else:
                        failure_import_count = failure_import_count + 1
                    imported_result.append({
                        "is_imported": is_imported,
                        "class": klass, 
                        "uuid": uuid, 
                        "name": name, 
                        "score": score,
                        "level": level,
                    })
        return {
            "import_result": imported_result,
            "action": "import",
            "title": title,
            "success_import_count": success_import_count,
            "failure_import_count": failure_import_count,
        }, template

@permission_required("exam.import_result")
@render_to("exam/import_result.html")
def import_result(request, template=None):
    if request.method == "GET":
        return {}, template
    elif request.method == "POST":
        category = request.POST.get("category", None)
        if category == "import_result_by_room":
            print "category room "
            return import_result_by_room(request, template=None)
        elif category == "import_result_by_class":
            print "category class" 

            #return import_result_by_class(request, template=None)
            res = import_result_by_class(request, template=None)
            print res
            return res
            return import_result_by_class(request, template=None)
        else:
            return HttpResponse(u"导入成绩文件的种类不正确")

@permission_required("exam.analysis_class")
def analysis_class(request, exam_pk=None):
    """分析班级成绩第一步，选择哪次考试"""
    exams = Exam.objects.all().order_by("-learning_year")
    try:
        current_exam = Exam.objects.get(pk=exam_pk)
    except Exam.DoesNotExist:
        current_exam = exams[0]
    current_classes = Class.objects.filter(dtcreated__year=current_exam.learning_year[:4]).order_by("-grade", "-class_no")
    return render_to_response("school/analysis_class.xhtml", {
        "exams": exams,
        "current_exam": current_exam,
        "current_classes": current_classes,
    }, context_instance=RequestContext(request))

@permission_required("exam.analyse_student")
#@cache_page(60*15)
@render_to("exam/analyse_student.html")
def analyse_student(request, template=None):
    """分析某班学生某次考试详情"""
    exam_pk = request.GET.get("exam_pk", None)
    klass_pk = request.GET.get("klass_pk", None)
    grade_pk = request.GET.get("grade_pk", None)
    page = request.GET.get("page", 1)
    subject_pk = request.GET.get("subject_pk", None)
    title = ""
    #import time
    #dtstart = time.time()
    
    exams = Exam.objects.all().order_by("-learning_year")
    try:
        current_exam = Exam.objects.get(pk=exam_pk)
    except Exam.DoesNotExist:
        current_exam = exams[0]

    filter = Q(subject__exam=current_exam)
    if grade_pk:
        grade = GradeCode.objects.get(pk=grade_pk)
        subjects = current_exam.subject_set.filter(grade=grade)
        title = u"%s " % grade
        filter = filter & Q(klass__grade=grade)
    elif klass_pk:
        klass = Class.objects.get(pk=klass_pk)
        subjects = current_exam.subject_set.filter(grade=klass.grade)
        title = u"%s " % klass
        filter = filter & Q(klass=klass)
    else:
        random_subject = current_exam.subject_set.all()[0]
        grade = random_subject.grade
        subjects = current_exam.subject_set.filter(grade=grade)
        title = u"%s " % grade
        filter = filter & Q(klass__grade=grade)


    from exam.misc import DecimalRanking
    from django.utils.datastructures import SortedDict

    ordered_result_list = Result.objects.filter(filter).values("student__uuid", "student", "student__gender__name", "student__name", "klass__uuid").annotate(Sum("score")).order_by("-score__sum")
    #ordered_result_list_length = ordered_result_list.count() 

    #ordered_result_list_pages = Paginator(ordered_result_list, 20)
    #page_ordered_result_list = ordered_result_list_pages.page(page).object_list

    result_list = Result.objects.filter(filter).values("subject", "score", "student")
    result_dict = SortedDict()
    for r in result_list:
        key = r["subject"], r["student"]
        result_dict[key] = r["score"]

    klass_dict = defaultdict()
    for r in ordered_result_list:
        klass = r.get("klass__uuid", None)
        klass_dict.setdefault(klass, [])

    subject_list = subjects.values_list("pk", flat=True)

    #rankings = SortedDict()
    rankings = []
    for index, student in enumerate(ordered_result_list):
        if index == 0:
            ranking = 1
        else:
            if student.get("score__sum") != pre_student.get("score__sum"):
                ranking = index + 1
        if student["score__sum"] is None:
            student["score__sum"] = 0
        pre_student = student
        
        klass = student.get("klass__uuid", None)
        score__sum = DecimalRanking(student.get("score__sum", 0))
        try:
            last_klass_item = klass_dict[klass][-1]
        except IndexError,e:
            score__sum.ranking = 1
            score__sum.next_ranking = 2
            klass_dict[klass].append(score__sum)
            klass_ranking = 1
        else:
            if last_klass_item == score__sum:
                klass_ranking = last_klass_item.ranking
            else:
                klass_ranking = last_klass_item.next_ranking
            score__sum.ranking = klass_ranking
            score__sum.next_ranking = last_klass_item.next_ranking + 1
            klass_dict[klass].append(score__sum)

        #加上这次考试各科目成绩
        #如何加在此，则所有要排序的学生都会加上， 而页面只显示其他一小部分数据
        #效率上考虑, 把增加科目的功能放在只要显示数目上面,移动到分页功能后
        #_subject_list = []
        #for c in subject_list:
            #try:
                #subject_score = result_dict[(c, student.get("student"))]
            #except KeyError,e:
                #subject_score = None 
            #_subject_list.append(subject_score)

        student_info = {
            "student": student.get("student", None),
            "student__uuid": student.get("student__uuid", None),
            "klass": klass,
            "ranking": ranking,
            "klass_ranking": klass_ranking,
            "score": score__sum,
            "name": student.get("student__name", None),
            "gender": student.get("student__gender__name", None),
            #"subject_list": _subject_list,
        }
        student_pk = student.get("student", None)
        rankings.append(student_info)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    print query_part
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(rankings, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    #加上这次考试各科目成绩
    for student in pages.cur_page.object_list:
        _subject_list = []
        for c in subject_list:
            try:
                subject_score = result_dict[(c, student.get("student"))]
            except KeyError,e:
                subject_score = None 
            _subject_list.append(subject_score)
        student["subject_list"] = _subject_list

    #dtend = time.time()
    #query_time = dtend - dtstart

    return {
        "exams": exams,
        "current_exam": current_exam,
        "rankings": pages.cur_page.object_list,
        #"rankings": rankings,
        "pages": pages,
        "subjects": subjects,
        "title": title,
        "grade_pk": grade_pk,
        "klass_pk": klass_pk,
        #"query_time": query_time, 
    }, template

@permission_required("exam.analysis_class_student2")
def analysis_class_student2(request, exam_pk=None, class_pk=None):
    """分析某班学生某次考试详情, 速度比上 analysis_class_student 慢"""
    exams = Exam.objects.all().order_by("-learning_year")
    try:
        current_exam = Exam.objects.get(pk=exam_pk)
    except Exam.DoesNotExist:
        current_exam = exams[0]

    class_= Class.objects.get(pk=class_pk)
    subjects = current_exam.subject_set.filter(grade=class_.grade)
    #此处还将加上学校字段的限制
    #students = Student.objects.filter(classes__grade=grade, classes__dtcreated__year=current_exam.learning_year[:4])
    students = class_.student_set.all()
    grade_rankings = misc.grade_sum_score_ranking(current_exam, class_.grade)

    classes_rankings = {}
    for student in students:
        result = []
        for subject  in subjects:
            try:
                score = subject.result_set.get(student=student)
            except Result.DoesNotExist:
                score = None
            result.append(score)
        setattr(student, "score", result)
        try:
            class_ = student.classes.filter(dtcreated__year=current_exam.learning_year[:4])[0]
            try:
                class_rankings = classes_rankings[class_.pk]
            except:
                class_rankings = misc.class_sum_score_ranking(current_exam, class_.pk)
                classes_rankings[class_.pk] = class_rankings
            setattr(student, "sum_score_class_ranking", class_rankings.get(student.pk, 0))
        except:
            class_ = None
            setattr(student, "sum_score_class_ranking", None)
        setattr(student, "class_", class_)
        setattr(student, "sum_score_grade_ranking", grade_rankings.get(student.pk, 0))

    students = sorted(students, key=operator.attrgetter("sum_score_class_ranking"), reverse=True)

    return render_to_response("school/analysis_class_student2.xhtml", {
        "exams": exams,
        "current_exam": current_exam,
        #"students": students[0:100],
        "students": students,
        "class": class_,
        "stat_item_step": range(len(subjects)),
        "subjects": subjects,
    }, context_instance=RequestContext(request))

@permission_required("exam.analysis_grade_student")
def analysis_grade_student(request, exam_pk=None, grade_pk=None):
    """分析某班学生某次考试详情"""
    exams = Exam.objects.all().order_by("-learning_year")
    try:
        current_exam = Exam.objects.get(pk=exam_pk)
    except Exam.DoesNotExist:
        current_exam = exams[0]

    grade = GradeCode.objects.get(pk=grade_pk)
    subjects = current_exam.subject_set.filter(grade=grade)
    #此处还将加上学校字段的限制
    students = Student.objects.filter(classes__grade=grade, classes__dtcreated__year=current_exam.learning_year[:4])
    grade_rankings = misc.grade_sum_score_ranking(current_exam, grade_pk)

    classes_rankings = {}
    for student in students:
        result = []
        for subject  in subjects:
            try:
                score = subject.result_set.get(student=student)
                score.analysis = misc.analyse_score(score)
            except Result.DoesNotExist:
                score = None
            result.append(score)
        setattr(student, "score", result)
        try:
            class_ = student.classes.filter(dtcreated__year=current_exam.learning_year[:4])[0]
            try:
                class_rankings = classes_rankings[class_.pk]
            except:
                class_rankings = misc.class_sum_score_ranking(current_exam, class_.pk)
                classes_rankings[class_.pk] = class_rankings
            setattr(student, "sum_score_class_ranking", class_rankings.get(student.pk, 0))
        except:
            class_ = None
            setattr(student, "sum_score_class_ranking", None)
        setattr(student, "class_", class_)
        setattr(student, "sum_score_grade_ranking", grade_rankings.get(student.pk, 0))

    students = sorted(students, key=operator.attrgetter("sum_score_class_ranking"), reverse=True)

    return render_to_response("exam/analysis_grade_student.xhtml", {
        "exams": exams,
        "current_exam": current_exam,
        #"students": students[0:100],
        "students": students,
        "grade": grade,
        "stat_item_step": range(len(subjects)),
        "subjects": subjects,
    }, context_instance=RequestContext(request))

@permission_required("exam.analyse_class")
#@cache_page(60*15)
@render_to("exam/analyse_class.html")
def analyse_class(request, template=None):
    """某一次考试各科目班级成绩统计"""
    exam_pk = request.GET.get("exam_pk", None)
    exams = Exam.objects.all().order_by("-learning_year")
    try:
        current_exam = Exam.objects.get(pk=exam_pk)
    except Exam.DoesNotExist:
        current_exam = exams[0]
    current_classes = Class.objects.filter(dtcreated__year=current_exam.learning_year[:4]).order_by("grade", "uuid")
    grade_subjects = defaultdict(list)
    grade_classes = defaultdict(list)
    for cls in current_classes:
        exam_subjects = Subject.objects.filter(grade=cls.grade, exam=current_exam)
        class_subjects = []
        for subject in exam_subjects:
            e_result_aggregate = subject.result_set.filter(student__classes__in=[cls.pk]).aggregate(\
                Sum("score"), Avg("score"), Count("score"), StdDev("score"), Max("score"), Min("score"))
            subject.stat = e_result_aggregate
            subject.stat["excellent_rate"] = misc.calc_subject_excellent_rate(subject, cls) #优秀率
            subject.stat["fine_rate"] = misc.calc_subject_fine_rate(subject, cls) #良好率
            subject.stat["pass_rate"] = misc.calc_subject_pass_rate(subject, cls) #合格率
            #通过如下方式计算，是为了确保 优秀率 ＋ 良好率 ＋ 合格率 ＋ 不合格率 ＝ 100
            #subject.stat["unpass_rate"] = 100 - subject.stat["pass_rate"] - subject.stat["fine_rate"] - subject.stat["excellent_rate"] #不合格率
            subject.stat["unpass_rate"] = misc.calc_subject_unpass_rate(subject, cls) #不合格率

            grade_subjects[cls.grade.pk].append(subject) 
            class_subjects.append(subject)
        setattr(cls, "class_subjects", class_subjects)

        if cls not in grade_classes[cls.grade.pk]:
            grade_classes[cls.grade.pk].append(cls)
        setattr(cls, "grade_classes", grade_classes[cls.grade.pk])

        exam_subjects_nums = len(exam_subjects)
        for subject in exam_subjects:
            subject.stat["avg_excellent_rate"] = sum([s.stat["excellent_rate"] for s in exam_subjects if s.stat["excellent_rate"] is not None]) / exam_subjects_nums
            subject.stat["avg_fine_rate"] = sum([s.stat["fine_rate"] for s in exam_subjects if s.stat["fine_rate"] is not None]) / exam_subjects_nums
            subject.stat["avg_pass_rate"] = sum([s.stat["pass_rate"] for s in exam_subjects if s.stat["pass_rate"] is not None]) / exam_subjects_nums
            subject.stat["avg_unpass_rate"] = sum([s.stat["unpass_rate"] for s in exam_subjects if s.stat["unpass_rate"] is not None]) / exam_subjects_nums
            subject.stat["avg_score__avg"] = sum([s.stat["score__avg"] for s in exam_subjects if s.stat["score__avg"] is not None]) / exam_subjects_nums
            subject.stat["avg_score__max"] = sum([s.stat["score__max"] for s in exam_subjects if s.stat["score__max"] is not None]) / exam_subjects_nums
            subject.stat["avg_score__min"] = sum([s.stat["score__min"] for s in exam_subjects if s.stat["score__min"] is not None]) / exam_subjects_nums
            subject.stat["avg_score__stddev"] = sum([s.stat["score__stddev"] for s in exam_subjects if s.stat["score__stddev"] is not None]) / exam_subjects_nums

        setattr(cls, "exam_subjects", exam_subjects)
    for cls in current_classes:
        setattr(cls, "grade_subjects", grade_subjects[cls.grade.pk])

    return {
        "exams": exams,
        "current_exam": current_exam,
        "current_classes": current_classes,
        "now": datetime.datetime.now(),
    }, template

@permission_required("exam.analyse_grade")
#@cache_page(60*15)
@render_to("exam/analyse_grade.html")
def analyse_grade(request, template=None):
    """分析某一次考试年级的统计分析数据"""
    exam_pk = request.GET.get("exam_pk", None)
    exams = Exam.objects.all().order_by("-learning_year")
    try:
        current_exam = Exam.objects.get(pk=exam_pk)
    except Exam.DoesNotExist:
        current_exam = exams[0]
    exam_subjects = current_exam.subject_set.all()
    exam_grade_subjects = defaultdict(list)
    for subject in exam_subjects:
        total = subject.result_set.count()
        excellent_score = str(subject.full_score * 0.9)
        fine_score = str(subject.full_score * 0.8)
        pass_score = str(subject.full_score * 0.6)
        excellent_num = subject.result_set.filter(score__gte=excellent_score).count()
        fine_num = subject.result_set.filter(score__gte=fine_score, score__lt=excellent_score).count()
        pass_num = subject.result_set.filter(score__gte=pass_score, score__lt=fine_score).count()
        #unpass_num = subject.result_set.filter(score__lt=pass_score).count()
        avg_score = subject.result_set.aggregate(Avg("score")).get("score__avg", None)
        stddev_score = subject.result_set.aggregate(StdDev("score")).get("score__stddev", None)
        max_score = subject.result_set.aggregate(Max("score")).get("score__max", None)
        min_score = subject.result_set.aggregate(Min("score")).get("score__min", None)
        try:
            excellent_rate = float(excellent_num) / total * 100
            fine_rate = float(fine_num) / total * 100
            pass_rate = float(pass_num) / total * 100
            unpass_rate = 100 - excellent_rate - fine_rate - pass_rate
        except ZeroDivisionError,e:
            excellent_rate = None
            fine_rate = None
            pass_rate = None
            unpass_rate = None
        subject.stat = {
            "excellent_rate": excellent_rate,
            "fine_rate": fine_rate,
            "pass_rate": pass_rate,
            "unpass_rate": unpass_rate,
            "avg_score": avg_score,
            "stddev_score": stddev_score,
            "min_score": min_score,
            "max_score": max_score,
        }
        exam_grade_subjects[subject.grade].append(subject)

    exam_grade_subjects = [s for s in exam_grade_subjects.values()]

    return {
        "exams": exams,
        "exam_grade_subjects": exam_grade_subjects,
        "current_exam": current_exam,
        "now": datetime.datetime.now(),
        "exam_subjects": exam_subjects,
    }, template

@permission_required("exam.analyse_subject")
#@cache_page(60*15)
@render_to("exam/analyse_subject.html")
def analyse_subject(request, template=None):
    """某一次考试按科目进行统计分析"""
    exam_pk = request.GET.get("exam_pk", None)
    exams = Exam.objects.all().order_by("-learning_year")
    try:
        current_exam = Exam.objects.get(pk=exam_pk)
    except Exam.DoesNotExist:
        current_exam = exams[0]
    exam_subjects = current_exam.subject_set.all()
    subjects = current_exam.subject_set.values_list("category", flat=True).annotate()
    subject_classes = [] 
    for subject in subjects:
        g_subjects = exam_subjects.select_related().filter(category=subject).order_by("-grade")
        grades = []
        class_list = []
        for g in g_subjects:
            #klass_list = g.result_set.values_list("klass", flat=True).annotate()
            #classes = Class.objects.filter(pk__in=klass_list)
            classes = g.grade.class_set.filter(dtcreated__year=g.exam.learning_year[:4]).order_by("-grade")
            for c in classes:
                stat = g.result_set.filter(klass=c).\
                       aggregate(Avg("score"), StdDev("score"), Max("score"), Min("score"))

                c.excellent_rate = misc.calc_subject_excellent_rate(g, c)
                c.fine_rate = misc.calc_subject_fine_rate(g, c)
                c.pass_rate = misc.calc_subject_pass_rate(g, c)
                c.unpass_rate = misc.calc_subject_unpass_rate(g,c)
                c.stat = stat
                c.subject = g
            class_list.extend(classes.all())
            # 计算级的统计
            cg = g.result_set.aggregate(Avg("score"), StdDev("score"), Max("score"), Min("score"))
            cg["grade_stat"] = True
            cg["grade"] = c.grade
            cg["excellent_rate"] = misc.calc_subject_excellent_rate(g, c.grade)
            cg["fine_rate"] = misc.calc_subject_fine_rate(g, c.grade)
            cg["pass_rate"] = misc.calc_subject_pass_rate(g, c.grade)
            cg["unpass_rate"] = misc.calc_subject_unpass_rate(g, c.grade)
            cg["stat"] = cg
            _classes = list(classes)
            _classes.append(cg)
            grades.append(_classes)
            class_list.append(cg)
        #print class_list
        #print "subject", subject, SubjectCategory.objects.get(pk=subject)
        subject_classes.append({
            "grade":grades,
            "subject": SubjectCategory.objects.get(pk=subject),
            "class_list": class_list,
        })

    return {
        "exams": exams,
        "current_exam": current_exam,
        "now": datetime.datetime.now(),
        "exam_subjects": exam_subjects,
        "subjects": subjects,
        "subject_classes": subject_classes,
    }, template

@login_required
def class_subject(request, exam_pk=None, subject_pk=None):
    """某次考试某班某科成绩"""
    pass

@login_required
@render_to("exam/grade_subject.html")
def grade_subject(request, subject_pk=None, template=None):
    """某次考试某级某科成绩"""
    exam_subject = Subject.objects.get(pk=subject_pk)
    exam_subject_students = exam_subject.result_set.all().order_by("-score")
    for index, student in enumerate(exam_subject_students):
        if index == 0:
            ranking = 1
        else:
            if student.score != pre_student.score:
                ranking = index + 1
        pre_student = student

        setattr(student, "ranking", ranking)
        analysis = misc.analyse_score(student)
        setattr(student, "analysis", analysis)

    return locals(), template
    #return render_to_response("exam/grade_subject.html", locals(), context_instance=RequestContext(request))

@permission_required("exam.add_studentexamsubject")
def add_studentexamsubject(request):
    """由学校来增加学生在校考试信息"""
    person = Person.objects.get(pk=request.user.pk)
    exam = request.GET.get("exam", None)
    exam = Exam.objects.get(pk=exam)

    form = AddSubjectForm(request.POST or None)
    if form.is_valid():
        _form = form.save(commit=False)
        _form.exam = exam
        _form.save()
        form.success = True

    return render_to_response("school/add_studentexamsubject.xhtml", {
        "site": u"PingNi.com",
        "form": form,
        "exam": exam,
    }, context_instance=RequestContext(request))

@permission_required("exam.manage_exam")
@render_to("exam/manage_exam.html")
def manage_exam(request, template=None):
    filter = Q()
    q = request.GET.get("q", "")
    if q:
        filter = filter & \
                 (
                     Q(name__icontains=q) |\
                     Q(exam_type__name__icontains=q) |\
                     Q(semester__name__icontains=q) |\
                     Q(learning_year__icontains=q)\
                 )
    exams = Exam.objects.filter(filter)

    #搜索分页结合
    page = request.REQUEST.get("page", 1)
    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qs in query_part:
        if not qs.startswith("page="):
            new_query_parts.append(qs)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(exams, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return {
        #"exams": exams,
        "exams": pages.cur_page.object_list,
        "q": q,
        "pages":  pages,
    }, template

@login_required
def manage_studentexamsubject(request):
    pass

@permission_required("exam.edit_studentexam")
def edit_studentexam(request, exam_pk):
    exam = Exam.objects.get(pk=exam_pk)
    form = EditExamForm(request.POST or None, instance=exam)
    if form.is_valid():
        form.save()
        form.success = True
    exam_subjects = exam.subject_set.all()
    return render_to_response("school/edit_studentexam.xhtml", {
        "form": form,
        "exam_subjects": exam_subjects,
        "exam": exam,
    }, context_instance=RequestContext(request))

@permission_required("exam.delete_studentexam")
def delete_studentexam(request, exam_pk):
    try:
        exam = Exam.objects.get(pk=exam_pk)
        exam.delete()
    except Exception,e:
        print e
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@permission_required("exam.delete_studentexamsubject")
def delete_studentexamsubject(request, exam_subject_pk):
    try:
        exam_subject = Subject.objects.get(pk=exam_subject_pk)
        exam_subject.delete()
    except Exception,e:
        print e
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@permission_required("exam.edit_studentexamsubject")
def edit_studentexamsubject(request, exam_subject_pk):
    exam_subject = Subject.objects.get(pk=exam_subject_pk)
    from exam.forms import EditSubjectForm
    form = EditSubjectForm(request.POST or None, instance=exam_subject)
    if form.is_valid():
        form.save()
        form.success = True
    return render_to_response("school/edit_studentexamsubject.xhtml", {
        "form": form,
        "exam_subject": exam_subject,
    }, context_instance=RequestContext(request))

@permission_required("exam.room_seat_arrange")
@render_to("exam/room_seat_arrange.html")
def room_seat_arrange(request, template=None):
    """试室座位编排"""
    if request.method == "GET":
        exam_list = Exam.objects.all()
        current_exam = exam_list[0]
        grade_list = Class.objects.filter(dtcreated__year=current_exam.learning_year[:4]).values("grade", "grade__name").annotate(klass_num=Count("uuid"))
        current_grade = grade_list[0]
        current_grade_uuid = "%(year)s%(grade)s" % {"year": current_exam.learning_year[0:4], "grade": current_grade["grade"] } 
        current_grade_num = Classmate.objects.filter(klass__uuid__startswith=current_grade_uuid).count()
        arranged_room_list = Room.objects.values_list("exam", "grade").annotate()
        arranged_room_str_list = []
        for e, g in arranged_room_list:
            arranged_room_str_list.append(u"%d.%s" % (e, g))
        print arranged_room_list
        return {
            "exam_list": exam_list,
            "grade_list": grade_list,
            "grade_student_num": current_grade_num,
            "arranged_room_list": json.dumps(list(arranged_room_str_list)),
        }, template
    elif request.method == "POST":
        postdata = request.POST.copy()
        exam_pk = postdata.get("exam", None)
        exam = get_object_or_404(Exam, pk=exam_pk)
        grade_pk = postdata.get("grade", None)
        grade = get_object_or_404(GradeCode, pk=grade_pk)
        arrange_way = request.POST.get("arrange_way", None)

        room = {}
        for r in postdata:
            if r.startswith("room_"):
                room_num = r.rsplit("_")[-1]
                room_col_num = postdata.get(r, None)
                room[room_num] = room_col_num
        print room

        #查询本本次考试某年级的学生列表
        query = Q(klass__dtcreated__year=exam.learning_year[:4]) & \
                Q(klass__grade=grade_pk) & \
                Q(dtend__isnull=True)
        members = Classmate.objects.filter(query)
        examinees = list(members)

        #生成座位表之前， 先删除之前的编排, 再重新编排
        arranged_room_list = Room.objects.filter(exam=exam, grade=grade)
        for r in arranged_room_list:
            r.delete()
        #print "members", members
        #得到考生记录
        #生成试室
        current_exam_room_uuid_list = Room.objects.filter(exam=exam).values_list("uuid", flat=True)
        try:
            max_room_uuid = max([int(s) for s in current_exam_room_uuid_list])
        except:
            max_room_uuid = 0

        print "max_room_uuid", max_room_uuid

        from random import randrange
        #产生试室列表
        new_room_list = []
        for k,v in room.items():
            uuid = str(int(k) + max_room_uuid),
            new_room = Room.objects.create(
                uuid = str(int(k) + max_room_uuid),
                name = u"第 %s 试室" % uuid, 
                exam = exam,
                grade = grade,
                seat_num = sum([int(n) for n in v.split(",")]),
                col_num = v,
            )
            new_room_list.append(new_room)

        #根据编排方式来生成座位表
        if arrange_way == "prev_exam_score": #按上次考试的总分成绩编排
            #按上次考试的总分成绩编排,尽可能把成绩好的学生编排在一个试室
            try:
                prev_exam = Exam.objects.order_by("-dtstart")[1]
            except IndexError, e:
                prev_exam = None
            else:
                ordered_examinee_pk_list = list(Result.objects.filter(subject__exam=prev_exam).values_list("student", flat=True).annotate(Sum("score")).order_by("-score__sum"))
                #assert False, ordered_examinee_pk_list
                max_examinee_index = len(ordered_examinee_pk_list)

                def sorted_by_sum_score(examinee):
                    try:
                        index = ordered_examinee_pk_list.index(examinee.person_id)
                    except Exception,e :
                        index = max_examinee_index
                    return index

                #如下是已经按总分由高到低排序过的考生名单
                examinees.sort(key=sorted_by_sum_score)
                #assert False, examinees

                for new_room in new_room_list:
                    from itertools import count
                    from random import shuffle
                    uuid_counter =  count(1)
                    seat_col_num_list = new_room.col_num.split(",")
                    seat_num = sum([int(n) for n in seat_col_num_list])

                    #获得一个由高到低分学生名单后，再重新随机打散顺序
                    new_room_examinees = examinees[:seat_num]
                    shuffle(new_room_examinees)
                    del examinees[:seat_num]

                    new_room_seat_dict = {}
                    for m in range(len(seat_col_num_list)):
                        for n in range(int(seat_col_num_list[m])):
                            row = n + 1
                            col = m + 1
                            uuid = uuid_counter.next()

                            if row == 1 and col == 1:
                                examinee = new_room_examinees.pop(0)
                            else:
                                last_examinee_index = len(new_room_examinees) - 1
                                for index, examinee in enumerate(new_room_examinees):
                                    if row == 1:
                                        left_examinee = new_room_seat_dict[row, col-1] 
                                        if examinee.klass == left_examinee.klass and index != last_examinee_index :
                                            continue
                                        else:
                                            break
                                    if col == 1:
                                        top_examinee = new_room_seat_dict[row-1, col]
                                        if examinee.klass == top_examinee.klass and index != last_examinee_index:
                                            continue
                                        else:
                                            break 
                                    else:
                                        left_examinee = new_room_seat_dict[row, col-1]
                                        top_examinee = new_room_seat_dict[row-1, col]
                                        if examinee.klass == top_examinee.klass or \
                                           examinee.klass == left_examinee.klass  and index != last_examinee_index:
                                            continue
                                        else:
                                            break
                                examinee = new_room_examinees.pop(index)
                            new_room_seat_dict[row,col] = examinee
                            print examinee

                            new_seat = Seat.objects.create(
                                examinee = examinee.person.student,
                                klass = examinee.klass,
                                classmate = examinee,
                                room = new_room,
                                uuid = uuid,
                                row = row,
                                col = col,
                            )

        if arrange_way == "pure_random" or prev_exam is None: #没有之前一次考试成绩数据， 只好按单纯的随机编排
            for new_room in new_room_list:
                from itertools import count
                uuid_counter =  count(1)
                seat_col_num_list = new_room.col_num.split(",")
                seat_num = sum([int(n) for n in seat_col_num_list])

                for m in range(len(seat_col_num_list)):
                    for n in range(int(seat_col_num_list[m])):
                        row = n + 1
                        col = m + 1
                        uuid = uuid_counter.next()

                        randnum = randrange(0, len(examinees))
                        examinee = examinees.pop(randnum)

                        new_seat = Seat.objects.create(
                            examinee = examinee.student,
                            klass = examinee.klass,
                            room = new_room,
                            uuid = uuid,
                            classmate = examinee,
                            row = row,
                            col = col,
                        )
        return redirect("exam.views.room_seat")

@permission_required("exam.room_seat")
@render_to("exam/room_seat.html")
def room_seat(request, template=None):
    """考室座位表"""
    exam_pk = request.GET.get("exam_pk", None)
    room_pk = request.GET.get("room_pk", None)
    action = request.GET.get("action", None)

    if action == "Print":
        template = "exam/print_room_seat.html"

    exam_list = Exam.objects.all()
    if exam_pk is None:
        current_exam = exam_list[0]
    else:
        current_exam = get_object_or_404(Exam, pk=exam_pk)

    current_room_list = current_exam.room_set.all()
    if room_pk is None:
        try:
            current_room = current_room_list[0]
        except:
            return HttpResponse(u"数据还没有准备好， 暂时没有访问")
    else:
        current_room = get_object_or_404(Room, pk=room_pk)

    current_seat_list = current_room.seat_set.all().order_by("col", "row")

    current_seat_array = []
    current_room_col_num_list  = current_room.col_num.split(",")

    for col in current_room_col_num_list:
        current_seat_array.append([])

    for k, s in enumerate(current_seat_list):
        current_seat_array[s.col-1].append(s)

    #填充列表，使得每行每行的元素个数相同
    max_room_col_num = max(current_room_col_num_list)
    for col in current_seat_array:
        delta = int(max_room_col_num) - len(col)
        if delta > 0:
            col.extend([None] * delta)

    import itertools
    current_seat_array = map(list, itertools.izip(*current_seat_array))
    #current_seat_array = map(list, zip(*current_seat_array))
    return {
        "exam_list": exam_list,
        "current_exam": current_exam,
        "current_room": current_room,
        "current_room_list": current_room_list,
        "current_seat_list": current_seat_list,
        "current_seat_array": current_seat_array,
        "current_room_col_num_list": current_room_col_num_list,
    }, template

@permission_required("exam.export_seat_list")
def export_seat_list(request):
    """导出exam_pk考试room_pk考室登分表"""
    exam_pk = request.GET.get("exam_pk", None)
    room_pk = request.GET.get("room_pk", None)

    exam = get_object_or_404(Exam, pk=exam_pk)
    room = get_object_or_404(Room, pk=room_pk)

    #获得此此次考试的试室座位（考生)名单
    seat_list = get_list_or_404(Seat, room=room_pk)
    #获得此次考试有几门科目
    subject_list = get_list_or_404(Subject, exam=exam_pk)

    #student_results = Result.objects.filter(subject=exam_subject_pk, student__in=students.values_list("id")).values_list("student", "score")
    #student_results_dict = dict(student_results)

    from pyExcelerator import Workbook, Font, XFStyle, Alignment

    wb = Workbook()
    t_font, al, t_style, style = Font(), Alignment(), XFStyle(), XFStyle()
    t_font.bold = True
    t_font.height = 18*0x14
    t_style.font = t_font
    al.horz = Alignment.HORZ_CENTER
    style.alignment = al

    for subject in subject_list:
        sheet_name = u"%s" % subject.name
        ws = wb.add_sheet(sheet_name)
        ws.write(0,0, u"考试科目编号")
        ws.write(0,1, subject.pk)
        title = u"%(learning_year)s %(semester)s %(exam)s %(room)s %(subject)s 登分表" % {
            "room": room,
            "learning_year": exam.learning_year_verbose_name,
            "semester": exam.semester.name,
            "exam": exam.name,
            "subject": subject.name,
        }
        ws.write_merge(1, 1, 0, 10, title, t_style)

        #生成标题项目
        for k, v in enumerate([u"序号", u"座号", u"学号", u"姓名", u"成绩"]):
            ws.write(2, k, v)

        for index, seat in enumerate(seat_list):
            row = index + 3
            ws.write(row, 0, index+1, style)
            ws.write(row, 1, seat.uuid, style)
            ws.write(row, 2, seat.examinee.pk, style) 
            #ws.write(row, 2, seat.examinee.uuid, style) 
            ws.write(row, 3, seat.examinee.name, style)
            ws.write(row, 4, u"", style)

    import tempfile
    tmpxls = tempfile.SpooledTemporaryFile()
    wb.save(tmpxls)
    tmpxls.seek(0)
    from utils.utils import send_file
    filename = u"%(learning_year)s %(semester)s %(exam)s %(room)s 登分表.xls" % {
        "room": room,
        "learning_year": exam.learning_year_verbose_name,
        "semester": exam.semester.name,
        "exam": exam.name,
    }
    return send_file(request, tmpxls, filename)


#@permission_required("exam.subject_list")
@login_required
@render_to("exam/subject_list.html")
def subject_list(request, pk=None, template=None):
    """显示考试信息"""

    q = request.REQUEST.get("q","")
    page = request.REQUEST.get("page", 1)

    filter = Q()
    if q:
        glist = Result.objects.filter(klass__uuid__icontains=q).values_list("subject__grade", flat=True).annotate()
        print glist
        filter = filter & Q(grade__in=glist)
    subject_list = Subject.objects.filter(filter)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(subject_list, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return {
        "subject_list": pages.cur_page.object_list,
        "pages": pages,
        "q": q,
    }, template

@permission_required("exam.subject_ranking")
@render_to("exam/subject_ranking.html")
def subject_ranking(request, subject_pk=None, template=None):
    """单科班级排名"""
    klass_pk = request.GET.get("klass_pk", None)
    subject = Subject.objects.get(pk=subject_pk)
    ordered_result_list = subject.result_set.all().order_by("-score")

    klass_dict = defaultdict()
    for r in ordered_result_list:
        klass = r.klass_id
        klass_dict.setdefault(klass, [])

    rankings = []
    for index, student in enumerate(ordered_result_list):
        if index == 0:
            ranking = 1
        else:
            if student.score != pre_student.score:
                ranking = index + 1
        pre_student = student

        setattr(student, "ranking", ranking)
        analysis = misc.analyse_score(student)
        setattr(student, "analysis", analysis)

        klass = student.klass_id
        try:
            last_klass_item = klass_dict[klass][-1]
        except IndexError,e:
            setattr(student, "klass_ranking", 1)
            setattr(student, "klass_next_ranking", 2)
            klass_dict[klass].append(student)
            klass_ranking = 1
        else:
            if last_klass_item.score == student.score :
                klass_ranking = last_klass_item.klass_ranking
            else:
                klass_ranking = last_klass_item.klass_next_ranking
            setattr(student, "klass_ranking", klass_ranking)
            setattr(student, "klass_next_ranking", last_klass_item.klass_next_ranking + 1)
            klass_dict[klass].append(student)

        if klass_pk:
            if student.klass_id == long(klass_pk):
                rankings.append(student)
        else:
            rankings.append(student)

    page = request.GET.get("page", 1)
    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    print query_part
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(rankings, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    if klass_pk:
        klass = get_object_or_404(Class, pk=klass_pk)
    else:
        klass = None

    #dtend = time.time()
    #query_time = dtend - dtstart

    return {
        "rankings": pages.cur_page.object_list,
        "pages": pages,
        "klass": klass,
        "subject": subject,
        #"query_time": query_time, 
    }, template

@permission_required("exam.chart_subject_analyse")
@render_to("exam/chart_subject_analyse.html")
def chart_subject_analyse(request, subject_pk=None, template=None):
    subject = get_object_or_404(Subject, pk=subject_pk)
    return {
        "subject": subject,
    }, template

@permission_required("exam.chart_exam_analyse")
@render_to("exam/chart_exam_analyse.html")
def chart_exam_analyse(request, exam_pk=None, template=None):
    grade_pk = request.GET.get("grade_pk", None)
    exam = get_object_or_404(Exam, pk=exam_pk)
    return {
        "exam": exam,
        "grade_pk": grade_pk,
    }, template

@permission_required("exam.subject")
@render_to("exam/subject.html")
def subject(request, pk=None, template=None):
    subject = get_object_or_404(Subject, pk=pk)
    related_subject_list = subject.exam.subject_set.all()
    return {
        "subject": subject,
        "related_subject_list": related_subject_list,
    }, template

@login_required
@render_to("exam/chart_subject_class.html")
def chart_subject_class(request, template=None):
    """单科班级学生成绩分布图"""
    return {}, template

@permission_required("exam.add_result_by_room")
@csrf_exempt
@render_to("exam/add_result_by_room.html")
def add_result_by_room(request, template=None):
    """按照教室批量增加学生某一科目的成绩"""
    if request.method == "GET":
        exam_list = Exam.objects.all()
        try:
            current_exam = exam_list[0]
            subject_list = current_exam.subject_set.all()
            room_list = current_exam.room_set.all()
        except:
            return HttpResponse(u"数据还没有准备好")


    elif request.method == "POST":
        print request.POST
        subject_pk = request.POST.get("subject_pk", None)
        room_pk = request.POST.get("room_pk", None)
        for k in request.POST:
            if k.startswith("examinee_"):
                key, student_pk, klass_pk = k.rsplit("_")
                try:
                    score = Decimal(request.POST.get(k))
                except:
                    score = None
                try:
                    result = Result.objects.get(student=student_pk, subject = subject_pk)
                    result.score = score
                except:
                    result = Result(
                        student_id = student_pk,
                        klass_id = klass_pk,
                        subject_id = subject_pk,
                        score = score,
                        level = None,
                        creator = request.person,
                    )
                result.save()
        res = {
            "success": True,
        }
        return HttpResponse(json.dumps(res))

    return {
        "exam_list": exam_list,
        "subject_list": subject_list,
        "room_list": room_list,
    }, template


@login_required
@render_to("exam/room_list.html")
def room_list(request, template=None):
    """显示考室列表"""
    q = request.REQUEST.get("q","")
    page = request.REQUEST.get("page", 1)

    room_list = Room.objects.all()
    query = Q()
    if q:
        query = query & \
                (Q(examinee__uuid__icontains=q) | \
                 Q(examinee__name__icontains=q) | \
                 Q(examinee__username__icontains=q)
                )
        seat_list = Seat.objects.filter(query).values_list("room", flat=True)
        room_list = Room.objects.filter(pk__in=seat_list)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(room_list, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return {
        "room_list": pages.cur_page.object_list,
        "pages": pages,
        "q": q,
    }, template


@login_required
@render_to("exam/room.html")
def room(request, pk=None, template=None):
    """考室条目信息"""
    room = get_object_or_404(Room, pk=pk)
    related_room_list = room.exam.room_set.all()
    return {
        "room": room,
        "related_room_list": related_room_list,
    }, template

@login_required
@render_to("exam/class_seat_list.html")
def class_seat_list(request, template=None):
    exam_pk = request.GET.get("exam_pk", None)
    exam_list = Exam.objects.all()
    if exam_pk is None:
        current_exam = exam_list.latest("dtstart")
    else:
        current_exam = get_object_or_404(Exam, pk=exam_pk)

    class_pk_list = Seat.objects.filter(room__exam=current_exam).values_list("klass", flat=True).annotate()
    class_list = Class.objects.filter(pk__in=class_pk_list)

    return {
        "exam_list": exam_list,
        "class_list": class_list,
        "current_exam": current_exam,
    }, template

@login_required
@render_to("exam/class_seat.html")
def class_seat(request, template=None):
    klass_pk = request.GET.get("klass_pk", None)
    exam_pk = request.GET.get("exam_pk", None)
    klass = get_object_or_404(Class, pk=klass_pk)
    exam = get_object_or_404(Exam, pk=exam_pk)
    seat_list = Seat.objects.filter(klass=klass_pk, room__exam=exam_pk)

    class_pk_list = Seat.objects.filter(room__exam=exam).values_list("klass", flat=True).annotate()
    class_list = Class.objects.filter(pk__in=class_pk_list)

    return {
        "seat_list": seat_list,
        "class_list": class_list,
        "klass": klass,
        "exam": exam,
    }, template

@permission_required("exam.export_class_seat")
def export_class_seat(request):
    """导出某次考试的班级座位表"""
    klass_pk = request.GET.get("klass_pk", None)
    exam_pk = request.GET.get("exam_pk", None)
    if klass_pk:
        klass = get_object_or_404(Class, pk=klass_pk)
    exam = get_object_or_404(Exam, pk=exam_pk)

    #如果指定某个班，则下载指定班的座位表,否则就下载这次考试所有的班级座位列表
    if klass_pk is None:
        class_pk_list = Seat.objects.filter(room__exam=exam_pk).values_list("klass", flat=True).annotate()
        class_list = Class.objects.filter(pk__in=class_pk_list)
    else:
        class_list = Class.objects.filter(pk=klass_pk)

    from pyExcelerator import Workbook, Font, XFStyle, Alignment
    wb = Workbook()
    t_font, al, t_style, style = Font(), Alignment(), XFStyle(), XFStyle()
    t_font.bold = True
    t_font.height = 18*0x14
    t_style.font = t_font
    al.horz = Alignment.HORZ_CENTER
    t_style.alignment = al
    style.alignment = al

    for klass in class_list:
        ws = wb.add_sheet(klass.uuid)
        title = u"%(learning_year)s %(exam_name)s %(klass)s 试室座位表" % {
            "learning_year": exam.learning_year_verbose_name,
            "exam_name": exam.category.name,
            "klass": klass.name
        }
        ws.write_merge(0, 0, 0, 6, title, t_style)
        for k, v in enumerate([u"序号", u"班学号", u"姓名", u"性别", u"考室", u"座号", u"座位"]):
            ws.write(1, k, v, style)

        seat_list = Seat.objects.filter(klass=klass, room__exam=exam)
        for index, item in enumerate(seat_list):
            row = index + 2
            ws.write(row, 0, index + 1, style)
            ws.write(row, 1, item.classmate.uuid, style)
            ws.write(row, 2, item.examinee.name, style)
            ws.write(row, 3, item.examinee.gender.name, style)
            ws.write(row, 4, item.room.name, style)
            ws.write(row, 5, item.uuid, style)
            ws.write(row, 6, u"%s 行 %s 列" % (item.row, item.col), style)
    import tempfile
    tmpxls = tempfile.SpooledTemporaryFile()
    wb.save(tmpxls)
    tmpxls.seek(0)
    from utils.utils import send_file
    filename = u"%(learning_year)s %(exam_name)s 试室座位编排表.xls" % {
        "learning_year": exam.learning_year_verbose_name,
        "exam_name": exam.category.name,
    }
    return send_file(request, tmpxls, filename)
