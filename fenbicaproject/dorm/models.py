#coding: utf-8
"""学生住宿模块"""
from django.db import models
from django.db.models import F
from datetime import datetime
from student.models import Student

# Create your models here.
class Building(models.Model):
    """宿舍楼"""

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'

    GENDER_CHOICES = (
        (GENDER_MALE, u"男生宿舍楼"),
        (GENDER_FEMALE, u"女生宿舍楼"),
    )

    uuid = models.CharField(u"宿舍编号", max_length=12)
    name = models.CharField(u"宿舍名称", max_length=12, blank=True)
    bedchamber_number = models.PositiveSmallIntegerField(verbose_name=u"房间数", null=True, blank=True)
    floor_number = models.PositiveSmallIntegerField(verbose_name=u"楼层数", null=True, blank=True)
    masters = models.ManyToManyField("staff.Staff", null=True, blank=True, verbose_name=u"宿舍楼管理员", help_text=u"可以填写多个管理员ID, 用英文逗号(,) 分开")
    gender = models.CharField(max_length=1, verbose_name=u"性别", choices=GENDER_CHOICES)
    remark = models.TextField(u"备注", blank=True)

    def __unicode__(self):
        return "%s %s" % (self.uuid, self.name)
    class Meta:
        verbose_name = u"宿舍楼"
        verbose_name_plural = u"宿舍楼"

class Bedchamber(models.Model):
    """寝室"""
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'

    GENDER_CHOICES = (
        (GENDER_MALE, u"男生"),
        (GENDER_FEMALE, u"女生"),
    )

    TYPE_NORMAL = 1
    TYPE_BAD_USE  = 2
    TYPE_BAD_UNUSE = 3
    TYPE_SPECIAL = 4

    TYPE_CHOICES = (
        (TYPE_NORMAL, u"正常"),
        (TYPE_BAD_USE, u"有损坏可以使用"),
        (TYPE_BAD_UNUSE, u"有损坏不能使用"),
        (TYPE_SPECIAL, u"特殊房间"),
    )

    uuid = models.CharField(u"寝室编号", primary_key=True, max_length=12, help_text=u"编号建议用200818518格式，从左到右1-4位是年份, 5-6位为楼（幢)号，7-8位为楼层,9-10位为寝室序号")
    dtcreated = models.DateTimeField(auto_now_add=True, verbose_name=u"创建日期")
    master = models.ForeignKey("student.Student", verbose_name=u"寝室长")
    building = models.ForeignKey("Building", verbose_name=u"宿舍楼")
    telephone = models.CharField(verbose_name=u"寝室电话", max_length="24", blank=True)
    capacity = models.PositiveSmallIntegerField(verbose_name=u"容纳人数", null=True, blank=True)
    living_number = models.PositiveSmallIntegerField(verbose_name=u"已住人数", default=0, editable=False)
    gender = models.CharField(max_length=1, verbose_name=u"性别", choices=GENDER_CHOICES, blank=True)
    price = models.PositiveSmallIntegerField(u"房间价格标准", null=True, blank=True, help_text=u"单位为人民币(元)")
    type = models.SmallIntegerField(u"房间状态", choices=TYPE_CHOICES, default=TYPE_NORMAL)
    infrastructure = models.TextField(verbose_name=u"基础设施", blank=True)
    remark = models.TextField(u"备注", blank=True)
    is_active = models.BooleanField(u"是否激活", help_text=u"当寝室注销的时候，设置为否", default=True)

    def __unicode__(self):
        return self.uuid

    @models.permalink
    def get_absolute_url(self):
        return ("dorm_bedchamber", [str(self.pk)])

    class Meta:
        unique_together = ("building", "uuid")
        verbose_name = u"寝室"
        verbose_name_plural = u"寝室"
        ordering = ("dtcreated",)

class Bed(models.Model):
    """床位"""
    uuid = models.CharField(max_length=12, primary_key=True, verbose_name="床位编号")
    dtcreated = models.DateTimeField(auto_now_add=True, verbose_name=u"创建日期")
    bedchamber = models.ForeignKey("Bedchamber", verbose_name=u"寝室编号")
    is_used = models.BooleanField(verbose_name=u"床位是否被用")

    def __unicode__(self):
        return u"%s 寝室 %s 床位 %s" % (self.bedchamber.building, self.bedchamber.uuid, self.uuid)

    class Meta:
        verbose_name = u"床位"
        verbose_name_plural = u"床位"

class Boarder(models.Model):
    """住宿生"""
    student = models.ForeignKey("student.Student", verbose_name=u"住宿生")
    dtstart = models.DateTimeField(verbose_name=u"入住日期")
    dtend = models.DateTimeField(verbose_name=u"退房日期", null=True, blank=True)
    bed = models.ForeignKey("Bed", verbose_name=u"床位")

    def __unicode__(self):
        return self.student.name

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.db.models import Q
        #filter = Q(dtend__isnull=True) | (Q(dtend__lt=self.dtstart) & Q(bed=self.bed))
        filter = Q(bed=self.bed) & ( Q(dtend__isnull=True) | Q(dtend__lt=self.dtstart) )  
        collision_count = self._default_manager.filter(filter).count()
        print "kkkk", collision_count
        if collision_count:
            raise ValidationError(u"输入的时间有冲突，请检查，务必确保此床位尚没有其他人正在使用")

    class Meta:
        unique_together = ("student", "bed")
        ordering = ("-dtstart","-dtend")
        verbose_name = u"住宿生"
        verbose_name_plural = u"住宿生"

def boarder_post_save(sender, instance, **kwargs):
    if kwargs["created"]:
        instance.bed.bedchamber.living_number = F("living_number") + 1
        instance.bed.bedchamber.save()

def boarder_post_delete(sender, instance, **kwargs):
    instance.bed.bedchamber.living_number = F("living_number") - 1
    instance.bed.bedchamber.save()

models.signals.post_save.connect(boarder_post_save, sender=Boarder)
models.signals.post_delete.connect(boarder_post_delete, sender=Boarder)

class Check(models.Model):
    """寝室评比"""
    dtchecked = models.DateField(verbose_name=u"评比日期")
    bedchamber = models.ForeignKey("Bedchamber", verbose_name=u"寝室")
    thing_ranking = models.SmallIntegerField(verbose_name=u"物品摆放得分")
    bed_ranking = models.SmallIntegerField(verbose_name=u"床铺整理得分")
    health_ranking = models.SmallIntegerField(verbose_name=u"卫生情况得分")
    infrastructure_ranking = models.PositiveSmallIntegerField(verbose_name=u"设施破坏得分")
    absence_ranking = models.SmallIntegerField(verbose_name=u"缺寝得分")
    discipline_ranking = models.SmallIntegerField(verbose_name=u"纪律得分")
    sum_ranking = models.SmallIntegerField(u"总分", editable=False)
    checker = models.ForeignKey("person.Person", related_name="dorm_check_checker", verbose_name=u"检查者", null=True, help_text=u"如果是自己， 可以不用输入", blank=True)
    creator = models.ForeignKey("person.Person", related_name="dorm_check_creator", verbose_name=u"录入者", editable=False)
    remark = models.TextField(verbose_name=u"备注", blank=True)

    def __unicode__(self):
        return self.bedchamber.uuid

    def save(self, *args, **kwargs):
        self.sum_ranking = sum([self.bed_ranking, self.health_ranking, self.infrastructure_ranking, self.absence_ranking, self.discipline_ranking])
        super(Check, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-dtchecked",)
        verbose_name = u"寝室评比"
        verbose_name_plural = u"寝室评比"
        unique_together = ("dtchecked", "bedchamber")

class Latelog(models.Model):
    """住宿生晚归登记"""
    boarder = models.ForeignKey("Boarder", related_name="dorm_latelog_boarder", verbose_name=u"住宿生")
    reason = models.TextField(u"晚归原因")
    dtlogged = models.DateTimeField(u"晚归时间", default=datetime.now())
    dtcreated = models.DateTimeField(u"创建时间", auto_now_add=True)
    creator = models.ForeignKey("person.Person", verbose_name=u"录入者", editable=False)

    def __unicode__(self):
        return self.boarder.student.name

    class Meta:
        verbose_name = u"住宿生晚归登记"
        verbose_name_plural = u"住宿生晚归登记"

#class LivedLog(models.Model):
    #"""学生日常住宿登记"""
    #pass

#class Maintenance(models.Model):
    #"""宿舍日常维修，　报修"""
    #dtreported = models.DateTimeField(verbose_name=u"报修时间")
    #reporter = models.CharField(verbose_name=u"报修人")
    #problem = models.TextField(verbose_name=u"报修问题")
    #dtrepaired = models.DateTimeField(verbose_name=u"起修时间")
    #dtcomplete = models.DateTimeField(verbose_name=u"完工时间")
    #status = models.CharField(verbose_name=u"处理結果")
    #remark = models.TextField(verbose_name=u"备注")
    #registrar = models.ForeignKey("User", verbose_name=u"记录员")
