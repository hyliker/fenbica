#coding: utf-8
import operator
import json
import datetime
from collections import defaultdict
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from exam.models import Exam, Subject, Result
from django.core import serializers
from classgrade.models import Class
from person.models import Person
from django.db.models import Count
from classgrade.models import Classmate 
from django.db.models import Q
from exam.models import Room, Subject
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required
def get_exam_grade_list(request, exam_pk=None):
    try:
        exam = Exam.objects.get(pk=exam_pk)
    except:
        exam = None
    grade_list = Class.objects.filter(dtcreated__year=exam.learning_year[:4]).values("grade", "grade__name").annotate(klass_num=Count("uuid"))

    for g in grade_list:
        grade_uuid = "%(year)s%(grade)s" % {"year": exam.learning_year[0:4], "grade": g["grade"] } 
        grade_student_num = Classmate.objects.filter(klass__uuid__startswith=grade_uuid).count()
        g["student_num"] = grade_student_num
    print "grade_list", grade_list

    res = json.dumps({
        "success": True,
        "data": list(grade_list),
    })
    return HttpResponse(res)

@login_required
def get_exam_subjects_by_exam(request, exam_pk=None):
    """获取某一次考试的科目"""
    exam = get_object_or_404(Exam, pk=exam_pk)
    exam_subjects = exam.subject_set.all().values("id", "grade__name", "category__name", "full_score")
    print exam_subjects
    json_res = json.dumps({
        "success": True,
        "data": list(exam_subjects)
    })
    return HttpResponse(json_res)

@login_required
def get_exam_room_list_by_exam(request, exam_pk=None):
    """获取某一次考试的试室列表"""
    exam = get_object_or_404(Exam, pk=exam_pk)
    room_list = exam.room_set.all().values("id", "name", "grade__name")
    print room_list
    json_res = json.dumps({
        "success": True,
        "data": list(room_list),
    })
    return HttpResponse(json_res)

@login_required
def get_exam_room_list_by_subject(request, subject_pk=None):
    """获取某一次考试的试室列表"""
    subject = get_object_or_404(Subject, pk=subject_pk)
    room_list = subject.exam.room_set.filter(grade=subject.grade).values("id", "name", "grade__name")
    print room_list
    json_res = json.dumps({
        "success": True,
        "data": list(room_list),
    })
    return HttpResponse(json_res)

@login_required
def get_seat_list_by_room(request, room_pk=None):
    """获取某一教室的考生列表"""
    room = get_object_or_404(Room, pk=room_pk)

    seat_list = list(room.seat_set.values("examinee", "klass", "klass__uuid", "uuid", "examinee__uuid", "examinee__name", "examinee__gender__name"))
    seat_list.sort(key=lambda s: int(s["uuid"]))
    examinee_list = room.seat_set.values_list("examinee", flat=True)

    #如果有考试科目， 则返回相应的已经录入的科目成绩
    subject_pk = request.GET.get("subject_pk", None)
    if subject_pk:
        result_list = Result.objects.filter(subject=subject_pk, student__in=examinee_list).values_list("student", "score")
        result_dict = dict(result_list)

        for seat in seat_list:
            score = result_dict.get(seat.get("examinee", None))
            if score is None:
                score = ""
            else:
                score = float(score)
            seat["score"] = score

    json_res = json.dumps({
        "success": True,
        "data": list(seat_list),
    })

    return HttpResponse(json_res)

@login_required
def get_exam_subject_classgrade(request):
    exam_subject_pk = request.GET.get("exam_subject_pk", None)
    exam_subject = get_object_or_404(Subject, pk=exam_subject_pk)
    classgrade = Class.objects.filter(dtcreated__year=exam_subject.exam.learning_year[:4], grade=exam_subject.grade).values("pk", "name")
    print classgrade
    json_res = json.dumps({
        "success": True,
        "data": list(classgrade)
    })
    return HttpResponse(json_res)

@login_required
def get_exam_subject_students(request):
    klass_pk = request.GET.get("klass_pk", None)
    exam_subject_pk = request.GET.get("exam_subject_pk", None)


    classgrade = get_object_or_404(Class, pk=klass_pk)
    students = classgrade.classmate_set.filter().values("student", "uuid", "student__name", "student__gender__name")
    students_pks = [s["student"] for s in students]

    student_exam_results = Result.objects.filter(subject=exam_subject_pk, student__in=students_pks).values_list("student", "score")
    student_exam_results_dict = dict(student_exam_results)
    #print students_pks,student_exam_results, student_exam_results_dict

    for s in students:
        score = student_exam_results_dict.get(s["student"], "")
        if score is None:
            s["score"] = ""
        else:
            s["score"] = str(score)

    json_res = json.dumps({
        "success": True,
        "data": list(students),
    })
    return HttpResponse(json_res)

@login_required
def get_exam_room_list(request, exam_pk=None):
    """获取某一次考试的试室列表"""
    exam = get_object_or_404(Exam, pk=exam_pk)
    room_list = exam.room_set.values("name", "pk", "grade__name", "grade")
    from django.core import serializers
    #room_list = serializers.serialize("python", room_list, fields=("name", "pk", "grade"))
    #room_list = serializers.serialize("python", room_list)
    res = json.dumps({
        "success": True,
        "data": list(room_list),
    })
    return HttpResponse(res)

def generate_colors(nsize):
    """返回nsize种不同的颜色"""
    import colorsys
    rgb_list = [colorsys.hsv_to_rgb(x*1.0/nsize, 1, 0.5) for x in range(nsize)]
    html_rgb_list = [ (r*255,g*255,b*255) for r,g,b in rgb_list]
    hex_list = ["%02x%02x%02x" % x for x in html_rgb_list]
    return hex_list

@login_required
def chart_student_analyse(request, student_pk=None):
    """某个学生的考试成绩汇总分析"""
    from student.models import Student
    from collections import defaultdict
    from exam.models import Result
    student = get_object_or_404(Student, pk=student_pk)
    result_list = Result.objects.filter(student=student)
    subject_name_list = result_list.values_list("subject__category__name", flat=True).annotate()
    subject_list = defaultdict(list)

    grade_ranking_list = []
    for r in result_list:
        grade_ranking_list.append(r.grade_ranking)
        subject_list[r.subject.category.name].append(r.grade_ranking)

    min_grade_ranking = min(grade_ranking_list)
    max_grade_ranking = max(grade_ranking_list)

    import colorsys
    n_color = len(subject_name_list)
    rgb_tuples = [colorsys.hsv_to_rgb(x*1.0/n_color, 1, 0.5) for x in range(n_color)]
    html_rgb_list = [ (r*255,g*255,b*255) for r,g,b in rgb_tuples]
    hex_list = ["%02x%02x%02x" % x for x in html_rgb_list]

    chart_title = u"%s 学生 历年考试成绩各科年级排名汇总分析图表" % student.name

    data = {
        "elements": [],
        "y_axis": {"min": max_grade_ranking + 10, "max": min_grade_ranking - 10, "steps": (max_grade_ranking - min_grade_ranking)/len(subject_name_list)},
        "title": { "text": chart_title, "style": "font-size:20px" },
    }

    for k, v in subject_list.items():
        data["elements"].append({
            "type": "scatter_line", 
            "width": 10,
            "text": k,
            "dot-style": {"type": "solid-dot","tip": u"%s #val#" % k },
            "colour": hex_list.pop(),
            "values": [{"x": k, "y": v} for k,v in enumerate(v)],
        })
    return HttpResponse(json.dumps(data), mimetype="application/json")


@login_required
def chart_data_subject_analyse(request, subject_pk=None):
    """分析某一考试科目的学生成绩图表"""
    from exam.models import Subject
    subject = get_object_or_404(Subject, pk=subject_pk)
    result_list =subject.result_set.values_list("score", flat=True).order_by("-score")
    chart_values_list = [int(r) for r in result_list if r is not None]

    if chart_values_list:
        y_axis_min = min(chart_values_list)
        y_axis_max = max(chart_values_list)
    else:
        return HttpResponse(u"数据还没有准备好")

    chart_title = u"%s 分析图表" % subject

    data = {
        "elements": [{
            "type": "area", 
            "width": 2,
            "colour": "#838A96",
            "fill": "#E01B49",
            "fill-alpha": 0.4,
            "values": chart_values_list,
            "dot-style": {"type": "dot","tip": u"分数:#val#, 序号:#x#" },
        }],
        "y_axis": {"min": y_axis_min, "max": y_axis_max, "steps": 10},
        "x_axis": {"min": 0, "max": len(chart_values_list), "steps": 50},
        "title": { "text": chart_title, "style": "font-size:20px" },
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")

#@login_required
def chart_data_exam_analyse(request, exam_pk=None):
    """分析某一考试科目的学生成绩图表"""
    from exam.models import Exam, Result
    from standard.models import GradeCode
    grade_pk = request.GET.get("grade_pk", None)
    exam = get_object_or_404(Exam, pk=exam_pk)
    subject_list = []
    query = Q()
    if grade_pk:
        grade = get_object_or_404(GradeCode, pk=grade_pk)
        query = query & Q(grade=grade)
        chart_title = u"%s %s 各科成绩分布图表" % (exam, grade.name)
    else:
        chart_title = u"%s 全年级 各科成绩分布图表" % exam

    subject_result_num_list = []
    for subject in exam.subject_set.filter(query):
        full_score = subject.full_score
        result_list =subject.result_set.values_list("score", flat=True).order_by("-score")
        chart_values_list = [int(r*100/full_score) for r in result_list if r is not None]
        subject_info = {
            "grade": subject.grade,
            "name": subject.category.name,
            "data": chart_values_list
        }
        subject_list.append(subject_info)
        subject_result_num_list.append(result_list.count())

    chart_data = {
        "elements": [],
        "y_axis": {"min": 0, "max": 120, "steps": 10},
        "x_axis": {"min": 0, "max": max(subject_result_num_list) + 10, "steps": 50},
        "title": { "text": chart_title, "style": "font-size:20px" },
    }

    color_list = generate_colors(len(subject_list))

    for subject in subject_list:
        if grade_pk:
            text = subject["name"]
            tip = u"%s 分数:#val#, 序号:#x#" % subject["name"] 
        else:
            text = u"%s %s" % (subject["grade"], subject["name"])
            tip = u"%s %s 分数:#val#, 序号:#x#" % (subject["grade"], subject["name"])
        element = {
            "type": "line", 
            "width": 5,
            "colour": "#838A96",
            "fill": "#E01B49",
            "fill-alpha": 0.4,
            "text": text,
            "values": [{"x": k, "y": v} for k,v in enumerate(subject["data"])],
            "colour": color_list.pop(),
            "dot-style": {"type": "dot","tip": tip},
        }
        chart_data["elements"].append(element)

    return HttpResponse(json.dumps(chart_data), mimetype="application/json")

@login_required
def chart_data_subject_class_analyse(request, subject_pk=None):
    """分析某一考试科目各班级学生成绩图表"""
    from exam.models import Subject
    subject = get_object_or_404(Subject, pk=subject_pk)
    result_list =subject.result_set.all()
    klass_list =result_list.values_list("klass", flat=True).annotate()
    result_list_num = result_list.count()

    if not result_list:
        return HttpResponse(u"数据还没有准备好")
    max_klass_rlist_num = max(result_list.values("klass").annotate(Count("score")).values_list("score__count", flat=True))

    color_list = generate_colors(len(klass_list))

    score_list = []
    chart_element_list = []
    for k in klass_list:
        rlist =result_list.filter(klass=k).values_list("score", flat=True).order_by("-score")
        vlist = [int(r) for r in rlist if r is not None]
        color = color_list.pop()
        element = {
            "type": "line", 
            "width": 5,
            "colour": color,
            "fill": color,
            "fill-alpha": 0.4,
            "text": u"%s 班" % k,
            "values": vlist,
            "dot-style": {"type": "dot","tip": u"%s 班 分数:#val#, 序号:#x#" % k },
        }
        chart_element_list.append(element)

    chart_title = u"%s %s 分析图表" % (subject.exam, subject.category.name)

    data = {
        "y_axis": {"min": 0, "max": int(subject.full_score), "steps": 10},
        "x_axis": {"min": 0, "max": max_klass_rlist_num, "steps": 10},
        "title": { "text": chart_title, "style": "font-size:20px" },
    }
    data["elements"] = chart_element_list
    return HttpResponse(json.dumps(data), mimetype="application/json")
