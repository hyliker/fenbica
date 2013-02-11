#coding:utf-8
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from utils.django_snippets import OverwriteStorage
from decimal import Decimal
from django.core.exceptions import ValidationError

class ExamCategory(models.Model):
    """考试分类"""
    name = models.CharField(max_length=32, unique=True, verbose_name=u"考试分类名称", help_text=u"如期中考试、期末考试、模拟1等等")

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u"考试分类"
        verbose_name_plural = u"考试分类"

# Create your models here.
class Exam(models.Model):
    """学生在校考试信息"""

    learning_year = models.CharField(max_length=8, verbose_name=u"学年", db_index=True, help_text=u"完成一年制学业所跨的年度,如20082009", \
                    validators=[RegexValidator(r"([1-9][0-9]{3}){2}", \
                                    message=u"学年格式举例,如2008至2009学年, 则填写20082009, 注意,数字的录入要切换到英文输入法", code=None)])
    semester = models.ForeignKey("standard.SemesterCode", verbose_name=u"学期")
    category = models.ForeignKey("ExamCategory", verbose_name=u"考试分类")
    exam_type = models.ForeignKey("standard.ExamTypeCode", null=True, blank=True, verbose_name=u"考试类别")
    dtstart = models.DateField(verbose_name=u"考试开始日期", null=True, blank=True)
    dtend = models.DateField(verbose_name=u"考试结束日期", null=True, blank=True)
    log = models.TextField(blank=True, verbose_name=u"备忘录")

    def __unicode__(self):
        return u"%(learning_year_start)s - %(learning_year_end)s年度 %(semester)s %(category)s" % {
            "learning_year_start": self.learning_year[:4],
            "learning_year_end": self.learning_year[4:],
            "category": self.category,
            "semester": self.semester.name,
        }
    @property
    def learning_year_verbose_name(self):
        return u"%s - %s年度" % (self.learning_year[:4],self.learning_year[4:])

    class Meta:
        verbose_name = u"考试"
        verbose_name_plural = u"考试"
        ordering = ("-dtstart","-id")
        permissions = (
            ("analyse_student", u"考试学生名次分析页面"),
            ("analyse_class", u"分析班级成绩"),
            ("analyse_grade", u"分析年级成绩"),
            ("analyse_subject", u"分析科目成绩"),
            ("room_seat", u"考室座位查看"),
            ("room_seat_arrange", u"考室座位编排"),
            ("export_seat_list", u"按考室导出登分表"),
            ("add_result_by_room", u"按考室名单录入成绩"),
            ("subject_list", u"考试信息"),
            ("add_result_by_room", u"按考室名单录入成绩"),
            ("add_result", u"按班级名单录入成绩"),
        )

class SubjectCategory(models.Model):
    """考试科目分类"""
    name = models.CharField(max_length=24, unique=True, verbose_name=u"科目名称", help_text=u"如语文")

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u"考试科目分类"
        verbose_name_plural = u"考试科目分类"


class Subject(models.Model):
    """考试科目信息"""
    #def get_file_path(instance, filename):
        #from datetime import datetime
        #now = datetime.now()
        #datetime_prefix = now.strftime("%Y/%m/%d")
        #return "uploads/exam/%s/%s/%s" % (datetime_prefix, filename)

    exam = models.ForeignKey(Exam, verbose_name=u"考试", help_text=u"如2008年秋期期末考试")
    grade = models.ForeignKey("standard.GradeCode", related_name="exam_course_set", verbose_name=u"年级")
    category = models.ForeignKey("SubjectCategory", verbose_name=u"科目")
    full_score = models.PositiveSmallIntegerField(max_length=3, verbose_name=u"考试满分值", help_text=u"100分则填写100, 120分则填写120")#add by me
    dtstart = models.DateTimeField(verbose_name=u"考试开始日期", null=True, blank=True)
    dtend = models.DateTimeField(verbose_name=u"考试结束日期", null=True, blank=True)
    learning_stage = models.ForeignKey("standard.LearningStageCode", verbose_name=u"学段", null=True, blank=True)
    exam_mode = models.ForeignKey("standard.ExamModeCode", related_name="exam_course_set", verbose_name=u"考试方式", null=True, blank=True)
    #file = models.FileField(upload_to=get_file_path, storage=OverwriteStorage(), null=True, blank=True, verbose_name=u"试卷文档", help_text=u"试卷文档本身，用来备案，方便以后查阅") # add by me
    file = models.FileField(upload_to="examfile/%Y/%m/%d", storage=OverwriteStorage(),  null=True, blank=True, verbose_name=u"附件", help_text=u"试卷文档本身，用来备案，方便以后查阅") # add by me
    log = models.TextField(blank=True, verbose_name=u"备忘录")

    def __unicode__(self):
        return u"%(learning_year_start)s - %(learning_year_end)s年度 %(semester)s %(grade)s %(exam_category)s %(subject_category)s" %  {
            "learning_year_start": self.exam.learning_year[:4],
            "learning_year_end": self.exam.learning_year[4:],
            "exam_category": self.exam.category,
            "semester": self.exam.semester.name,
            "subject_category": self.category,
            "grade": self.grade.name,
        }

    @models.permalink
    def get_absolute_url(self):
        return ("exam_subject", (), {"pk": self.pk})

    class Meta:
        verbose_name = u"考试科目"
        verbose_name_plural = u"考试科目"
        ordering = ("-dtstart", "-id", "-grade")

class Result(models.Model):
    """学生在校考试成绩信息"""

    STATUS_NORMAL = 0
    STATUS_MISSING = 1
    STATUS_CHEATING  = 2

    STATUS_CHOICES = (
        (STATUS_NORMAL, u"正常"),
        (STATUS_MISSING, u"缺考"),
        (STATUS_CHEATING, u"作弊"),
    )

    student = models.ForeignKey("student.Student", related_name="exam_result_set", verbose_name=u"学生档案")
    klass = models.ForeignKey("classgrade.Class", verbose_name=u"班级")
    #kuid = models.ForeignKey("classgrade.Classmate", to_field="uuid", verbose_name=u"班学号")
    subject = models.ForeignKey("Subject", verbose_name=u"考试科目")
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=u"分数类考试成绩", validators=[MinValueValidator(0)]) #(得分/总分)*100
    level = models.ForeignKey("standard.LevelScoreCode", null=True, blank=True, verbose_name=u"等级类考试成绩", help_text=u"共ABCDE五个等级，其中A>=90, B>=80, c>=70, d>=60,e<60", editable=False) 
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_NORMAL, verbose_name=u"状态")
    creator = models.ForeignKey("person.Person", editable=False, verbose_name=u"录入者")

    #def clean(self):
        #if self.score < 0 or self.score > self.course.full_score:
            #raise ValidationError(u"你输入的分数不在允许的 [0, %d]范围之内" % self.course.full_score)

    def save(self, *args, **kwargs):
        if self.score is None:
            super(Result, self).save(*args, **kwargs)
            return 

        full_score = self.subject.full_score
        if not 0 <= self.score <= full_score:
            raise ValidationError(u"你输入的分数不在允许的 [0, %d]范围之内" % self.subject.full_score)
        level_A = full_score * Decimal('0.9')
        level_B = full_score * Decimal('0.8')
        level_C = full_score  * Decimal('0.7')
        level_D =  full_score  * Decimal('0.6')
        score = self.score

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
            self.level = LevelScoreCode.objects.get(pk=level)
        except:
            self.level = None

        super(Result, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.student.name

    @staticmethod
    def _skip_ranking(element, ordered_list):
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

    @property
    def class_ranking(self):
        """返回该科目的成绩班排名"""
        #result_list = Result.objects.filter(course=self.course_id, klass=self.klass_id)
        result_list = Result.objects.filter(subject=self.subject_id, klass=self.klass_id)
        ordered_score_list = result_list.values_list("score", flat=True).order_by("-score")

        for index, item in enumerate(ordered_score_list):
            if index == 0:
                ranking = 1
            else:
                if item != pre_element:
                    ranking = index + 1
            if item == self.score:
                return ranking
            pre_element = item 

        #return self._skip_ranking(self.score, ordered_score_list)

    @property
    def grade_ranking(self):
        """返回该科目的成绩班排名"""
        result_list = Result.objects.filter(subject=self.subject, klass__grade=self.klass.grade_id)
        ordered_score_list = result_list.values_list("score", flat=True).order_by("-score")
        return self._skip_ranking(self.score, ordered_score_list)

    class Meta:
        verbose_name = u"考试成绩"
        verbose_name_plural = u"考试成绩"
        unique_together = ("student", "subject")
        ordering = ("-subject__dtstart", )

class Seat(models.Model):
    """考试座位"""
    examinee = models.ForeignKey("student.Student", verbose_name=u"考生")
    klass = models.ForeignKey("classgrade.Class", verbose_name=u"班级")
    classmate = models.ForeignKey("classgrade.Classmate", to_field="uuid", verbose_name=u"班学号")
    room = models.ForeignKey("Room", verbose_name=u"试室")
    uuid = models.CharField(u"编号", max_length=12)
    row = models.PositiveSmallIntegerField(u"行号")
    col = models.PositiveSmallIntegerField(u"列号")

    def __unicode__(self):
        return self.examinee.name

    class Meta:
        verbose_name = u"考试座位"
        verbose_name_plural = u"考试座位"
        ordering = ["uuid",]

class Room(models.Model):
    """试室"""
    uuid = models.CharField(u"试室编号", max_length=12)
    name = models.CharField(u"试室名称", max_length=24)
    exam = models.ForeignKey("Exam", verbose_name=u"考试")
    grade = models.ForeignKey("standard.GradeCode", verbose_name=u"年级")
    examiner = models.ManyToManyField("person.Person", verbose_name=u"考官")
    seat_num = models.PositiveSmallIntegerField(u"座位数目")
    col_num = models.CommaSeparatedIntegerField(u"各列人数分布", help_text=u"例如: 7,8,8,8,7", max_length=24)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("exam_room", (), {"pk": self.pk})

    class Meta:
        verbose_name = u"考试试室"
        verbose_name_plural = u"考试试室"
        unique_together = ("exam", "uuid")
        ordering = ("exam__dtstart", "uuid",)
