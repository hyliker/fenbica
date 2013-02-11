#coding: utf-8
from decimal import Decimal
from django.db.models import Sum
from exam.models import Result
from classgrade.models import Class
from standard.models import GradeCode
from utils.utils import dotdict

class DecimalRanking(Decimal):
    pass
    #def __init__(self, decimal):
        #if decimal is None:
            #decimal = 0
        #super(DecimalRanking, self).__init__(self)

def class_sum_score_ranking(current_exam, class_pk):
    """返回某班的总分成绩排名字典"""
    #class_students = Class.objects.get(pk=class_pk).student_set.all()
    #exam_subject_class_student = Result.objects.filter(exam_subject__exam=current_exam.pk, exam_subject__grade=grade)
    exam_subject_class_student = Result.objects.filter(subject__exam=current_exam.pk, klass__in=[class_pk])
    class_students = exam_subject_class_student.values("student").annotate(Sum("score")).order_by("-score__sum")
    #assert False, class_students

    rankings = {}
    for index, student in enumerate(class_students):
        if index == 0:
            ranking = 1
        else:
            if student.get("score__sum") != pre_student.get("score__sum"):
                ranking = index + 1
        if student["score__sum"] is None:
            student["score__sum"] = 0
        sum_score = DecimalRanking(student["score__sum"])
        sum_score.ranking = ranking
        rankings[student["student"]] = sum_score
        pre_student = student
    return rankings

def grade_sum_score_ranking(current_exam, grade):
    exam_subject_grade_student = Result.objects.filter(subject__exam=current_exam.pk, subject__grade=grade)
    grade_students = exam_subject_grade_student.values("student").annotate(Sum("score")).order_by("-score__sum")

    students_grade_ranking = {}
    for index, student in enumerate(grade_students):
        if index == 0:
            ranking = 1
        else:
            if student.get("score__sum") != pre_student.get("score__sum"):
                ranking = index + 1

        students_grade_ranking[student["student"]] = ranking
        pre_student = student
    return students_grade_ranking

def score_ranking(students, score):

    """
    根据已经排序后的students的score分数项进行由高到低的名次排序
    并把排序所在結果保存在所有项的ranking所属里
    """
    #按部分并列名次排序有2种方式， 一种是[1,2,2,3,4,5], 一种是[1,2,2,4,5,6]
    # 如下students 列表是已经按分数由高低到低排好序的，如果不是，则要由高到低排序后再进行下面的处理
    # 排序方案按[10, 11, 11, 13, 14,14,15], 则产生的排名如下[1, 2, 2, 4, 5, 5, 7] 
    #for index, student in enumerate(students):
        #if index == 0:
            #class_ranking = 1
            #setattr(student, "class_ranking", class_ranking)
        #else:
            #if student.sum_score == pre_student.sum_score:
                #setattr(student, "class_ranking", class_ranking)
            #else:
                #class_ranking = index + 1
                #setattr(student, "class_ranking", class_ranking)
        #pre_student = student

    #def score_ranking(students, score):

        #class DecimalRanking(Decimal):
            #pass

        #"""
        #根据已经排序后的students的score分数项进行由高到低的名次排序
        #并把排序所在結果保存在所有项的ranking所属里
        #"""
        #for index, student in enumerate(students):
            #if index == 0:
                #ranking = 1
            #else:
                #if getattr(student, score) != getattr(pre_student,score):
                    #ranking = index + 1

            #_score = DecimalRanking(getattr(student, score))
            #_score.ranking = ranking
            #setattr(student, score, _score) 
            #pre_student = student
    for index, student in enumerate(students):
        if index == 0:
            ranking = 1
        else:
            if getattr(student, score) != getattr(pre_student,score):
                ranking = index + 1

        _score = DecimalRanking(getattr(student, score))
        _score.ranking = ranking
        setattr(student, score, _score) 
        pre_student = student


def calc_subject_excellent_rate(subject, classgrade):
    """计算优秀率"""
    e_fullscore = subject.full_score
    if isinstance(classgrade, GradeCode):
        e_result = subject.result_set.filter(klass__grade=classgrade)
    elif isinstance(classgrade, Class):
        e_result = subject.result_set.filter(klass=classgrade)
    totoal = e_result.count()
    e_excellent_score = str(e_fullscore * 0.9)
    e_excellent_num = e_result.filter(score__gte=e_excellent_score).count() 
    try:
        return float(e_excellent_num) / totoal * 100
    except ZeroDivisionError,e:
        return None
    #subject.stat["excellent"] = excellent * 100

def calc_subject_fine_rate(subject, classgrade):
    """计算良好率"""
    e_fullscore = subject.full_score
    if isinstance(classgrade, GradeCode):
        e_result = subject.result_set.filter(klass__grade=classgrade)
    elif isinstance(classgrade, Class):
        e_result = subject.result_set.filter(klass=classgrade)
    totoal = e_result.count()
    e_excellent_score = str(e_fullscore * 0.9)
    e_fine_score = str(e_fullscore * 0.8)
    e_fine_num = e_result.filter(score__lt=e_excellent_score, score__gte=e_fine_score).count() 
    try:
        return float(e_fine_num) / totoal * 100
    except ZeroDivisionError,e:
        return None
def calc_subject_pass_rate(subject, classgrade):
    """计算合格率"""
    e_fullscore = subject.full_score
    if isinstance(classgrade, GradeCode):
        e_result = subject.result_set.filter(klass__grade=classgrade)
    elif isinstance(classgrade, Class):
        e_result = subject.result_set.filter(klass=classgrade)
    totoal = e_result.count()
    e_fine_score = str(e_fullscore * 0.8)
    e_pass_score = str(e_fullscore * 0.6)
    e_pass_num = e_result.filter(score__lt=e_fine_score, score__gte=e_pass_score).count() 
    try:
        return float(e_pass_num) / totoal * 100
    except ZeroDivisionError,e:
        return None

def calc_subject_unpass_rate(subject, classgrade):
    """计算合格率"""
    e_fullscore = subject.full_score
    if isinstance(classgrade, GradeCode):
        e_result = subject.result_set.filter(klass__grade=classgrade)
    elif isinstance(classgrade, Class):
        e_result = subject.result_set.filter(klass=classgrade)
    totoal = e_result.count()
    e_unpass_score = str(e_fullscore * 0.6)
    e_unpass_num = e_result.filter(score__lt=e_unpass_score).count() 
    try:
        return float(e_unpass_num) / totoal * 100
    except ZeroDivisionError,e:
        return None

def analyse_score(result):
    """score为成绩对象"""
    full_score = result.subject.full_score
    excellent_score = full_score * Decimal('0.9')
    fine_score = full_score * Decimal('0.8')
    pass_score = full_score  * Decimal('0.6')
    score = result.score

    if score < pass_score:
        analysis = "unpass" 
    elif pass_score <= score < fine_score:
        analysis = "pass"
    elif fine_score <= score < excellent_score:
        analysis = "fine"
    elif excellent_score <= score <= full_score:
        analysis = "excellent"
    else:
        analysis = None
    return analysis

def calc_score_level(full_score, score):
    """分数成绩转化为等级成绩"""
    level_A = full_score * Decimal('0.9')
    level_B = full_score * Decimal('0.8')
    level_C = full_score  * Decimal('0.7')
    level_D =  full_score  * Decimal('0.6')

    if score < level_D:
        level = 'E'
    elif level_D <= score <  level_C:
        level = 'D'
    elif level_C <= score <  level_B:
        level = 'C'
    elif level_B <= score <= level_A:
        level = 'B'
    else:
        level = 'A'
    try:
        from standard.models import LevelScoreCode
        level = LevelScoreCode.objects.get(pk=level)
    except:
        level = None
    return level

def skip_ranking(element, ordered_list):
    """计划一个元素在顺序列表中的并列名次"""
    for index, item in enumerate(ordered_list):
        if index == 0:
            ranking = 1
        else:
            if item != pre_element:
                ranking = index + 1
        if item == element:
            return ranking
        pre_element = item 
