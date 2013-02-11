#coding:utf-8
from django.db import models
from common.stdimage import StdImageField
from django.contrib.auth.models import User

class Person(User):
    """官方档案信息"""

    IDENTITY_STAFF = 0
    IDENTITY_STUDENT = 1

    IDENTITY_CHOICES = (
        (IDENTITY_STAFF, u"教职工"),
        (IDENTITY_STUDENT, u"学生"),
    )

    GENDER_UNKNOWN = "0"
    GENDER_MALE = "1"
    GENDER_FEMALE = "2"

    identity = models.SmallIntegerField(u"身份", null=True, blank=True, max_length=1, choices=IDENTITY_CHOICES)
    name = models.CharField(max_length=30, db_index=True, verbose_name=u"户口姓名")
    #uuid = models.CharField(max_length=18, unique=True, verbose_name=u"编号")
    uuid = models.CharField(max_length=32, null=True, blank=True, unique=True, verbose_name=u"编号", help_text=\
    """
    学生编号格式: S20100001, 从左到右排序，第1位为大写字母S, 第2－5位为注册年份, 第6-9位 为注册序号
    教职工编号格式: T20100001, 从左到右排序，第1位为大写字母T, 第2－5位为注册年份, 第6-9位 为注册序号
    """)
    #学生学籍号  000000  0000  000 0 0000 (18位、从左到右排序)
    #第 1— 6位  表示省市县行政区划代码  (参见GB/T2260《中华人民共和国行政区划代码》)
    #第 7--10位  表示学生初始注册年份
    #第 11-13位  表示行政区划下的学校序号    ( 参见SC-XXBH《学校编号代码》)  
    #第 14位     性别码                (参见GB/T2261.1-2003《人的性别代码》)
    #第 15-18位  表示学生在校初始注册序号)
    spell_name = models.CharField(max_length=60, db_index=True, blank=True, verbose_name=u"姓名拼音")
    abbr_name = models.CharField(max_length=60, db_index=True, blank=True, verbose_name=u"姓名简称")
    used_name = models.CharField(max_length=30, db_index=True, blank=True, verbose_name=u"曾用名")
    id_no = models.CharField(max_length=18, null=True, db_index=True, blank=True, verbose_name=u"身份证号")
    gender = models.ForeignKey("standard.GenderCode", null=True, blank=True, verbose_name=u"性别")
    marriage = models.ForeignKey("standard.MarriageCode", null=True, blank=True, verbose_name=u"婚姻状况")
    blood_type = models.ForeignKey("standard.BloodTypeCode", null=True, blank=True, verbose_name=u"血型")
    birthday = models.DateField(null=True, blank=True, verbose_name=u"出生日期", help_text=u"日期格式为YYYY-MM-DD")
    diploma = models.ForeignKey("standard.DiplomaCode", null=True, blank=True, verbose_name=u"文化程度")
    born_place = models.ForeignKey("standard.LocationCode", null=True, blank=True, related_name="staff_born_place",  verbose_name=u"出生地")
    native_place = models.ForeignKey("standard.LocationCode", null=True, blank=True, related_name="staff_native_place", verbose_name=u"籍贯")
    folk = models.ForeignKey("standard.FolkCode", null=True, blank=True, verbose_name=u"民族")
    religion = models.CharField(max_length=24, blank=True, verbose_name=u"宗教信仰")
    emigrant = models.ForeignKey("standard.EmigrantCode", null=True, blank=True, verbose_name=u"港澳台侨")
    health = models.ForeignKey("standard.HealthCode", null=True, blank=True, verbose_name=u"健康状况")
    politics = models.ForeignKey("standard.PoliticsCode", null=True, blank=True, verbose_name=u"政治面貌")
    residence_address = models.CharField(max_length=60, blank=True, verbose_name=u"现住址", help_text=u"指本人当前的常住地址")
    domicle_location = models.CharField(max_length=64, blank=True, verbose_name=u"户口所在地", help_text=u"指户口所在地址，包括省（自治区、直辖市）/地（市、州）/县（区、旗）/乡（镇）/街（村）详细地址")
    domicle_type = models.ForeignKey("standard.DomicleTypeCode", null=True, blank=True, verbose_name=u"户口性质")
    is_floating = models.ForeignKey("standard.FloatingCode", null=True, blank=True, verbose_name=u"流动人口状况")
    is_singleton  = models.ForeignKey("standard.SingletonCode", null=True, blank=True, verbose_name=u"独生子女")
    #is_farmer_child = models.BooleanField(null=True, blank=True, verbose_name=u"是否农民工子女")
    #farmers_children = models.CharField(max_length=1, blank=True, verbose_name=u"农民工子女")
    nationality = models.ForeignKey("standard.NationalityCode", null=True, blank=True, verbose_name=u"国别")
    telephone = models.CharField(max_length=30, blank=True, verbose_name=u"联系电话")
    postal_address = models.CharField(max_length=60, blank=True, verbose_name=u"通信地址")
    postal_code = models.CharField(max_length=6, blank=True, verbose_name=u"邮政编码")
    homepage = models.CharField(max_length=30, blank=True, verbose_name=u"主页地址")
    #photo = models.ImageField(null=True, blank=True, upload_to="person_photo", verbose_name=u"照片")
    #photo = StdImageField(upload_to="person_photo/%Y/%m/%d", null=True, blank=True, size=(150,185), thumbnail_size=(100,300), verbose_name=u"上传照片")

    photo = StdImageField(upload_to="person_photo/%Y/%m/%d", null=True, blank=True, size=(150,185), thumbnail_size=(100,300), verbose_name=u"上传照片")
    #avatar = models.ImageField(upload_to="profile_avatar", blank=True, verbose_name=u"上传头像")
    #motto = models.CharField(blank=True, max_length=256, verbose_name=u"座右铭")
    fortes = models.TextField(blank=True, verbose_name=u"特长")
    interest = models.TextField(blank=True, verbose_name=u"兴趣爱好")
    log = models.TextField(blank=True, verbose_name=u"档案备忘录")
    is_leaved = models.BooleanField(verbose_name=u"已经离校", default=False, help_text=u"如果已经离校， 则打勾标记")
    departments = models.ManyToManyField("school.Department", verbose_name=u"部门成员", through='school.DepartmentMember')
    #remark = models.TextField(blank=True, verbose_name=u"备注")

    dtmodify = models.DateTimeField(auto_now=True, verbose_name=u"修改日期", editable=False)

    class Meta:
        ordering = ("spell_name","name")
        verbose_name = u"个人官方档案"
        verbose_name_plural = u"个人官方档案"

    class Template:
        exclude = ("name", "password")

    def __unicode__(self):
        return u"%s %s" % (self.name, self.get_identity_display())

    @models.permalink
    def get_absolute_url(self):
        return ("person", [str(self.pk)])


    def save(self, *args, **kwargs):
        #根据身份证号来填充出生日期
        if self.id_no and self.birthday is None:
            from common.utils import id_number2birthday
            self.birthday = id_number2birthday(self.id_no)

        super(Person, self).save(*args, **kwargs)

def user_post_save(sender, instance, **kwargs):
    person, new_person = Person.objects.get_or_create(pk=instance.pk)

models.signals.post_save.connect(user_post_save, sender=User)
