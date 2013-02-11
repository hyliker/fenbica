#coding: utf-8
"""各种定制的特殊页面，如校园风光、便民服务页面"""
from django.db import models
from common.stdimage import StdImageField

# Create your models here.

class Scenery(models.Model):
    """校园风光"""
    image = StdImageField(upload_to="page_scenery", size=(800,600), thumbnail_size=(200,130), verbose_name=u"照片")
    title = models.CharField(max_length=75, verbose_name=u"标题")
    description = models.TextField(blank=True, verbose_name=u"描述")
    dtcreated = models.DateTimeField(auto_now_add=True, verbose_name=u"日期")
    display_order = models.IntegerField(default=0, verbose_name=u"显示顺序")
    is_published = models.BooleanField(default=True, verbose_name=u"是否发布")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"校园风光"
        verbose_name_plural = u"校园风光"
        ordering = ["-display_order"]

class PhoneCategory(models.Model):
    """电话簿分类"""
    name = models.CharField(max_length=24,unique=True, verbose_name="分类名称")
    display_order = models.IntegerField(default=0, verbose_name=u"显示顺序")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"电话簿分类"
        verbose_name_plural = u"电话簿分类"
        ordering = ["-display_order"]

class Phone(models.Model):
    """对外公布的服务电话簿"""
    category = models.ForeignKey("PhoneCategory", verbose_name=u"分类")
    name = models.CharField(max_length=16, verbose_name="名称")
    phone = models.CharField(max_length=32, verbose_name=u"号码")
    display_order = models.IntegerField(default=0, verbose_name=u"显示顺序")
    is_valid = models.BooleanField(default=True, verbose_name=u"是否有效")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"电话簿号码"
        verbose_name_plural = u"电话簿号码"
        ordering = ["-display_order"]

class Teacher(models.Model):
    """师资队伍"""
    staff = models.OneToOneField("staff.Staff", verbose_name="教职工")
    title = models.CharField(max_length=75, verbose_name=u"头街")
    introduction = models.TextField(blank=True, verbose_name=u"简介")
    photo = StdImageField(upload_to="page_teacher", size=(800,600), thumbnail_size=(200,130), verbose_name=u"照片")
    display_order = models.IntegerField(default=0, verbose_name=u"显示顺序")
    is_published = models.BooleanField(default=True, verbose_name=u"是否有效")

    def __unicode__(self):
        return self.staff.name

    class Meta:
        verbose_name = u"师资队伍"
        verbose_name_plural = u"师资队伍"
        ordering = ["-display_order"]

#class CollegeEnrolleeSummary(models.Model):
    #"""高考录取总结"""
    #year = models.CharField(max_length=4, verbose_name=u"年度")
    #summary = models.TextField(verbose_name=u"总结")
    #dtcreated = models.DateTimeField(auto_now_add=True, verbose_name=u"日期")

#class CollegeEnrolleeLevel(models.Model):
    #"""高考录取批次等级"""
    #name = models.CharField(max_length=32, unique=True, verbose_name="名称", \
                            #help_text=u"例如: 本科提前批A 本科提前批B 本科一批A 本科一批B 本科二批A 本科二批B 本科三批 专科提前批 专科一批 专科二批")
    #priority = models.IntegerField(default=0, verbose_name=u"优先顺序", help_text=u"数值越大，越显示在前")

    #def __unicode__(self):
        #return self.name

    #class Meta:
        #verbose_name = u"高考录取批次等级"
        #verbose_name_plural = u"高考录取批次等级"

#class CollegeEnrollee(models.Model):
    #"""高考录取榜"""
    #uuid = models.CharField(u"准考证", max_length=32, primary_key=True)
    #student = models.ForeignKey("student.Student", verbose_name=u"学生")
    #level = models.ForeignKey(CollegeEnrolleeLevel, verbose_name=u"录取批次") 
    #college = models.CharField(u"录取院校", max_length=32)
    #major = models.CharField(u"专业", max_length=32)
    #score = models.PositiveSmallIntegerField(u"分数成绩")
    #dtenrolled = models.DateField(verbose_name=u"录取日期")
    #priority = models.IntegerField(default=0, verbose_name=u"优先顺序", help_text=u"数值越大，越显示在前")
    #is_approved = models.BooleanField(u"是否经核准通过", default=False)
    #remark = models.TextField(u"备注", blank=True)

    #def __unicode__(self):
        #return self.student.name

    #class Meta:
        #verbose_name = u"高考录取榜"
        #verbose_name_plural = u"高考录取榜"
        #ordering = ["priority", "-dtenrolled"]
