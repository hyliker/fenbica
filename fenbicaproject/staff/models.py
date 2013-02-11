#coding:utf-8
import datetime
from django.db import models
from person.models import Person
from treebeard.mp_tree import MP_Node

# Create your models here.
class Staff(Person):
    """教职工信息模型"""
    section_code = models.CharField(max_length=5, blank=True, verbose_name=u"科室号")
    dtenroll = models.DateField(db_index=True, default=datetime.datetime.now, verbose_name=u"入校年月")
    dtcome = models.DateField(db_index=True, null=True, blank=True, verbose_name=u"来校年月",help_text=u"来校工作的实际报到年月，以人事部门记载为准")
    dtteach = models.DateField(db_index=True, null=True, blank=True, verbose_name=u"从教年月", help_text=u"来校工作的实际报到年月，以人事部门")
    #dtwork = models.DateField(db_index=True, null=True, blank=True, verbose_name=u"参加工作日期", help_text=u"参加工作日期")
    type = models.ForeignKey("standard.StaffTypeCode", null=True, blank=True, verbose_name=u"编制类别")
    profile_no = models.CharField(max_length=12, null=True, blank=True, verbose_name=u"档案编号")
    profile_text = models.TextField(blank=True, verbose_name=u"档案文本")
    post_occupation = models.ForeignKey("standard.PostOccupationCode", null=True, blank=True, verbose_name=u"岗位职业")
    post = models.ForeignKey("Post", verbose_name=u"行政职务", null=True, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.uuid)

    def save(self, *args, **kwargs):
        self.identity = Person.IDENTITY_STAFF
        #自动创建一个uuid
        if self.uuid is None:
            try:
                year = self.dtenroll.year
            except:
                from datetime import datetime
                year = datetime.now().year
            staff_num = Staff.objects.filter(dtenroll__year=year).count() + 1
            self.uuid = u"T%(year)s%(next)s" % {"year": year, "next":str(staff_num).zfill(4)} 
        super(Staff, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"教职工档案"
        verbose_name_plural = u"教职工档案"
        permissions = (
            ("staff", u"查看某人的档案资料库"),
            ("experience_list", u"显示教职工简历列表"),
            ("experience", u"教职工简历条目"),
            ("diploma_list", u"显示教职工学历学位列表"),
            ("diploma", u"显示教职工学历学位条目"),
            ("family_list", u"教职工家庭成员列表"),
            ("family", u"教职工家庭成员条目"),
            ("workload_list", u"教职工工作量信息列表"),
            ("workload", u"教职工工作量信息条目"),
            ("spouse", u"教职工配偶信息条目"),
            ("course_classgrade_list", u"教职工班级课程记录"),
            ("teaching_list", u"教职工任课信息列表"),
            ("teaching", u"教职工任课信息列表"),
        )

def person_post_save(sender, instance, **kwargs):
    if instance.identity == instance.IDENTITY_STAFF:
        staff, new_staff = Staff.objects.get_or_create(pk=instance.pk)

models.signals.post_save.connect(person_post_save, sender=Person)

class Diploma(models.Model):
    """教职工学历学位信息"""
    staff = models.ForeignKey("Staff", verbose_name=u"教职工档案", related_name="diplomas")
    diploma = models.ForeignKey("standard.DiplomaCode", verbose_name=u"学历", help_text=u"文化程度")
    major = models.CharField(max_length=60, verbose_name=u"所学专业", help_text=u"职得学历所学习的专业名称")
    date_enrollment = models.DateField(verbose_name=u"入学年月")
    learning_mode = models.ForeignKey("standard.LearningModeCode", verbose_name=u"学习形式")
    learning_way = models.ForeignKey("standard.LearningWayCode", verbose_name=u"学习方式")
    learning_year = models.DecimalField(decimal_places=1, max_digits=3, verbose_name=u"学制", help_text="接受学历教育在校学习完成学业的规定(年限，单位：年，保留一位小数)")
    graduate_school = models.CharField(max_length=180, verbose_name=u"毕肄业学校或单位")
    degree = models.ForeignKey("standard.DegreeCode", verbose_name=u"学位")
    grant_country = models.ForeignKey("standard.NationalityCode", verbose_name=u"学位授予国家/地区")
    grant_org = models.CharField(max_length=180, verbose_name=u"学位授予单位")

    def __unicode__(self):
        return "%s %s" % (self.staff.name, self.diploma.name)

    class Meta:
        verbose_name = u"教职工学历学位信息"
        verbose_name_plural = u"教职工学历学位信息"
        ordering = ("-date_enrollment",)

class Experience(models.Model):
    """教职工简历信息"""
    staff = models.ForeignKey("Staff", verbose_name=u"教职工档案")
    dtstart = models.DateField(verbose_name=u"起始时间", help_text=u"日期格式：YYYY-MM-DD")
    dtend = models.DateField(verbose_name=u"结束时间", help_text=u"日期格式：YYYY-MM-DD")
    enterprise = models.CharField(max_length=60, verbose_name=u"所在单位名称")
    job_content = models.CharField(max_length=80, verbose_name=u"人事工作内容")
    cadre_post = models.ForeignKey("standard.CadrePostCode", null=True, blank=True, verbose_name=u"曾任党政职务")
    technical_post = models.ForeignKey("standard.TechnicalPostCode", null=True, blank=True, verbose_name=u"曾任技术职务")
    attestor = models.CharField(max_length=30, blank=True, verbose_name=u"证明人")
    remark = models.TextField(blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return "%s %s" % (self.staff.name, self.enterprise)

    class Meta:
        verbose_name = u"教职工简历信息"
        verbose_name_plural = u"教职工简历信息"
        ordering = ("-dtstart",)

class Spouse(models.Model):
    """教职工配偶情况"""
    staff = models.OneToOneField("Staff", verbose_name=u"教职工档案", primary_key=True)
    name = models.CharField(max_length=30, verbose_name=u"配偶姓名", help_text=u"你的户口姓名")
    gender = models.ForeignKey("standard.GenderCode", null=True, blank=True, verbose_name=u"性别")
    birthday = models.DateField(verbose_name=u"出生日期", null=True, blank=True)
    folk = models.ForeignKey("standard.FolkCode", null=True, blank=True, verbose_name=u"民族")
    domicle_location = models.CharField(max_length=60, blank=True, verbose_name=u"户口所在地")
    politics = models.ForeignKey("standard.PoliticsCode", null=True, blank=True, verbose_name=u"政治面貌")
    diploma = models.ForeignKey("standard.DiplomaCode", null=True, blank=True, verbose_name=u"文化程度")
    degree = models.ForeignKey("standard.DegreeCode", null=True, blank=True, verbose_name=u"学位")
    emigrant = models.ForeignKey("standard.EmigrantCode", null=True, blank=True, verbose_name=u"港澳台侨")
    enterprise = models.CharField(max_length=60, blank=True, verbose_name=u"所在单位名称")
    enterprise_location = models.ForeignKey("standard.LocationCode", null=True, blank=True, verbose_name=u"所在单位所在地区划")
    dtstart_job = models.DateField(verbose_name=u"参加工作年月", null=True, blank=True)
    telephone = models.CharField(max_length=30, blank=True, verbose_name=u"联系电话")
    postal_code = models.CharField(max_length=6, blank=True, verbose_name=u"邮政编码")
    technical_post = models.ForeignKey("standard.TechnicalPostCode", null=True, blank=True, verbose_name=u"曾任技术职务")
    cadre_post_level  = models.ForeignKey("standard.CadrePostLevelCode", null=True, blank=True, verbose_name=u"职务级别")#参见干部职务级别代码
    cadre_post = models.ForeignKey("standard.CadrePostCode", null=True, blank=True, verbose_name=u"曾任党政职务")
    social_job = models.ForeignKey("standard.SocialJobCode", null=True, blank=True, verbose_name=u"社会兼职") #参见社会兼职代码
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=u"工资总额(单位:元)")
    family_members_number = models.PositiveIntegerField(verbose_name=u"家庭人口", null=True, blank=True)
    children_number = models.PositiveIntegerField(verbose_name=u"子女人数", null=True, blank=True)
    foster_number = models.PositiveIntegerField(verbose_name=u"抚养人口数", null=True, blank=True, help_text=u"指本人经济上負担赡养的人口数，单位:人")

    def __unicode__(self):
        return "%s %s" % (self.staff.name, self.name)
    class Meta:
        verbose_name = u"教职工配偶情况"
        verbose_name_plural = u"教职工配偶情况"

class Family(models.Model):
    """教职工家庭其他成员情况"""
    staff = models.ForeignKey("Staff", verbose_name=u"教职工档案")
    relation = models.ForeignKey("standard.RelationCode", verbose_name=u"关系")
    name = models.CharField(max_length=30, verbose_name=u"姓名", help_text=u"你的户口姓名")
    telephone = models.CharField(max_length=30, verbose_name=u"联系电话")
    enterprise = models.CharField(max_length=60, blank=True, verbose_name=u"所在单位名称")
    occupation = models.ForeignKey("standard.OccupationCode", null=True, blank=True, verbose_name=u"职业") #参见职业分类与代码
    technical_post = models.ForeignKey("standard.TechnicalPostCode", null=True, blank=True, verbose_name=u"曾任技术职务")
    cadre_post_level  = models.ForeignKey("standard.CadrePostLevelCode", null=True, blank=True, verbose_name=u"职务级别")#参见干部职务级别代码
    politics = models.ForeignKey("standard.PoliticsCode", null=True, blank=True, verbose_name=u"政治面貌")
    marriage = models.ForeignKey("standard.MarriageCode", null=True, blank=True, verbose_name=u"婚姻状况")
    colony = models.ForeignKey("standard.NationalityCode", null=True, blank=True, verbose_name=u"侨居地")#,参见世界各国和地区名称代码

    def __unicode__(self):
        return "%s %s" % (self.staff.name, self.name)

    class Meta:
        verbose_name = u"教职工家庭其他成员情况"
        verbose_name_plural = u"教职工家庭其他成员情况"

class Workload(models.Model):
    """教学工作量"""
    staff = models.ForeignKey("Staff", verbose_name=u"教职工档案")
    type = models.ForeignKey("standard.TeachingTypeCode", verbose_name=u"教学类型")
    workload = models.IntegerField(verbose_name=u"教学工作量", help_text=u"单位：小时/年")
    dtstart = models.DateField(verbose_name=u"教学起始时间", help_text=u"日期格式：YYYY-MM-DD")
    dtend = models.DateField(verbose_name=u"教学结束时间", help_text=u"日期格式：YYYY-MM-DD")
    content = models.TextField(verbose_name=u"教学内容", blank=True)
    comment = models.TextField(verbose_name=u"教学评语", blank=True)

    def __unicode__(self):
        return self.staff.name

    class Meta:
        verbose_name = u"教学工作量"
        verbose_name_plural = u"教学工作量"

class Teaching(models.Model):
    """任课信息"""
    staff = models.ForeignKey("Staff", verbose_name=u"教职工档案")
    course = models.ForeignKey("course.Course", verbose_name=u"任课课程")
    dtstart = models.DateField(verbose_name=u"任课起始时间", help_text=u"日期格式：YYYY-MM-DD")
    dtend = models.DateField(verbose_name=u"任课结束时间",  null=True, blank=True, help_text=u"日期格式：YYYY-MM-DD")
    period = models.IntegerField(verbose_name=u"任课总学时", null=True, blank=True)
    learning_stage = models.ForeignKey("standard.LearningStageCode", null=True, blank=True, verbose_name=u"任课学段")
    role = models.ForeignKey("standard.TeachingRoleCode", null=True, blank=True, verbose_name=u"任课角色")
    #classes = models.CharField(max_length=120, verbose_name=u"任课班级") #有待调整
    classes = models.ManyToManyField("classgrade.Class", verbose_name=u"任课班级")
    teached_number = models.IntegerField(verbose_name=u"授课人数", null=True, blank=True, help_text=u"指听课的人数，单位：人")

    def __unicode__(self):
        return self.staff.name

    class Meta:
        verbose_name = u"教职工任课"
        verbose_name_plural = u"教职工任课"

class Post(MP_Node):
    """教职工行政职务"""
    name = models.CharField(max_length=30, unique=True, verbose_name=u"职务名称")
    description = models.TextField(blank=True, verbose_name=u"职务描述")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"教职工行政职务"
        verbose_name_plural = u"教职工行政职务"

#class Politics(models.Model):
    #"""政治面貌信息类"""
    #staff = models.ForeignKey("Staff", verbose_name = u"教职工")
    #politics = models.ForeignKey("standard.PoliticsCode", null=True, blank=True, verbose_name=u"政治面貌")
    #dtjoined = models.DateField(verbose_name=u"参加日期")
    #enterprise = models.CharField(max_length=60, blank=True, verbose_name=u"参加党派时所在单位")
    #introducer = models.CharField(max_length=30, blank=True, verbose_name=u"介绍人", help_text=u"指介绍本人参加党派的人员姓名")
    #dtbecomed_regular = models.DateField(verbose_name=u"转正日期")
    #exception_type =  models.ForeignKey("standard.ExceptionCode", verbose_name=u"异常类别")
    #exception_reason = models.CharField(max_length=80, verbose_name=u"异常原因")
