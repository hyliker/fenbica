#coding: utf-8
import re
import datetime
from django.db import models
from django.db.models import F

# Create your models here.

class Class(models.Model):
    """班级信息模型"""
    grade = models.ForeignKey("standard.GradeCode", verbose_name=u"年级")
    dtcreated = models.DateField(default=datetime.datetime.now, verbose_name=u"建班年月")
    uuid = models.CharField(max_length=8, unique=True, verbose_name=u"班级代码", help_text=u"代码格式如 20083101, 共8位， 从左到右排序，第1－4位表示本班年份，5-6位表示年级代码 7-8位表示学校班级序号")
    name = models.CharField(max_length=20, verbose_name=u"班级名称", help_text=u"例如：2007届01班, 或者是高一7班, 物理1班 之类的说明性名称")
    type = models.ForeignKey("standard.ClassTypeCode", null=True, blank=True, verbose_name=u"班级类型")
    honorary_title = models.CharField(max_length=40, blank=True, verbose_name=u"荣誉称号")
    schooling_length = models.SmallIntegerField(max_length=2, null=True, blank=True, verbose_name=u"学制", help_text=u"接受学历教育在校学习完成学业规定的年限，单位：年")
    master = models.ForeignKey("staff.Staff", null=True, blank=True, verbose_name=u"班主任")#班主任编号
    monitor = models.ForeignKey("student.Student", null=True, blank=True, verbose_name=u"班长") #班长学号
    classroom = models.ForeignKey("school.Classroom", null=True, blank=True, verbose_name=u"教室")
    #courses = models.ManyToManyField("course.Course", null=True, blank=True, verbose_name=u"课程", through="Course")
    student_number = models.PositiveIntegerField(u"班学生人数", editable=False, default=0)

    class Meta:
        verbose_name = u"班级"
        verbose_name_plural = u"班级"
        ordering = ["-uuid", "grade",]

    def __unicode__(self):
        return "%s %s" % (self.uuid, self.name)

    @property
    def learning_year(self):
        return u"%s%s" % (self.dtcreated.year, self.dtcreated.year + 1)

    @models.permalink
    def get_absolute_url(self):
        return ("classgrade_class", [str(self.pk)])

#class Grade(models.Model):
    #"""年级信息模型"""
    #uuid = models.CharField(max_length=6, primary_key=True, verbose_name=u"年级代码", help_text=u"如200831, 6位， 从左到右排序，第1－4位表示本班年份，5-6位表示年级代码")
    #grade = models.ForeignKey("standard.GradeCode", verbose_name=u"年级")
    #master = models.ForeignKey("staff.Staff", verbose_name=u"级组长")
    #dtcreated = models.DateField(u"创建年月")
    #remark = models.TextField(u"备注")

#class Course(models.Model):
    #"""班级选课"""
    #klass = models.ForeignKey("Class", verbose_name=u"班级")
    #course = models.ForeignKey("course.Course", verbose_name=u"课程")
    #dtstart = models.DateField(u"开始日期", default=datetime.datetime.now)
    #dtend = models.DateField(u"结束日期", null=True, blank=True)
    #remark = models.TextField(blank=True, verbose_name=u"备注")

    #def __unicode__(self):
        #return u"%s %s" % (self.klass, self.course)

    #class Meta:
        #verbose_name = u"班级课程"
        #verbose_name_plural = u"班级课程"
        #unique_together = ("klass", "course",)

class Classmate(models.Model):
    """同班同学"""
    uuid = models.CharField(max_length=11, unique=True, verbose_name=u"班学号", help_text=u"格式如:20083101001, 共11位， 从左到右排序，第1－8位表示班级编号 9-10位表示班级学生序号01-999之间")
    klass = models.ForeignKey("Class", verbose_name=u"班级")
    student = models.ForeignKey("student.Student", verbose_name=u"学生")
    dtstart = models.DateField(u"开始日期", default=datetime.datetime.now, help_text=u"加入此班的日期")
    dtend = models.DateField(u"结束日期", help_text=u"退出此班的日期", null=True, blank=True)
    remark = models.TextField(u"备注", blank=True, help_text=u"学生班级变动时候，可以在此备注栏说明变动的原因")

    def __unicode__(self):
        return u"%s %s" % (self.klass, self.student)

    def save(self, *args, **kwargs):
        if not self.pk and not self.uuid: #created 
            from django.db.models import Max
            max_uuid = Classmate.objects.filter(klass=self.klass_id).aggregate(Max("uuid")).get("uuid__max")
            if max_uuid is None:
                new_uuid = u"%s%s" % (self.klass.uuid, "001") 
            else:
                new_uuid = str(int(max_uuid + 1))
            self.uuid = new_uuid
        super(Classmate, self).save(*args, **kwargs)

    class Meta:
        verbose_name= u"同班同学"
        verbose_name_plural = u"同班同学"
        ordering = ("uuid", "-dtstart")

def classmate_post_save(sender, instance, **kwargs):
    #更新班级学生有效的名单人数
    klass = instance.klass
    klass.student_number = klass.classmate_set.filter(dtend__isnull=True).count()
    klass.save()

models.signals.post_save.connect(classmate_post_save, sender=Classmate)

class Leader(models.Model):
    """班干部"""
    klass = models.ForeignKey("Class", verbose_name=u"班级")
    student = models.ForeignKey("student.Student", verbose_name=u"学生")
    duty = models.CharField(u"职务", max_length="24", help_text=u"例如: 班长, 副班长, 学习委员等等")
    dtstart = models.DateField(u"开始日期")
    dtend = models.DateField(u"结束日期", null=True, blank=True)
    performance = models.TextField(u"工作表现", blank=True)
    quit_reason = models.TextField(u"辞职原因", blank=True)
    remark = models.TextField(u"备注", blank=True)

    def __unicode__(self):
        return self.duty

    class Meta:
        verbose_name = u"班干部"
        verbose_name_plural = u"班干部"

class Check(models.Model):
    """班级考核信息"""
    klass = models.ForeignKey("classgrade.Class", verbose_name=u"班级")
    dtchecked = models.DateField(u"考勤日期", null=True, blank=True)
    early_morning_ranking = models.SmallIntegerField(u"早晨考勤分数")
    morning_ranking = models.SmallIntegerField(u"上午考勤分数")
    afternoon_ranking = models.SmallIntegerField(u"下午考勤分数")
    evening_ranking = models.SmallIntegerField(u"晚上考勤分数")
    #student_attendance_ranking = models.PositiveSmallIntegerField(u"学生出勤分数")
    student_attendance_ranking = models.SmallIntegerField(u"学生出勤分数")
    school_uniform_ranking = models.SmallIntegerField(u"校服分数")
    classroom_order_ranking = models.SmallIntegerField(u"教室秩序分数")
    hairstyle_finery_ranking = models.SmallIntegerField(u"发型服饰分数")
    smoke_drink_ranking = models.SmallIntegerField(u"吸烟喝酒分数")
    game_ranking = models.SmallIntegerField(u"手机游戏分数")
    classroom_discipline_ranking = models.SmallIntegerField(u"课堂纪律分数")
    home_visiting_ranking = models.SmallIntegerField(u"家长联系分数")
    other_ranking = models.SmallIntegerField(u"其他分数")
    sum_ranking = models.SmallIntegerField(u"总分", editable=False)
    checker = models.ForeignKey("person.Person", related_name="classgrade_check_checker", verbose_name=u"检查者", null=True, help_text=u"如果是自己， 可以不用输入", blank=True)
    creator = models.ForeignKey("person.Person", related_name="classgrade_check_creator", verbose_name=u"录入者", editable=False)
    remark = models.TextField(blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.klass.name

    def save(self, *args, **kwargs):
        self.sum_ranking = sum([self.early_morning_ranking, self.morning_ranking, self.afternoon_ranking, self.evening_ranking,
                    self.student_attendance_ranking, self.school_uniform_ranking, self.classroom_order_ranking, 
                    self.hairstyle_finery_ranking, self.smoke_drink_ranking, self.classroom_discipline_ranking,
                    self.home_visiting_ranking, self.other_ranking, self.game_ranking,
                   ])
        super(Check, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ("classgrade_check", [str(self.pk)])

    class Meta:
        unique_together = ("klass", "dtchecked")
        verbose_name = u"班级考核信息"
        verbose_name_plural = u"班级考核信息"
        ordering = ("-dtchecked", "-klass" )

class AttendanceResult(models.Model):
    name = models.CharField(u"名称", max_length=16, help_text=u"例如:到岗, 迟到, 病假,　事假,　旷课,　其他")
    score = models.SmallIntegerField(u"分数")
    remark = models.TextField(blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"考勤結果项"
        verbose_name_plural = u"考勤結果项"
        ordering = ["-score"]

class Timeno(models.Model):
    learning_year = models.CharField(max_length=8, verbose_name=u"学年", help_text=u"完成一年制学业所跨的年度,如20082009")
    semester = models.ForeignKey("standard.SemesterCode", verbose_name=u"学期")
    number  = models.PositiveSmallIntegerField(u"第几节课")
    dtstart = models.TimeField(u"开始时间")
    dtend = models.TimeField(u"结束时间")

    def __unicode__(self):
        return u"%s 学年 %s 学期 %d" % (self.learning_year, self.semester, self.number)

    class Meta:
        unique_together = ("learning_year", "semester", "number")
        verbose_name = u"课表时间段配置"
        verbose_name_plural = u"课表时间段配置"
        ordering = ("-learning_year", "number", "-id")

class Timetable(models.Model):
    TYPE_EVEN_WEEK = 1
    TYPE_ODD_WEEK = 2
    TYPE_FULL_WEEK = 3

    TYPE_CHOICES = (
        (TYPE_EVEN_WEEK, u"双周制"),
        (TYPE_ODD_WEEK, u"单周制"),
        (TYPE_FULL_WEEK, u"全周制"),
    )

    WEEK_MONDAY = 1
    WEEK_TUESDAY = 2
    WEEK_WEDNESDAY = 3
    WEEK_THURSDAY = 4
    WEEK_FRIDAY = 5
    WEEK_SATURDAY = 6
    WEEK_SUNDAY = 7

    WEEK_CHOICES = (
        (WEEK_MONDAY, u"星期一"),
        (WEEK_TUESDAY, u"星期二"),
        (WEEK_WEDNESDAY, u"星期三"),
        (WEEK_THURSDAY, u"星期四"),
        (WEEK_FRIDAY, u"星期五"),
        (WEEK_SATURDAY, u"星期六"),
        (WEEK_SATURDAY, u"星期日"),
    )

    klass = models.ForeignKey("Class", verbose_name=u"班级")
    week = models.PositiveSmallIntegerField(u"星期几", choices=WEEK_CHOICES)
    timeno = models.ForeignKey("Timeno", verbose_name=u"第几节课")
    course = models.ForeignKey("course.Course", verbose_name=u"课程")
    type = models.PositiveSmallIntegerField(u"周制类型", choices=TYPE_CHOICES, default=TYPE_FULL_WEEK)
    remark = models.TextField(blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return u"%s %s" % (self.klass, self.course)

    class Meta:
        verbose_name = u"班级课程时间表"
        verbose_name_plural = u"班级课程时间表"
