#coding: utf-8
from django.db import models

# Create your models here.

class Course(models.Model):
    """课程信息"""
    #COURSE_CHOICES = (
        #(u"语文", u"语文"),
        #(u"数学", u"数学"),
        #(u"英语", u"英语"),
        #(u"物理", u"化学"),
        #(u"历史", u"历史"),
        #(u"地理", u"地理"),
        #(u"生物", u"生物"),
        #(u"体育", u"体育"),
        #(u"音乐", u"音乐"),
        #(u"美术", u"美术"),
        #(u"信息技术", u"信息技术"),
    #)
    uuid = models.CharField(max_length=12, unique=True, verbose_name=u"编号", primary_key=True)
    name = models.CharField(max_length=32, verbose_name=u"名称")
    #name = models.CharField(max_length=32, choices = COURSE_CHOICES, verbose_name=u"名称")
    english_name = models.CharField(max_length=32, verbose_name=u"英文名称")
    semester = models.ForeignKey("standard.SemesterCode", verbose_name=u"学期")
    teaching_year = models.CharField(max_length=8, verbose_name=u"开课学年", help_text="输入的格式样例,如果是2008年至2009年度的,则填写20082009")
    exam_mode = models.ForeignKey("standard.ExamModeCode", verbose_name=u"考试方式", null=True, blank=True)
    teaching_mode = models.ForeignKey("standard.TeachingModeCode", verbose_name=u"授课方式", null=True, blank=True)
    teacher = models.ForeignKey("staff.Staff", verbose_name=u"授课老师职工")
    grade = models.ForeignKey("standard.GradeCode", verbose_name=u"授课年级")
    #klass = models.ForeignKey("classgrade.Class", verbose_name=u"班级")
    capacity = models.PositiveIntegerField(u"选修学生人数限制", null=True, blank=True)
    description = models.TextField(verbose_name=u"课程简介", blank=True)
    requires = models.TextField(verbose_name=u"课程要求", blank=True)
    total_period = models.IntegerField(max_length=3, null=True, blank=True, verbose_name=u"总学时")
    week_period = models.IntegerField(max_length=2, null=True, blank=True, verbose_name=u"周学时")
    self_study_period = models.IntegerField(max_length=2, null=True, blank=True, verbose_name=u"自学学时")
    textbook = models.TextField(verbose_name=u"教材", blank=True)
    billiography = models.TextField(verbose_name=u"参考书目", blank=True)
    teaching_resource = models.TextField(verbose_name=u"教学资源", blank=True)
    place = models.CharField(max_length=60, verbose_name=u"教学地点", blank=True)
    dtcreated = models.DateTimeField(u"创建日期", auto_now_add=True)
    dtmodified = models.DateTimeField(u"修改日期", auto_now=True)

    def __unicode__(self):
        return "%s %s %s" % (self.name, self.teacher.name, self.teaching_year)

    @models.permalink
    def get_absolute_url(self):
        return ("course_course", [str(self.pk)])

    class Meta:
        verbose_name = u"开设课程"
        verbose_name_plural = u"开设课程"
        ordering = ("-teaching_year",)

class StudentCourse(models.Model):
    """学生选课"""
    student = models.ForeignKey("student.Student", verbose_name=u"学生")
    course = models.ForeignKey("Course", verbose_name=u"课程")
    dtstart = models.DateTimeField(u"选课日期", auto_now_add=True)
    dtend = models.DateTimeField(u"退课日期", null=True, blank=True, help_text=u"退课日期是指中途退课日期")
    remark = models.TextField(u"备注", blank=True)
    dtmodified = models.DateTimeField(u"最后修改日期", auto_now=True)
    is_active = models.BooleanField(u"是否激活", default=True)

    def __unicode__(self):
        return u"%s %s" % (self.student, self.course)

    class Meta:
        unique_together = ("student", "course")
        verbose_name = u" 学生选课"
        verbose_name_plural = u"学生选课"

#class Timetable(models.Model):
    #"""学校课程表"""
    #school = models.ForeignKey("School", verbose_name=u"学校")
    #classroom = models.ForeignKey(Classroom, verbose_name=u"教室")
    #course = models.ForeignKey(Course)
    #dtstart = models.TimeField()
    #dtstop = models.TimeField()
    #Class = models.ForeignKey(Class, verbose_name=u"班号")

#class TeachingWorkload(models.Model):
    #"""教学工作量信息类"""
    #school = models.ForeignKey("school.School", verbose_name=u"学校")
    #teaching_type_code = models.CharField(max_length=2, verbose_name=u"教学类型码")
    #content = models.CharField(max_length=80, verbose_name=u"教学内容")
    #workload = models.PositiveIntegerField(max_length=4, verbose_name=u"教学工作量", help_text="单位：小时／年")
    #comment = models.TextField(verbose_name=u"教学评语")
    #dtstart = models.DateField(verbose_name=u"教学起始年月")
    #dtend = models.DateField(verbose_name=u"教学终止年月")

    #def __unicode__(self):
        #return self.content

#class Teaching(models.Model):
    #"""任课信息类"""
    #school = models.ForeignKey("school.School", verbose_name=u"学校")
    #teacher = models.ForeignKey("staff.Staff", verbose_name=u"老师")
    #course = models.CharField(max_length=8, verbose_name=u"课程号")
    #dtstart = models.DateField(verbose_name=u"起始年月")
    #dtend = models.DateField(verbose_name=u"终止年月")
    #total_period = models.PositiveIntegerField(max_length=3, verbose_name=u"总学时（单位：学时)")
    #learning_stage = models.CharField(max_length=1, verbose_name=u"学段")
    #role_code =  models.CharField(max_length=1, verbose_name=u"角色")
    #classes = models.CharField(max_length=120, verbose_name=u"指听课的班级")
    #student_amount = models.PositiveIntegerField(max_length=4, verbose_name=u"授课人数", help_text=u"指听课的人数，单位：人")

    #def __unicode__(self):
        #return self.course
