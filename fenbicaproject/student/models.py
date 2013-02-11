#coding: utf-8
import datetime
from django.db import models
from person.models import Person
from django.contrib.auth.models import User

# Create your models here.
class Student(Person):
    """学生信息模型"""

    ARCHIVE_CANCEL_REASON_CHOICES = (
        (1, u"已毕（结、肄）业"),
        (2, u"已升学或转学进入其他学校就读"),
        (3, u"年满18周岁已经不在本校读书"),
        (4, u"已经死亡或被宣告死亡或被宣告失踪"),
    )

    ARCHIVE_CREATE_REASON_CHOICES = (
        (1, u"新生入学"),
        (2, u"转入"),
    )

    ARCHIVE_STATUS_AWAITING = 1
    ARCHIVE_STATUS_APPROVED = 2
    ARCHIVE_STATUS_REJECTED = 3

    ARCHIVE_APPROVE_STATUS = (
        (ARCHIVE_STATUS_AWAITING, u"等待审核"),
        (ARCHIVE_STATUS_APPROVED, u"通过审核"),
        (ARCHIVE_STATUS_REJECTED, u"驳回审核"),
    )

    #Class = models.CharField(max_length=6, verbose_name=u"班号", blank=True, help_text=u"如200801, 6位， 从左到右排序，第1－4位表示本班毕业年份， 5-6位表示学校班级序号")
    #grade = models.ForeignKey("standard.GradeCode", null=True, blank=True, max_length=2, verbose_name=u"年级", help_text=u"当前就读年级")
    classes = models.ManyToManyField("classgrade.Class", verbose_name=u"班级成员", through='classgrade.Classmate')
    dtenroll = models.DateField(db_index=True, default=datetime.datetime.now,  verbose_name=u"入学年月")
    student_type = models.ForeignKey("standard.StudentTypeCode", null=True, blank=True, verbose_name=u"学生类别")
    original_school_name= models.CharField(max_length=60, blank=True, verbose_name=u"原学校名称")
    original_school_code = models.CharField(max_length=9, blank=True, verbose_name=u"原学校代码")
    enrollment_type = models.ForeignKey("standard.EnrollmentTypeCode", null=True, blank=True,  verbose_name=u"入学方式")
    original_area = models.ForeignKey("standard.LocationCode", null=True, blank=True, verbose_name=u"学生来源地区")
    source_type = models.ForeignKey("standard.SourceTypeCode", null=True, blank=True, verbose_name=u"生源类型")
    attendance_type = models.ForeignKey("standard.AttendanceTypeCode", null=True, blank=True, verbose_name=u"就读方式") #此处与标准文档有差别， 因为标准文档此处与入学方式码相同
    graduate_score = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=u"升学总分", help_text=u"入学时升学总分")

    dtrudui = models.DateField(verbose_name=u"入队时间", help_text=u"指加入中国少年先锋队", null=True, blank=True)
    dtrutuan = models.DateField(verbose_name=u"入团时间", help_text=u"中国共产主义青年团（简称共青团）", null=True, blank=True)

    latest_classgrade = models.ForeignKey("classgrade.Class", related_name="latest_classgrade", verbose_name=u"最近所在班级", null=True, blank=True, editable=False)

    #根据广东省义务教育阶段学生学籍卡， 增加如下字段
    archive_cancel_date = models.DateField(db_index=True, blank=True, null=True, verbose_name=u"注销学籍日期")
    archive_cancel_reason = models.SmallIntegerField(verbose_name=u"注销学籍原因", null=True, blank=True, max_length=1, choices=ARCHIVE_CANCEL_REASON_CHOICES)
    archive_approve_status = models.SmallIntegerField(verbose_name=u"学籍审核状态", null=True, blank=True, max_length=1, choices=ARCHIVE_APPROVE_STATUS)
    archive_approver = models.ForeignKey("staff.Staff", related_name="archive_verifier", editable=False, null=True, blank=True, verbose_name=u"学籍审核人", help_text=u"指教务处审核人")
    archive_administrator = models.ForeignKey("staff.Staff", related_name="archive_administrator", null=True, blank=True, verbose_name=u"学籍管理员")
    archive_remark = models.TextField(verbose_name="转学、休学、复学、辍学、出国记录", blank=True)
    archive_create_reason = models.SmallIntegerField(verbose_name=u"建卡原因", null=True, blank=True, max_length=1, \
                                                     choices=ARCHIVE_CREATE_REASON_CHOICES, help_text=u"指学籍卡建立的原因")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.identity = Person.IDENTITY_STUDENT
        #自动创建一个uuid
        if self.uuid is None:
            try:
                year = self.dtenroll.year
            except:
                from datetime import datetime
                year = datetime.now().year
            try:
                max_uuid = Student.objects.filter(dtenroll__year=year).order_by("-uuid")[0].uuid
                student_num = int(max_uuid[4:]) + 1
                if student_num > 10000:
                    print u"max uuid student_num < 10000"
            except Exception, e:
                print e
                student_num = Student.objects.filter(dtenroll__year=year).count() + 1
            self.uuid = u"S%(year)s%(next)s" % {"year": year, "next":str(student_num).zfill(4)} 

        if self.pk is None:
            exist_user_count = User.objects.filter(username__regex=u"%s[1-9]{0,}" % self.username).count()
            if exist_user_count > 0:
                self.username = self.username + str(exist_user_count + 1)

        #根据身份证号来填充出生日期
        if self.id_no and self.birthday is None:
            from common.utils import id_number2birthday
            self.birthday = id_number2birthday(self.id_no)

        super(Student, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"学生信息"
        verbose_name_plural = u"学生信息"
        permissions = (
            ("student", u"查看某人的档案资料库"),
            ("student_archive", u"查看学生的学籍卡"),
            ("experience_list", u"显示学生简历列表"),
            ("experience", u"学生简历条目"),
            ("keeper_list", u"学生监护人列表"),
            ("keeper", u"学生监护人条目"),
            ("family_member_list", u"学生家庭成员列表"),
            ("family_member", u"学生家庭成员条目"),
            ("register_list", u"学生注册信息列表"),
            ("register", u"学生注册信息"),
            ("comment_list", u"学生考评信息列表"),
            ("comment", u"学生考评信息条目"),
            ("rewards_list", u"学生奖励信息列表"),
            ("rewards", u"学生奖励信息条目"),
            ("punishment_list", u"学生处分信息列表"),
            ("punishment", u"学生处分信息条目"),
            ("graduate_list", u"学生毕业信息列表"),
            ("graduate", u"学生毕业信息条目"),
            ("finish_study_list", u"学生结业信息列表"),
            ("finish_study", u"学生结业信息条目"),
            ("transfer_list", u"学生学籍异动信息列表"),
            ("transfer", u"学生学籍异动信息条目"),
            ("assistance_list", u"学生贫困補助信息列表"),
            ("assistance", u"学生贫困補助信息条目"),
            ("drill_list", u"学生军训信息列表"),
            ("drill", u"学生军训信息条目"),
            ("exam_result_list", u"学生的考试信息列表"),
            ("exam_result_analyse", u"学生的考试成绩汇总分析"),
            ("classmate_list", u"学生就读班级记录"),
        )

def person_post_save(sender, instance, **kwargs):
    if instance.identity == instance.IDENTITY_STUDENT:
        student, new_student = Student.objects.get_or_create(pk=instance.pk)

models.signals.post_save.connect(person_post_save, sender=Person)

class Experience(models.Model):
    """学生简历"""
    student = models.ForeignKey("Student", verbose_name=u"学生档案")
    dtstart = models.DateField(verbose_name=u"起始时间", help_text=u"日期格式：YYYY-MM-DD")
    dtend = models.DateField(verbose_name=u"结束时间", help_text=u"日期格式：YYYY-MM-DD")
    school_name = models.CharField(max_length=60, verbose_name=u"所在学校名称")
    duty = models.CharField(max_length=30, blank=True, verbose_name=u"担任职务")
    attestor = models.CharField(max_length=30, blank=True, verbose_name=u"证明人")
    remark = models.TextField(blank=True, verbose_name=u"备注")

    class Meta:
        ordering = ["dtstart", "dtend"]
        verbose_name = "学生简历"
        verbose_name_plural = "学生简历"

    def __unicode__(self):
        return "%s %s" % (self.student.name, self.school_name)

class Keeper(models.Model):
    """学生监护人"""
    student = models.ForeignKey("student", verbose_name=u"学生档案")
    name = models.CharField(max_length=30, db_index=True, verbose_name=u"姓名")
    relation = models.ForeignKey("standard.RelationCode", verbose_name=u"关系")
    postal_address = models.CharField(max_length=60, verbose_name=u"联系地址")
    telephone = models.CharField(max_length=30, verbose_name=u"联系电话")
    postal_code = models.CharField(max_length=6, verbose_name=u"邮政编码")
    email = models.EmailField(max_length=30, blank=True, verbose_name=u"电子信箱")

    def __unicode__(self):
        return "%s %s" % (self.student.name, self.name )

    class Meta:
        verbose_name = "学生监护人"
        verbose_name_plural = "学生监护人"

class FamilyMember(models.Model):
    """学生家庭成员"""
    student = models.ForeignKey("Student", verbose_name=u"学生档案")
    name = models.CharField(max_length=30, db_index=True, verbose_name=u"姓名")
    relation = models.ForeignKey("standard.RelationCode", verbose_name=u"关系")
    id_no = models.CharField(db_index=True, max_length=18, blank=True, verbose_name=u"身份证号")
    company = models.CharField(max_length=18, blank=True, verbose_name=u"单位名称")
    telephone = models.CharField(max_length=30, blank=True, verbose_name=u"联系电话")
    folk = models.ForeignKey("standard.FolkCode", null=True, blank=True, verbose_name=u"民族")
    marriage = models.ForeignKey("standard.MarriageCode", null=True, blank=True, verbose_name=u"婚姻状况")
    emigrant = models.ForeignKey("standard.NationalityCode", null=True, blank=True, verbose_name=u"侨居地")

    def __unicode__(self):
        return "%s %s" % (self.student.name, self.name )

    class Meta:
        verbose_name = "学生家庭成员"
        verbose_name_plural = "学生家庭成员"

class Register(models.Model):
    """学生注册信息"""
    STATUS_REGISTERED = 1
    STATUS_UNREGISTERED = 0
    STATUS_CHOICES = (
        (STATUS_REGISTERED, u'注册'),
        (STATUS_UNREGISTERED, u'未注册'),
    )

    student = models.ForeignKey("Student", verbose_name=u"学生档案")
    learning_stage = models.ForeignKey("standard.LearningStageCode", verbose_name=u"学段")
    learning_year = models.CharField(max_length=8, verbose_name=u"学年", help_text="完成一年制学业所跨的年度,如20082009")
    semester = models.ForeignKey("standard.SemesterCode", verbose_name=u"学期")
    grade = models.ForeignKey("standard.GradeCode", verbose_name=u"年级")
    classgrade = models.ForeignKey("classgrade.Class", verbose_name=u"注册班级")
    status = models.SmallIntegerField(verbose_name=u"注册状况", choices=STATUS_CHOICES, default=STATUS_REGISTERED)
    #is_registered = models.BooleanField(verbose_name=u"是否已注册", default=False)
    deadline_date = models.DateField(verbose_name=u"要求最晚注册时间", null=True, blank=True)
    actual_date = models.DateField(verbose_name=u"实际注册时间", null=True, blank=True)
    not_reg_causation = models.TextField(max_length=120, blank=True, verbose_name=u"未注册原因")

    def __unicode__(self):
        return "%s %s" % (self.student.name, self.learning_year)

    class Meta:
        verbose_name = "学生注册"
        verbose_name_plural = "学生注册"


class Comment(models.Model):
    """学生考评信息"""
    student = models.ForeignKey("Student", related_name="student_comment", verbose_name=u"学生档案")
    learning_stage = models.ForeignKey("standard.LearningStageCode", verbose_name=u"学段")
    learning_year = models.CharField(max_length=8, verbose_name=u"学年", help_text="完成一年制学业所跨的年度,如20082009")
    semester = models.ForeignKey("standard.SemesterCode", verbose_name=u"学期")
    grade = models.ForeignKey("standard.GradeCode", verbose_name=u"年级")
    dtcomment = models.DateField(blank=True, verbose_name=u"考评日期", default=datetime.datetime.now)
    #teacher = models.ForeignKey("staff.Staff", blank=True, verbose_name=u"考评老师")
    teacher = models.ForeignKey("staff.Staff", related_name="student_comment", blank=True, verbose_name=u"考评老师", editable=False)
    comment = models.TextField(blank=True, verbose_name=u"学期评语")

    def __unicode__(self):
        return "%s %s" % (self.student.name, self.learning_year)

    class Meta:
        ordering = ("-dtcomment", "-id")
        verbose_name = "学生考评信息"
        verbose_name_plural = "学生考评信息"

class Rewards(models.Model):
    """学生奖励信息"""
    student = models.ForeignKey("Student", verbose_name=u"学生档案")
    name = models.CharField(max_length=60, verbose_name=u"奖励名称")
    level = models.ForeignKey("standard.RewardsLevelCode", verbose_name=u"奖励级别")
    type = models.ForeignKey("standard.RewardsTypeCode", verbose_name=u"奖励类别")
    money = models.DecimalField(max_digits=10, decimal_places=2,blank=True, verbose_name=u"奖励金額(单位:元)")
    file_no = models.CharField(max_length=30, blank=True, verbose_name=u"奖励文号")
    date = models.DateField(verbose_name=u"奖励年月")
    bureau = models.CharField(max_length=60, verbose_name=u"颁奖单位")
    causation = models.TextField(blank=True, verbose_name=u"奖励原因")

    def __unicode__(self):
        return "%s %s" % (self.student.name, self.name)
    
    class Meta:
        verbose_name = "学生奖励信息"
        verbose_name_plural = "学生奖励信息"


class Punishment(models.Model):
    """学生处分信息"""
    student = models.ForeignKey("Student", verbose_name=u"学生档案")
    name = models.ForeignKey("standard.PunishmentNameCode", verbose_name=u"处分名称")
    date = models.DateField(verbose_name=u"处分日期")
    file_no = models.CharField(max_length=30, blank=True, verbose_name=u"处分文号")
    repeal_date = models.DateField(blank=True, verbose_name=u"处分撤销日期")
    repeal_file_no = models.CharField(max_length=30, blank=True, verbose_name=u"处分撤销文号")
    causation = models.TextField(verbose_name=u"处分原因")

    def __unicode__(self):
        return "%s %s" % (self.student.name, self.name)
    
    class Meta:
        verbose_name = "学生处分信息"
        verbose_name_plural = "学生处分信息"

#class Enrollment(models.Model):
    #"""学生入学信息"""
    #student = models.OneToOneField("Student", verbose_name=u"学生档案")
    #original_school_name= models.CharField(max_length=60, verbose_name=u"原学校名称")
    #original_school_code = models.CharField(max_length=9, verbose_name=u"原学校代码")
    #date = models.DateField(verbose_name=u"入学年月")
    #type = models.ForeignKey("standard.EnrollmentTypeCode", verbose_name=u"入学方式")
    #original_area = models.ForeignKey("standard.LocationCode", verbose_name=u"来源地区")
    #original_student = models.ForeignKey("standard.OriginalStudentCode", verbose_name=u"学生来源")
    #attendance_type = models.ForeignKey("standard.AttendanceTypeCode", verbose_name=u"就读方式") #此处与标准文档有差别， 因为标准文档此处与入学方式码相同
    #graduate_score = models.DecimalField(max_digits=5, decimal_places=1, blank=True, verbose_name=u"升学总分")
    #fortes = models.TextField(blank=True, verbose_name=u"特长")

    #def __unicode__(self):
        #return self.student.name
    
    #class Meta:
        #verbose_name = "学生入学信息"
        #verbose_name_plural = "学生入学信息"

class Graduate(models.Model):
    """学生毕业信息"""
    student = models.OneToOneField("Student", primary_key=True, verbose_name=u"毕业生")
    direction = models.ForeignKey("standard.GraduateDirectionCode", verbose_name=u"毕业去向")
    date = models.DateField(verbose_name=u"毕业年月")
    comment = models.TextField(u"毕业评语", blank=True, help_text=u"登记入档的评语")

    def __unicode__(self):
        return self.student.name
    
    class Meta:
        verbose_name = "学生毕业信息"
        verbose_name_plural = "学生毕业信息"


class FinishStudy(models.Model):
    """学生结业信息"""
    student = models.OneToOneField("Student", primary_key=True, verbose_name=u"毕业生")
    date = models.DateField(verbose_name=u"结业年月", help_text=u"格式：CCYYMM")
    education_result = models.ForeignKey("standard.EducationResultCode", verbose_name=u"教育結果")
    causation = models.TextField(u"结业原因", blank=True)

    def __unicode__(self):
        return self.student.name

    class Meta:
        verbose_name = "学生结业信息"
        verbose_name_plural = "学生结业信息"

class Transfer(models.Model):
    """学生学籍异动信息"""
    student = models.ForeignKey("Student", verbose_name=u"学生档案")
    type = models.ForeignKey("standard.TransferTypeCode", verbose_name=u"变动类别")
    date = models.DateField(verbose_name=u"变动日期")
    causation = models.TextField(verbose_name=u"变动原因", blank=True)
    auditing_date = models.DateField(verbose_name=u"审批日期")
    auditing_file_no = models.CharField(max_length=30, blank=True, verbose_name=u"审批文号")
    original_school_name = models.CharField(max_length=60, verbose_name=u"原学校名称")
    original_school_code = models.CharField(max_length=9, verbose_name=u"原就读学校代码")
    target_school_code = models.CharField(max_length=9, verbose_name=u"现就读学校代码")
    original_class_code =  models.CharField(max_length=6, verbose_name=u"原就读班级代码")
    target_class_code = models.CharField(max_length=6, verbose_name=u"现就读班级代码")
    original_student_code = models.CharField(max_length=18, verbose_name=u"原学籍号")
    target_student_code = models.CharField(max_length=18, verbose_name=u"现学籍号")
    status = models.ForeignKey("standard.TransferStatusCode", verbose_name=u"处理状态")
    result = models.TextField(verbose_name=u"处理結果", blank=True)

    def __unicode__(self):
        return "%s %s" % (self.student.name, self.type)

    class Meta:
        verbose_name = "学籍异动信息"
        verbose_name_plural = "学籍异动信息"

class Assistance(models.Model):
    """学生贫困補助信息"""
    student = models.ForeignKey("Student", verbose_name=u"学生档案")
    learning_stage = models.ForeignKey("standard.LearningStageCode", verbose_name=u"学段")
    learning_year = models.CharField(max_length=8, verbose_name=u"学年")
    semester = models.ForeignKey("standard.SemesterCode", verbose_name=u"学期")
    grade = models.ForeignKey("standard.GradeCode", verbose_name=u"年级")
    reason = models.TextField(verbose_name=u"补助原因")
    date = models.DateField(verbose_name=u"补助时间")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"补助金额(单位:元)")
    implementator = models.ForeignKey("staff.Staff", verbose_name=u"经办老师")

    def __unicode__(self):
        return self.student.name

    class Meta:
        verbose_name = "贫困補助信息"
        verbose_name_plural = "贫困補助信息"

class Drill(models.Model):
    """学生军训信息"""
    student = models.ForeignKey("Student", verbose_name=u"学生档案")
    dtstart = models.DateField(verbose_name=u"军训起始时间")
    dtend = models.DateField(verbose_name=u"军训结束时间")
    troops = models.CharField(max_length=40, verbose_name=u"军训部队", help_text=u"部队的名称或番号")
    result = models.CharField(max_length=30, verbose_name=u"军训成绩", help_text=u"分数类或者等级类成绩")

    def __unicode__(self):
        return self.student.name

    class Meta:
        verbose_name = "军训信息"
        verbose_name_plural = "军训信息"

class Attendance(models.Model):
    """日常学生考勤"""
    student = models.ForeignKey("Student", verbose_name=u"学生")
    classgrade = models.ForeignKey("classgrade.Class", verbose_name=u"班级")
    event = models.CharField(u"考勤事件/项目", max_length=128, help_text=u"例如: 早读, 晚读, 自修, 第一节课等等")
    dtchecked = models.DateField(u"考勤日期", null=True, blank=True)
    checker = models.ForeignKey("person.Person", related_name="attendance_checker", verbose_name=u"检查者", null=True, help_text=u"如果是自己， 可以不用输入", blank=True)
    creator = models.ForeignKey("person.Person", related_name="attendance_creator", verbose_name=u"录入者", editable=False)
    result = models.ForeignKey("AttendanceResult", verbose_name=u"考勤結果")
    remark = models.TextField(blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return u"%s %s" % (self.student, self.event)

    class Meta:
        verbose_name = u"学生考勤信息"
        verbose_name_plural = u"学生考勤信息"

class AttendanceResult(models.Model):
    """学生考勤信息"""
    name = models.CharField(u"名称", max_length=16, help_text=u"例如:到岗, 迟到, 病假,　事假,　旷课,　其他")
    score = models.SmallIntegerField(u"分数")
    remark = models.TextField(blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"考勤結果项"
        verbose_name_plural = u"考勤結果项"
        ordering = ["-score"]

class CollegeEnrolleeSummary(models.Model):
    """高考录取总结"""
    year = models.CharField(max_length=4, verbose_name=u"年度")
    summary = models.TextField(verbose_name=u"总结")
    dtcreated = models.DateTimeField(auto_now_add=True, verbose_name=u"日期")

class CollegeEnrolleeLevel(models.Model):
    """高考录取批次等级"""
    name = models.CharField(max_length=32, unique=True, verbose_name="名称", \
                            help_text=u"例如: 本科提前批A 本科提前批B 本科一批A 本科一批B 本科二批A 本科二批B 本科三批 专科提前批 专科一批 专科二批")
    priority = models.IntegerField(default=0, verbose_name=u"优先顺序", help_text=u"数值越大，越显示在前")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"高考录取批次等级"
        verbose_name_plural = u"高考录取批次等级"

class CollegeEnrollee(models.Model):
    """高考录取榜"""
    uuid = models.CharField(u"准考证", max_length=32, primary_key=True)
    student = models.ForeignKey("student.Student", verbose_name=u"学生")
    level = models.ForeignKey(CollegeEnrolleeLevel, verbose_name=u"录取批次") 
    college = models.CharField(u"录取院校", max_length=32)
    major = models.CharField(u"专业", max_length=32)
    score = models.PositiveSmallIntegerField(u"分数成绩")
    dtenrolled = models.DateField(verbose_name=u"录取日期")
    priority = models.IntegerField(default=0, verbose_name=u"优先顺序", help_text=u"数值越大，越显示在前")
    is_approved = models.BooleanField(u"是否经核准通过", default=False)
    remark = models.TextField(u"备注", blank=True)

    def __unicode__(self):
        return self.student.name

    class Meta:
        verbose_name = u"高考录取榜"
        verbose_name_plural = u"高考录取榜"
        ordering = ["priority", "-dtenrolled"]

class ZhongKaoEnrolleeSummary(models.Model):
    """中考录取总结"""
    year = models.CharField(max_length=4, verbose_name=u"年度")
    summary = models.TextField(verbose_name=u"总结")
    dtcreated = models.DateTimeField(auto_now_add=True, verbose_name=u"日期")

class ZhongKaoEnrollee(models.Model):
    """中考录取榜"""
    uuid = models.CharField(u"准考证", max_length=32, primary_key=True)
    student = models.ForeignKey("student.Student", verbose_name=u"学生")
    klass = models.ForeignKey("classgrade.Class", verbose_name=u"所有班级")
    school = models.CharField(u"录取学校", max_length=32)
    score = models.PositiveSmallIntegerField(u"分数成绩")
    dtenrolled = models.DateField(verbose_name=u"录取日期")
    priority = models.IntegerField(default=0, verbose_name=u"优先顺序", help_text=u"数值越大，越显示在前")
    is_approved = models.BooleanField(u"是否经核准通过", default=False)
    remark = models.TextField(u"备注", blank=True)

    def __unicode__(self):
        return self.student.name

    class Meta:
        verbose_name = u"中考录取榜"
        verbose_name_plural = u"中考录取榜"
        ordering = ["priority", "-dtenrolled"]
