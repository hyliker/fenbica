#coding: utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Setting(models.Model):
    """key=value"""
    key = models.CharField(max_length=128, unique=True, verbose_name=u"变量名", help_text=u"变量名的长度限制在128个字符以下")
    value = models.TextField(verbose_name=u"变量值")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.key

    class Meta:
        abstract = True

class SystemSetting(Setting):
    """系统配置参数设置"""
    class Meta:
        verbose_name = u"系统变量"
        verbose_name_plural = u"系统变量"

class UserSetting(Setting):
    """用户配置参数设置"""
    user = models.ForeignKey(User)
    class Meta:
        verbose_name = u"用户配置变量"
        verbose_name_plural = u"用户配置参数设置"

class Term(models.Model):
    """学期"""
    year = models.IntegerField(max_length=4, verbose_name=u"年份")
    term = models.ForeignKey("TermCategory", verbose_name=u"学期")
    dtstart = models.DateTimeField(verbose_name=u"开始时间")
    dtend = models.DateTimeField(verbose_name=u"结束时间")
    week = models.PositiveIntegerField(verbose_name=u"周数")
    remark = models.TextField(verbose_name=u"备注")

    class Meta:
        verbose_name = u"学期配置"
        verbose_name_plural = u"学期配置"



class ClassroomCategory(models.Model):
    name = models.CharField(max_length=32, verbose_name=u"名称")
    abbr = models.CharField(max_length=16, verbose_name=u"简称")
    remark = models.TextField(verbose_name=u"备注")

#class ClassGrade(models.Model):
    #"""班级"""
    #uuid = models.CharField(max_length=32, verbose_name=u"编号")
    #term = models.ForeignKey("Term", verbose_name=u"学期")
    #name = models.CharField(max_length=12, verbose_name=u"名称")
    #population = models.PositiveIntegerField(verbose_name=u"人数")
    #class_teacher = models.ForeignKey("TeacherProfile", verbose_name=u"班主任")
    #grade_teacher = models.ForeignKey("TeacherProfile", verbose_name=u"年级组长")
    #classroom = models.ForeignKey("Classroom", verbose_name=u"教室")

    #class Meta:
        #verbose_name = u"班级"
        #verbose_name_plural = u"班级"

class TermCategory(models.Model):
    name = models.CharField(max_length=32, verbose_name=u"名称")
    abbr = models.CharField(max_length=16, verbose_name=u"简称")
    remark = models.TextField(verbose_name=u"备注")
