#!/usr/bin/env python
#coding: utf-8

from datetime import datetime
import time

import os, sys
if os.path.basename(os.getcwd()) == 'tools':
    os.chdir('..')
from django.core.management import setup_environ
sys.path.append( os.getcwd() )
import settings
setup_environ(settings)

from staff.models import Staff
from student.models import Student
from person.models import Person
from django.contrib.auth.models import User
from pyExcelerator import parse_xls
from standard.models import GenderCode, DiplomaCode
import hzpy
import yaml

def import_location_code(file_path="tools/codeset/location.xls", sheet_number=0):
    from standard.models import LocationCode
    """行政区划码"""
    print "locationCode"
    LocationCode.objects.all().delete()
    cell_mapping = {
            "name": 0, #名称
            "pinyin":1, #罗马拼音
            "code": 2, #代码
            "letter_code":3, #字母
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(8, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    location = LocationCode(
                            name = sheet.get((r, cell_mapping["name"]),""),
                            pinyin = sheet.get((r, cell_mapping["pinyin"]),""),
                            code = sheet.get((r, cell_mapping["code"]),""),
                            letter_code = sheet.get((r, cell_mapping["letter_code"]),""),
                            )
                    location.save()
                    print location, location.name, location.pinyin, location.code , location.letter_code
                break
            except KeyError, e:
                print e

def import_folk_code(file_path="tools/codeset/folk.xls", sheet_number=0):
    from standard.models import FolkCode
    """民族码"""
    print "folk_code"
    FolkCode.objects.all().delete()
    cell_mapping = {
            "name": 0, #名称
            "pinyin": 1, #拼音名称
            "letter_code": 2, #字母代码
            "code": 3, #代码
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(1, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = FolkCode(
                            name = sheet.get((r, cell_mapping["name"]),""),
                            code = sheet.get((r, cell_mapping["code"]),""),
                            letter_code = sheet.get((r, cell_mapping["letter_code"]),""),
                            pinyin = sheet.get((r, cell_mapping["pinyin"]),""),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_grade_code(file_path="tools/codeset/grade.xls", sheet_number=0):
    from standard.models import GradeCode as Obj
    Obj.objects.all().delete()
    """年级代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_teaching_mode_code(file_path="tools/codeset/teachingMode.xls", sheet_number=0):
    from standard.models import TeachingModeCode as Obj
    Obj.objects.all().delete()
    """授课方式代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_semester_code(file_path="tools/codeset/semester.xls", sheet_number=0):
    from standard.models import SemesterCode as Obj
    Obj.objects.all().delete()
    """学期代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_exam_mode_code(file_path="tools/codeset/examMode.xls", sheet_number=0):
    from standard.models import ExamModeCode as Obj
    Obj.objects.all().delete()
    """考试方式码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_exam_type_code(file_path="tools/codeset/examType.xls", sheet_number=0):
    from standard.models import ExamTypeCode as Obj
    Obj.objects.all().delete()
    """考试类型码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_level_score_code(file_path="tools/codeset/levelScore.xls", sheet_number=0):
    from standard.models import LevelScoreCode as Obj
    Obj.objects.all().delete()
    """考试等级成绩代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_rewards_type_code(file_path="tools/codeset/rewardsType.xls", sheet_number=0):
    from standard.models import RewardsTypeCode as Obj
    Obj.objects.all().delete()
    """学生获奖类别代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_rewards_level_code(file_path="tools/codeset/rewardsLevel.xls", sheet_number=0):
    from standard.models import RewardsLevelCode as Obj
    Obj.objects.all().delete()
    """学生获奖级别代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_punishment_name_code(file_path="tools/codeset/punishmentName.xls", sheet_number=0):
    from standard.models import PunishmentNameCode as Obj
    Obj.objects.all().delete()
    """处分名称代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_enrollment_type_code(file_path="tools/codeset/enrollmentType.xls", sheet_number=0):
    from standard.models import EnrollmentTypeCode as Obj
    Obj.objects.all().delete()
    """入学方式代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_attendance_type_code(file_path="tools/codeset/attendanceType.xls", sheet_number=0):
    from standard.models import AttendanceTypeCode as Obj
    Obj.objects.all().delete()
    """就读方式代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_source_type_code(file_path="tools/codeset/sourceType.xls", sheet_number=0):
    from standard.models import SourceTypeCode as Obj
    Obj.objects.all().delete()
    """就读方式代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_graduate_direction_code(file_path="tools/codeset/graduateDirection.xls", sheet_number=0):
    from standard.models import GraduateDirectionCode as Obj
    Obj.objects.all().delete()
    """毕业去向代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_education_result_code(file_path="tools/codeset/educationResult.xls", sheet_number=0):
    from standard.models import EducationResultCode as Obj
    Obj.objects.all().delete()
    """教育結果代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_transfer_type_code(file_path="tools/codeset/transferType.xls", sheet_number=0):
    from standard.models import TransferTypeCode as Obj
    Obj.objects.all().delete()
    """学籍异动代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_transfer_status_code(file_path="tools/codeset/transferStatus.xls", sheet_number=0):
    from standard.models import TransferStatusCode as Obj
    Obj.objects.all().delete()
    """学籍异动处理状态代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_occupation_code(file_path="tools/codeset/occupation.xls", sheet_number=0):
    from standard.models import OccupationCode as Obj
    Obj.objects.all().delete()
    """职业分类代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_teaching_type_code(file_path="tools/codeset/teachingType.xls", sheet_number=0):
    from standard.models import TeachingTypeCode as Obj
    Obj.objects.all().delete()
    """教学类型码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_teaching_role_code(file_path="tools/codeset/teachingRole.xls", sheet_number=0):
    from standard.models import TeachingRoleCode as Obj
    Obj.objects.all().delete()
    """任课角色类型码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_learning_stage_code(file_path="tools/codeset/learningStage.xls", sheet_number=0):
    from standard.models import LearningStageCode as Obj
    Obj.objects.all().delete()
    """学段代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_singleton_code(file_path="tools/codeset/singleton.xls", sheet_number=0):
    from standard.models import SingletonCode as Obj
    Obj.objects.all().delete()
    """独生子女代码 """
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_domicle_type_code(file_path="tools/codeset/domicleType.xls", sheet_number=0):
    from standard.models import DomicleTypeCode as Obj
    Obj.objects.all().delete()
    """户口性质代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_social_job_code(file_path="tools/codeset/socialJob.xls", sheet_number=0):
    from standard.models import SocialJobCode as Obj
    Obj.objects.all().delete()
    """社会兼职代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if len(unicode(sheet.get((r, cell_mapping["code"]))).strip())>1:
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_technical_post_code(file_path="tools/codeset/technicalPost.xls", sheet_number=0):
    from standard.models import TechnicalPostCode as Obj
    Obj.objects.all().delete()
    """专业技术职务"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if len(unicode(sheet.get((r, cell_mapping["code"])))) == 3:
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_cadre_post_code(file_path="tools/codeset/cadrePost.xls", sheet_number=0):
    from standard.models import CadrePostCode as Obj
    Obj.objects.all().delete()
    """干部职务"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if len(unicode(sheet.get((r, cell_mapping["code"])))) == 4:
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_cadre_post_level_code(file_path="tools/codeset/cadrePostLevel.xls", sheet_number=0):
    from standard.models import CadrePostLevelCode as Obj
    Obj.objects.all().delete()
    """干部职务级别"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if len(unicode(sheet.get((r, cell_mapping["code"])))) == 2:
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_relation_code(file_path="tools/codeset/relation.xls", sheet_number=0):
    from standard.models import RelationCode as Obj
    Obj.objects.all().delete()
    """家庭关系码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_learning_mode_code(file_path="tools/codeset/learningMode.xls", sheet_number=0):
    from standard.models import LearningModeCode as Obj
    Obj.objects.all().delete()
    """学习形式"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_learning_way_code(file_path="tools/codeset/learningWay.xls", sheet_number=0):
    from standard.models import LearningWayCode as Obj
    Obj.objects.all().delete()
    """学习方式"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e



def import_degree_code(file_path="tools/codeset/degree.xls", sheet_number=0):
    from standard.models import DegreeCode
    DegreeCode.objects.all().delete()
    """学位代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = DegreeCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_location_folk_code(file_path="tools/codeset/locationFolk.xls", sheet_number=0):
    from standard.models import LocationFolkCode
    LocationFolkCode.objects.all().delete()
    """地区民族属性码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = LocationFolkCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_location_type_code(file_path="tools/codeset/locationType.xls", sheet_number=0):
    from standard.models import LocationTypeCode
    LocationTypeCode.objects.all().delete()
    """地区类别码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = LocationTypeCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_location_econ_code(file_path="tools/codeset/locationEcon.xls", sheet_number=0):
    from standard.models import LocationEconCode
    LocationEconCode.objects.all().delete()
    """地区经济属性码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = LocationEconCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_floating_code(file_path="tools/codeset/floating.xls", sheet_number=0):
    from standard.models import FloatingCode
    FloatingCode.objects.all().delete()
    """流动人口"""
    print "流动人口"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if str(sheet.get((r, cell_mapping["code"]))):
                    obj = FloatingCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_gender_code(file_path="tools/codeset/gender.xls", sheet_number=0):
    from standard.models import GenderCode
    GenderCode.objects.all().delete()
    """性别码"""
    print "性别码"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = GenderCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_diploma_code(file_path="tools/codeset/diploma.xls", sheet_number=0):
    from standard.models import DiplomaCode
    DiplomaCode.objects.all().delete()
    """文化程度"""
    print "diploma"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = DiplomaCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_staff_type_code(file_path="tools/codeset/staffType.xls", sheet_number=0):
    from standard.models import StaffTypeCode
    StaffTypeCode.objects.all().delete()
    """员工编制类型"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = StaffTypeCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_school_type_code(file_path="tools/codeset/schoolType.xls", sheet_number=0):
    from standard.models import SchoolTypeCode
    """学校类别"""
    print "schooltype"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    SchoolTypeCode.objects.all().delete()
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = SchoolTypeCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_class_type_code(file_path="tools/codeset/classType.xls", sheet_number=0):
    from standard.models import ClassTypeCode
    """班级类别"""
    print "classtype"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    ClassTypeCode.objects.all().delete()
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = ClassTypeCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_student_type_code(file_path="tools/codeset/studentType.xls", sheet_number=0):
    from standard.models import StudentTypeCode
    """学生类别码"""
    print "student type"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    StudentTypeCode.objects.all().delete()
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = StudentTypeCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_blood_type_code(file_path="tools/codeset/bloodType.xls", sheet_number=0):
    from standard.models import BloodTypeCode
    """血型代码"""
    print "post_occupation"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    BloodTypeCode.objects.all().delete()
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = BloodTypeCode(
                            name = sheet.get((r, cell_mapping["name"]),""),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_health_code(file_path="tools/codeset/health.xls", sheet_number=0):
    from standard.models import HealthCode
    """健康代码"""
    print "post_occupation"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(6, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = HealthCode(
                            name = sheet.get((r, cell_mapping["name"]),""),
                            code = sheet.get((r, cell_mapping["code"]),""),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_marriage_code(file_path="tools/codeset/marriage.xls", sheet_number=0):
    from standard.models import MarriageCode
    MarriageCode.objects.all().delete()
    """婚姻状况"""
    print "post_occupation"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = MarriageCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_emigrant_code(file_path="tools/codeset/emigrant.xls", sheet_number=0):
    from standard.models import EmigrantCode
    """港台码"""
    print "post_occupation"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = EmigrantCode(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_post_occupation_code(file_path="tools/codeset/postOccupation.xls", sheet_number=0):
    from standard.models import PostOccupationCode
    """岗位职业码"""
    print "post_occupation"
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(2, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    post_occupation = PostOccupationCode(
                            name = sheet.get((r, cell_mapping["name"]),""),
                            code = sheet.get((r, cell_mapping["code"]),""),
                            )
                    post_occupation.save()
                    print post_occupation.code, post_occupation.name
                break
            except KeyError, e:
                print e

def import_nationality_code(file_path="tools/codeset/nationality.xls", sheet_number=0):
    from standard.models import NationalityCode
    """国家代码"""
    cell_mapping = {
            "code": 1, #代码
            "name": 0, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(5, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = NationalityCode(
                            name = sheet.get((r, cell_mapping["name"]),""),
                            code = sheet.get((r, cell_mapping["code"]),""),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_politics_code(file_path="tools/codeset/politics.xls", sheet_number=0):
    from standard.models import PoliticsCode
    """政治面貌"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(6, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if sheet.get((r, cell_mapping["code"])):
                    obj = PoliticsCode(
                            name = sheet.get((r, cell_mapping["name"]),""),
                            code = sheet.get((r, cell_mapping["code"]),""),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def id_number2birthday(id_number):
    """身份证号码转换到出身日期"""
    #id_number = "441202197612027318"
    birthday_str = id_number[6:14]
    birthday = datetime.strptime(birthday_str, "%Y%m%d")
    return birthday

def import_student(file_path, sheet_number):
    """把指定格式的excel数据导入到数据库"""
    cell_mapping = {
            "name": 1,
            "id_number": 6,
            "birthday":3,         
            "gender": 2,
            "telephone": 7,
            "domicle_location": 8,
            "postal_address": 10,
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    #print rows, cols
    for r in range(1, rows+1):
        for c in range(cols+1):
            name = sheet[(r, cell_mapping["name"])]
            username = hzpy.hz2py(name)
            try:
                id_number = sheet[(r, cell_mapping["id_number"])]
            except:
                id_number = ""
            try:
                gender = sheet[(r, cell_mapping["gender"])]
            except KeyError, e:
                gender=u"未知的性别"
            email = "%s@pingni.com" % username
            try:
                birth_date = id_number2birthday(id_number)
            except:
                birth_date = None
            password = "dir"#id_number[6:14]
            #print "excel: ", username
            exist_user_count = User.objects.filter(username__exact=username).count()
            #print exist_user_count
            if exist_user_count > 0:
                username = username + str(exist_user_count + 1)


            #p = user.get_profile()
            #p.name = name
            #p.gender=GenderCode.objects.get(name=gender)
            #p.identity = "School.Student"
            #p.identity_group = school.pk
            #p.gender=GenderCode.objects.get(name=gender)
            #p.save()

            #student.name = name
            #student.gender = GenderCode.objects.get(name=gender)
            #student.identity = student.IDENTITY_STUDENT

            if len(id_number) > 18:
                id_number = ""

            telephone = str(sheet.get((r, cell_mapping["telephone"]), "")).split(".")[0]
            try:
                domicle_location = sheet.get((r, cell_mapping["domicle_location"]), "")
                print domicle_location
            except Exception,e:
                print e
            else:
                domicle_location = domicle_location
            postal_address = sheet.get((r, cell_mapping["postal_address"]), "")

            student = Student(
                username=username,
                email=email,
                password=password,
                spell_name=username,
                identity=Person.IDENTITY_STUDENT,
                gender=GenderCode.objects.get(name=gender),
                id_no=id_number,
                birthday=birth_date,
                telephone=telephone,
                domicle_location=domicle_location,
                postal_address=postal_address,
                name=name,
            )
            student.set_password(password)
            student.save()

            #print id_number
            #student_profile = Student(
                    #school = school,
                    #profile = p,
                    #name = name,
                    #id_no =id_number,
                    #gender=GenderCode.objects.get(name=gender),
                    #spell_name = username,
                    #birthday = birth_date,
                    #telephone = str(sheet.get((r, cell_mapping["telephone"]), "")).split(".")[0],
                    #domicle_location = sheet.get((r, cell_mapping["domicle_location"]), ""),
                    #postal_address = sheet.get((r, cell_mapping["postal_address"]), ""),
                    #)
            #student_profile.save()
            break

def import_staff(file_path, sheet_number):
    """把指定格式的excel数据导入到数据库"""
    cell_mapping = {
            u"name": 2, #u"姓名") 
            u"id_number": 1, #u"身份证号码"):
            #u"id_type": 1, #,u"身份证明类型")
            u"gender": 6, #u"性别"): 6,
            #u"social_insurance_number":1 # u"个人社保号码"): 1,
            u"work_date": 9, # u"参加工作时间"): 9,
            u"technical_title": 11, #, u"技术职称"): 12,
            u"birth_date": 8, # u"出身日期"): 8,
            #u"job_status": 1, # u"工作状态"): 1,
            u"diploma": 7, # u"学历"): 7,
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(1, rows+1):
        for c in range(cols+1):
            try:
                #print sheet[(r,c)]
                name = sheet[(r, cell_mapping["name"])]
                username = hzpy.hz2py(name)
                id_number = sheet[(r, cell_mapping["id_number"])]
                try:
                    gender = sheet[(r, cell_mapping["gender"])]
                except KeyError, e:
                    gender=u"未知的性别"
                #technical_title = sheet[(r, cell_mapping["technical_title"])]
                #job_status = sheet[(r, cell_mapping["job_status"])]
                #diploma = sheet[(r, cell_mapping["diploma"])]
                email = "%s@pingni.com" % username
                birth_date = id_number2birthday(id_number)
                #password = id_number[6:14]
                password = "dir"
                print username, id_number, gender#, technical_title, diploma, email
                exist_user_count = User.objects.filter(username = username).count()
                if exist_user_count > 0:
                    username = username + str(exist_user_count + 1)
                staff = Staff(
                    username=username,
                    email = email,
                    name=name,
                    password=password,
                    identity= Staff.IDENTITY_STAFF,
                    gender = GenderCode.objects.get(name=gender),
                    id_no = id_number,
                    spell_name = username,
                    birthday = birth_date
                )
                #staff.save()
                staff.set_password(password)
                staff.save()
                #user = User.objects.create_user(username, email, password)

                #user.person.identity = staff.IDENTITY_STAFF
                #person = user.person.save()

                #person.staff.name = name
                #person.staff.gender=GenderCode.objects.get(name=gender)

                #person.staff.id_no = id_number
                #person.staff.spell_name = username
                #person.staff.birthday = birth_date
                #person.staff.save()

                #user.person.staff.name = name
                #user.person.staff.gender=GenderCode.objects.get(name=gender)

                #user.person.staff.id_no = id_number
                #user.person.staff.spell_name = username
                #user.person.staff.birthday = birth_date
                #user.person.staff.save()

                #staff = Staff(user=user, school=school)
                #staff.save()


                #user.first_name = name[1:] #名字
                #user.last_name = name[0] #姓氏
                #person, new = Person.objects.get_or_create(person=user.person)
                #staff_profile = Staff(
                        #school = school,
                        #name = name,
                        #id_no =id_number,
                        ##id_type = u"身份证",
                        #gender=GenderCode.objects.get(name=gender),
                        #spell_name = username,
                        ##technical_title = technical_title,
                        ##diploma = diploma,
                        #birthday = birth_date,
                        #)
                #staff_profile.save()
                break
            except KeyError, e:
                print e


#def import_exam():
    #"""初始化考试相关的数据"""
    #from exam.models import StudentExamName
    #from school.models import School
    #from datetime import datetime
    #COURSE_CHOICES = [ u"语文", u"数学", u"英语", u"物理", u"历史", u"地理", u"生物", u"体育", u"音乐", u"美术", u"信息技术"]
    #school = School.objects.get(code=u"441721001")
    #for year in range(2000, 2010):
        #dtstart = datetime.now()
        #exam = StudentExamName(
            #dtstart = dtstart,
            #name = u"%s 年期中考试" % year,
            #school = school
        #)
        #exam.save()

def import_room_usage_code(file_path="tools/codeset/roomUsage.xls", sheet_number=0):
    from standard.models import RoomUsageCode as Obj
    Obj.objects.all().delete()
    """学期代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_teaching_use_property_code(file_path="tools/codeset/TeachingUseProperty.xls", sheet_number=0):
    from standard.models import TeachingUsePropertyCode as Obj
    Obj.objects.all().delete()
    """学期代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_school_unit_level_code(file_path="tools/codeset/schoolUnitLevel.xls", sheet_number=0):
    from standard.models import SchoolUnitLevelCode as Obj
    Obj.objects.all().delete()
    """学期代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_building_category_code(file_path="tools/codeset/buildingCategory.xls", sheet_number=0):
    from standard.models import BuildingCategoryCode as Obj
    Obj.objects.all().delete()
    """学期代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_building_structrue_code(file_path="tools/codeset/buildingStructure.xls", sheet_number=0):
    from standard.models import BuildingStructureCode as Obj
    Obj.objects.all().delete()
    """学期代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_funding_source_code(file_path="tools/codeset/fundingSource.xls", sheet_number=0):
    from standard.models import FundingSourceCode as Obj
    Obj.objects.all().delete()
    """学期代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def import_building_status_code(file_path="tools/codeset/buildingStatus.xls", sheet_number=0):
    from standard.models import BuildingStatusCode as Obj
    Obj.objects.all().delete()
    """学期代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e

def import_property_usage_code(file_path="tools/codeset/propertyUsage.xls", sheet_number=0):
    from standard.models import PropertyUsageCode as Obj
    Obj.objects.all().delete()
    """学期代码"""
    cell_mapping = {
            "code": 0, #代码
            "name": 1, #名称
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(0, rows+1):
        for c in range(cols+1):
            try:
                #time.sleep(1)
                #print sheet[(r,c)], sheet[(r,c+1)], sheet[(r,c+2)], sheet[(r, c+3)]
                if unicode(sheet.get((r, cell_mapping["code"]))):
                    obj = Obj(
                            name = sheet.get((r, cell_mapping["name"]),"").strip(),
                            code = unicode(sheet.get((r, cell_mapping["code"]),"")).strip(),
                            )
                    obj.save()
                    print obj.code, obj.name
                break
            except KeyError, e:
                print e


def generate_classgrade():
    """初始化兴华中学的班级, 以便导入学生档案的时候进行绑定"""
    from classgrade.models import Class
    from standard.models import GradeCode, ClassTypeCode
    import datetime
    #初三有11个班, 初一有10个班， 初二有10个班
    dtcreated = datetime.date(2010, 9, 1)
    classgrade_mapping = (
        #(grade, classnum, classname),
        (31, 10, u"初一"), 
        (32, 10, u"初二"),
        (33, 11, u"初三"),
    )

    for grade, classnum, classname in classgrade_mapping:
        for index in range(classnum):
            sn = str(index + 1).zfill(2)
            uuid = u"%s%s%s" % (dtcreated.year, grade, sn)
            name = u"%s%s班" % (classname, index + 1)
            print sn, uuid, name
            try:
                new_class = Class.objects.create(
                    grade = GradeCode.objects.get(pk=grade), 
                    dtcreated = dtcreated,
                    uuid = uuid, 
                    name = name,
                    type= ClassTypeCode.objects.get(pk=20), 
                )
            except:
                pass
            else:
                print new_class    


#http://stackoverflow.com/questions/1108428/how-do-i-read-a-date-in-excel-format-in-python
def minimalist_xldate_as_datetime(xldate, datemode):
    import datetime
    # datemode: 0 for 1900-based, 1 for 1904-based
    return (
        datetime.datetime(1899, 12, 30)
        + datetime.timedelta(days=xldate + 1462 * datemode)
        )

def import_data_staff(file_path, sheet_number):
    """把指定格式的excel数据导入到数据库"""
    cell_mapping = {
            u"name": 1, #u"姓名") 
            u"id_number": 2, #u"身份证号码"):
            u"gender": 3, #u"性别"): 6,
            #u"technical_title": 11, #, u"技术职称"): 12,
            u"birth_date": 4, # u"出身日期"): 8,
            u"dtenroll": 6, # u"入校日期"): 6,
            #u"job_status": 1, # u"工作状态"): 1,
            u"diploma": 5, # u"学历"): 7,
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])
    print rows, cols
    for r in range(30, rows+1):
        for c in range(cols+1):
            try:
                #print sheet[(r,c)]
                name = sheet[(r, cell_mapping["name"])]
                username = hzpy.hz2py(name)
                id_number = sheet[(r, cell_mapping["id_number"])]
                try:
                    gender = sheet[(r, cell_mapping["gender"])]
                except KeyError, e:
                    gender=u"未知的性别"
                #technical_title = sheet[(r, cell_mapping["technical_title"])]
                #job_status = sheet[(r, cell_mapping["job_status"])]
                #diploma = sheet[(r, cell_mapping["diploma"])]
                email = "%s@fenbica.com" % username
                birth_date = id_number2birthday(id_number)
                dtenroll = sheet[(r, cell_mapping["dtenroll"])]
                diploma = sheet[(r, cell_mapping["diploma"])]
                #print dtenroll, minimalist_xldate_as_datetime(dtenroll, 0)
                #password = id_number[6:14]
                password = "dir"
                print username, id_number, gender, dtenroll, diploma#, technical_title, diploma, email
                if diploma.startswith(u"本科"):
                    diploma = DiplomaCode.objects.get(pk=20)
                elif diploma.startswith(u"大专"):
                    diploma = DiplomaCode.objects.get(pk=30)
                elif diploma.startswith(u"中专"):
                    diploma = DiplomaCode.objects.get(pk=40)
                elif diploma.startswith(u"高中"):
                    diploma = DiplomaCode.objects.get(pk=60)
                elif diploma.startswith(u"初中"):
                    diploma = DiplomaCode.objects.get(pk=70)
                else:
                    diploma = DiplomaCode.objects.none()

                print diploma

                exist_user_count = User.objects.filter(username = username).count()
                if exist_user_count > 0:
                    username = username + str(exist_user_count + 1)
                staff = Staff(
                    username=username,
                    email = email,
                    name=name,
                    password=password,
                    identity= Staff.IDENTITY_STAFF,
                    gender = GenderCode.objects.get(name=gender),
                    id_no = id_number,
                    spell_name = username,
                    dtenroll=minimalist_xldate_as_datetime(dtenroll, 0),
                    birthday = birth_date,
                    diploma = diploma
                )
                #staff.save()
                staff.set_password(password)
                staff.save()
                #user = User.objects.create_user(username, email, password)

                #user.person.identity = staff.IDENTITY_STAFF
                #person = user.person.save()

                #person.staff.name = name
                #person.staff.gender=GenderCode.objects.get(name=gender)

                #person.staff.id_no = id_number
                #person.staff.spell_name = username
                #person.staff.birthday = birth_date
                #person.staff.save()

                #user.person.staff.name = name
                #user.person.staff.gender=GenderCode.objects.get(name=gender)

                #user.person.staff.id_no = id_number
                #user.person.staff.spell_name = username
                #user.person.staff.birthday = birth_date
                #user.person.staff.save()

                #staff = Staff(user=user, school=school)
                #staff.save()


                #user.first_name = name[1:] #名字
                #user.last_name = name[0] #姓氏
                #person, new = Person.objects.get_or_create(person=user.person)
                #staff_profile = Staff(
                        #school = school,
                        #name = name,
                        #id_no =id_number,
                        ##id_type = u"身份证",
                        #gender=GenderCode.objects.get(name=gender),
                        #spell_name = username,
                        ##technical_title = technical_title,
                        ##diploma = diploma,
                        #birthday = birth_date,
                        #)
                #staff_profile.save()
                break
            except KeyError, e:
                print e

def import_data_student_chu1(file_path, sheet_number):
    """把指定格式的excel数据导入到数据库"""
    cell_mapping = {
            "classgrade": 1,
            "name": 2,
            "gender": 3,
            "birthday":4,         
            "id_number": 5,
            "domicle_location": 7,
            "postal_address": 7
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])

    import datetime
    dtstart = datetime.date(2010, 9, 1)
    from classgrade.models import Classmate, Class
    #print rows, cols
    for r in range(2, rows+1):
        for c in range(cols+1):
            try:
                name = sheet[(r, cell_mapping["name"])]
            except:
                break
            username = hzpy.hz2py(name)
            try:
                id_number = sheet[(r, cell_mapping["id_number"])]
            except:
                id_number = ""

            try:
                gender = sheet[(r, cell_mapping["gender"])]
            except KeyError, e:
                gender=u"未知的性别"
            else:
                if gender == 1:
                    gender = u"男"
                elif gender == 2:
                    gender = u"女"
                else:
                    gender=u"未知的性别"
                print gender

            email = "%s@fenbica.com" % username
            try:
                birth_date = id_number2birthday(id_number)
            except:
                birth_date = None
            password = "dir"#id_number[6:14]
            #print "excel: ", username
            #exist_user_count = User.objects.filter(username__exact=username).count()
            exist_user_count = User.objects.filter(username__regex=u"%s[1-9]{0,}" % username).count()
            #print exist_user_count
            if exist_user_count > 0:
                username = username + str(exist_user_count + 1)

            if len(id_number) > 18:
                id_number = ""
            #try:
                #telephone = str(sheet.get((r, cell_mapping["telephone"]), "")).split(".")[0]
            #except:
                #telephone = sheet.get((r, cell_mapping["telephone"]), "")
            try:
                domicle_location = sheet.get((r, cell_mapping["domicle_location"]), "")
                print domicle_location
            except Exception,e:
                print e
            else:
                domicle_location = domicle_location
            postal_address = sheet.get((r, cell_mapping["postal_address"]), "")

            classgrade = str(sheet.get((r, cell_mapping["classgrade"]), ""))
            classgrade = Class.objects.get(uuid="201031%s" % classgrade.zfill(2))
            print classgrade

            student = Student(
                username=username,
                email=email,
                password=password,
                spell_name=username,
                identity=Person.IDENTITY_STUDENT,
                gender=GenderCode.objects.get(name=gender),
                id_no=id_number,
                birthday=birth_date,
                #telephone=telephone,
                domicle_location=domicle_location,
                postal_address=postal_address,
                dtenroll = dtstart,
                name=name,
            )
            student.set_password(password)
            student.save()

            classmate = Classmate.objects.create(
                klass = classgrade,
                student = student,
                dtstart = dtstart
            )
            print classmate

            break

def import_data_student_chu2(file_path, sheet_number):
    """把指定格式的excel数据导入到数据库"""
    cell_mapping = {
            "classgrade": 0,
            "name": 1,
            "gender": 2,
            "birthday":3,         
            "id_number": 4,
            "telephone": 5,
            "domicle_location": 6,
            "postal_address": 6
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])

    import datetime
    dtstart = datetime.date(2010, 9, 1)
    from classgrade.models import Classmate, Class
    #print rows, cols
    for r in range(1, rows+1):
        for c in range(cols+1):
            try:
                name = sheet[(r, cell_mapping["name"])]
            except:
                break
            username = hzpy.hz2py(name)
            try:
                id_number = sheet[(r, cell_mapping["id_number"])]
            except:
                id_number = ""
            try:
                gender = sheet[(r, cell_mapping["gender"])]
            except KeyError, e:
                gender=u"未知的性别"
            else:
                print gender
            email = "%s@fenbica.com" % username
            try:
                birth_date = id_number2birthday(id_number)
            except:
                birth_date = None
            password = "dir"#id_number[6:14]
            #print "excel: ", username
            exist_user_count = User.objects.filter(username__exact=username).count()
            #print exist_user_count
            if exist_user_count > 0:
                username = username + str(exist_user_count + 1)

            if len(id_number) > 18:
                id_number = ""
            try:
                telephone = str(sheet.get((r, cell_mapping["telephone"]), "")).split(".")[0]
            except:
                telephone = sheet.get((r, cell_mapping["telephone"]), "")
            try:
                domicle_location = sheet.get((r, cell_mapping["domicle_location"]), "")
                print domicle_location
            except Exception,e:
                print e
            else:
                domicle_location = domicle_location
            postal_address = sheet.get((r, cell_mapping["postal_address"]), "")

            classgrade = sheet.get((r, cell_mapping["classgrade"]), "")[1:]
            classgrade = Class.objects.get(uuid="201032%s" % classgrade.zfill(2))
            print classgrade

            student = Student(
                username=username,
                email=email,
                password=password,
                spell_name=username,
                identity=Person.IDENTITY_STUDENT,
                gender=GenderCode.objects.get(name=gender),
                id_no=id_number,
                birthday=birth_date,
                telephone=telephone,
                domicle_location=domicle_location,
                postal_address=postal_address,
                dtenroll = dtstart,
                name=name,
            )
            student.set_password(password)
            student.save()

            classmate = Classmate.objects.create(
                klass = classgrade,
                student = student,
                dtstart = dtstart
            )
            print classmate

            break

def import_data_student_chu3(file_path, sheet_number):
    """把指定格式的excel数据导入到数据库"""
    cell_mapping = {
            "classgrade": 0,
            "name": 1,
            "gender": 2,
            "birthday":3,         
            "id_number": 4,
            "telephone": 5,
            "domicle_location": 6,
            "postal_address": 6
            }
    sheet = parse_xls(file_path)[sheet_number][1]
    rows = max([r[0] for r in sheet])
    cols = max([c[1] for c in sheet])

    import datetime
    dtstart = datetime.date(2010, 9, 1)
    from classgrade.models import Classmate, Class
    #print rows, cols
    for r in range(1, rows+1):
        for c in range(cols+1):
            try:
                name = sheet[(r, cell_mapping["name"])]
            except:
                break
            username = hzpy.hz2py(name)
            try:
                id_number = sheet[(r, cell_mapping["id_number"])]
            except:
                id_number = ""
            try:
                gender = sheet[(r, cell_mapping["gender"])]
            except KeyError, e:
                gender=u"未知的性别"
            else:
                print gender
            email = "%s@fenbica.com" % username
            try:
                birth_date = id_number2birthday(id_number)
            except:
                birth_date = None
            password = "dir"#id_number[6:14]
            #print "excel: ", username
            exist_user_count = User.objects.filter(username__exact=username).count()
            #print exist_user_count
            if exist_user_count > 0:
                username = username + str(exist_user_count + 1)

            if len(id_number) > 18:
                id_number = ""
            try:
                telephone = str(sheet.get((r, cell_mapping["telephone"]), "")).split(".")[0]
            except:
                telephone = sheet.get((r, cell_mapping["telephone"]), "")
            try:
                domicle_location = sheet.get((r, cell_mapping["domicle_location"]), "")
                print domicle_location
            except Exception,e:
                print e
            else:
                domicle_location = domicle_location
            postal_address = sheet.get((r, cell_mapping["postal_address"]), "")

            classgrade = sheet.get((r, cell_mapping["classgrade"]), "")[1:]
            classgrade = Class.objects.get(uuid="201033%s" % classgrade.zfill(2))
            print classgrade

            student = Student(
                username=username,
                email=email,
                password=password,
                spell_name=username,
                identity=Person.IDENTITY_STUDENT,
                gender=GenderCode.objects.get(name=gender),
                id_no=id_number,
                birthday=birth_date,
                telephone=telephone,
                domicle_location=domicle_location,
                postal_address=postal_address,
                dtenroll = dtstart,
                name=name,
            )
            student.set_password(password)
            student.save()

            classmate = Classmate.objects.create(
                klass = classgrade,
                student = student,
                dtstart = dtstart
            )
            print classmate

            break

if __name__ == "__main__":
    import_location_code()
    import_post_occupation_code()
    import_folk_code()
    import_nationality_code()
    import_politics_code()
    import_health_code()
    import_emigrant_code()
    import_marriage_code()
    import_blood_type_code()
    import_student_type_code()
    import_class_type_code()
    import_school_type_code()
    import_diploma_code()
    import_staff_type_code()
    import_gender_code()
    import_floating_code()
    import_location_type_code()
    import_location_econ_code()
    import_location_folk_code()
    import_degree_code()
    import_singleton_code()
    import_domicle_type_code()
    import_relation_code()
    import_learning_mode_code()
    import_learning_way_code()
    import_technical_post_code()
    import_cadre_post_code()
    import_cadre_post_level_code()
    import_social_job_code()
    import_learning_stage_code()
    import_grade_code()
    import_semester_code()

    import_rewards_type_code()
    import_rewards_level_code()
    import_punishment_name_code()
    import_enrollment_type_code()
    import_attendance_type_code()
    import_source_type_code()
    import_graduate_direction_code()
    import_education_result_code()
    import_transfer_type_code()
    import_transfer_status_code()
    import_occupation_code()
    import_teaching_type_code()
    import_teaching_role_code()
    import_exam_mode_code()
    import_exam_type_code()
    import_level_score_code()
    import_teaching_mode_code()
    import_room_usage_code()
    import_teaching_use_property_code()
    import_school_unit_level_code()
    import_building_category_code()
    import_building_structrue_code()
    import_funding_source_code()
    import_building_status_code()
    import_property_usage_code()
