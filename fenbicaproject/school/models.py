#coding: utf-8
from django.db import models
from treebeard.mp_tree import MP_Node

# Create your models here.
#class School(models.Model):
    #"""学校信息模型"""
    #code = models.CharField(max_length=9, verbose_name=u"学校编号代码")
    #org_code = models.CharField(max_length=9, blank=True, verbose_name=u"学校组织机构代码")
    #bureau = models.ForeignKey("bureau.Bureau", verbose_name=u"所属主管单位")
    #name = models.CharField(max_length=60, verbose_name=u"学校名称")
    #english_name = models.CharField(max_length=180, blank=True, verbose_name=u"学校英文名称")
    #address = models.CharField(max_length=60, blank=True, verbose_name=u"学校地址")
    #location = models.ForeignKey("standard.LocationCode", verbose_name=u"所在地区行政区划")
    #master = models.CharField(max_length=30, blank=True, verbose_name=u"学校校长")
    #establishment_date = models.DateField(blank=True, null=True, verbose_name=u"建校年月")
    #host = models.ForeignKey("standard.SchoolHostCode", null=True, blank=True, verbose_name=u"学校办别")
    #type = models.ForeignKey("standard.SchoolTypeCode", null=True, blank=True, verbose_name=u"学校类别码")
    #location_econ = models.ForeignKey("standard.LocationEconCode", null=True, blank=True, verbose_name=u"所在地区经济属性")
    #location_folk = models.ForeignKey("standard.LocationFolkCode", null=True, blank=True, verbose_name=u"所在地民族属性")
    #first_teach_language = models.CharField(max_length=3, blank=True, verbose_name=u"主教学语言码")
    #second_teach_language = models.CharField(max_length=3, blank=True, verbose_name=u"辅教学语言码")
    #postal_code = models.CharField(max_length=6, blank=True, verbose_name=u"邮政编码")
    #telephone = models.CharField(max_length=30, blank=True, verbose_name=u"联系电话")
    #fax = models.CharField(max_length=30, blank=True, verbose_name=u"传真电话")
    #email = models.EmailField(max_length=30, blank=True, verbose_name=u"电子信箱")
    #homepage = models.CharField(max_length=30, blank=True, verbose_name=u"主页地址")
    #biographical_notes = models.TextField(max_length=4096, blank=True, verbose_name=u"学校简历")

    #def __unicode__(self):
        #return self.name

    #class Meta:
        #verbose_name = u"学校"
        #verbose_name_plural = u"学校"

#class Class(models.Model):
    #"""班级信息模型"""
    #uuid = models.CharField(max_length=8, primary_key=True, verbose_name=u"班级代码", help_text=u"如20083101, 8位， 从左到右排序，第1－4位表示本班年份，5-6位表示年级代码 7-8位表示学校班级序号")
    #dtcreated = models.DateField(null=True, blank=True, verbose_name=u"建班年月")
    #type = models.ForeignKey("standard.ClassTypeCode", verbose_name=u"班级类型")
    #grade = models.ForeignKey("standard.GradeCode", verbose_name=u"年级")
    #class_no = models.CharField(max_length=2, verbose_name=u"班号", help_text=u"2位表示学校班序号")
    #name = models.CharField(max_length=20, verbose_name=u"名称", help_text=u"例如：2007届01班, 或者是高一7班, 物理1班等")
    #honorary_title = models.CharField(max_length=40, blank=True, verbose_name=u"荣誉称号")
    #schooling_length = models.SmallIntegerField(max_length=2, null=True, blank=True, verbose_name=u"学制", help_text=u"接受学历教育在校学习完成学业规定的年限，单位：年")
    #master = models.ForeignKey("staff.Staff", null=True, blank=True, verbose_name=u"班主任")#班主任编号
    #monitor = models.ForeignKey("student.Student", null=True, blank=True, verbose_name=u"班长") #班长学号
    #classroom = models.ForeignKey("Classroom", null=True, blank=True, verbose_name=u"教室")
    #courses = models.ManyToManyField("course.Course", null=True, blank=True, verbose_name=u"课程")

    #class Meta:
        #verbose_name = u"班级"
        #verbose_name_plural = u"班级"
        #ordering = ["grade", "class_no"]
        #unique_together=("uuid", "grade", "class_no")

    #def __unicode__(self):
        #return "%s %s" % (self.dtcreated, self.name)

class Category(MP_Node):
    name = models.CharField(max_length=30)
    description = models.TextField()

    node_order_by = ["name"]

    def __unicode__(self):
        return u"Category: %s" % self.name


class Office(models.Model):
    """科室信息类"""
    uuid = models.CharField(max_length=9, verbose_name=u"科室号", primary_key=True, help_text=u"指教研室、研究室及党政各科室的代码，学校自编")
    name = models.CharField(max_length=20, verbose_name=u"名称")
    abbr = models.CharField(max_length=10, verbose_name=u"简称")
    master = models.ForeignKey("staff.Staff", verbose_name=u"科室负责人")

    class Meta:
        verbose_name = u"科室"
        verbose_name_plural = u"科室"

    def __unicode__(self):
        return self.name

class Classroom(models.Model):
    """教室信息"""
    uuid = models.CharField(max_length=32, verbose_name=u"编号", primary_key=True)
    name = models.CharField(max_length=30, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注", blank=True)

    class Meta:
        verbose_name = u"教室"
        verbose_name_plural = u"教室"

    def __unicode__(self):
        return self.name

class EntranceResultSubject(models.Model):
    """入学成绩科目设置"""
    student = models.ForeignKey("student.Student", verbose_name=u"学生档案")
    name = models.CharField(max_length=32, verbose_name=u"名称")
    abbr = models.CharField(max_length=16, verbose_name=u"简称")
    remark = models.TextField(verbose_name=u"备注")

    class Meta:
        verbose_name = u"入学成绩科目"
        verbose_name_plural = u"入学成绩科目"

class Subject(models.Model):
    """学科"""
    uuid = models.CharField(max_length=32, verbose_name=u"编号")
    name = models.CharField(max_length=32, verbose_name=u"名称")

    class Meta:
        verbose_name = u"学科"
        verbose_name_plural = u"学科"

class Building(models.Model):
    """学校建筑物体基本情况"""
    ANTI_KNOCK_STATUS_REACH = 1
    ANTI_KNOCK_STATUS_UNREACH = 1
    ANTI_KNOCK_STATUS_CHOICES  = (
        (ANTI_KNOCK_STATUS_REACH, u"达到当地抗震标准"),
        (ANTI_KNOCK_STATUS_UNREACH, u"未达到抗震标准"),
    )

    PLACE_STATUS_IN_SCHOOL = 1
    PLACE_STATUS_OUT_SCHOOL = 0
    PLACE_STATUS_CHOICES = (
        (PLACE_STATUS_IN_SCHOOL, u"校内"),
        (PLACE_STATUS_OUT_SCHOOL, u"校外"),
    )

    uuid = models.CharField(max_length=6, primary_key=True, verbose_name=u"编号", help_text=u"学校自编的建筑物编号")
    name = models.CharField(max_length=32, unique=True, verbose_name=u"名称", help_text=u"指建筑物的汉字名称")
    property_usage = models.ForeignKey("standard.PropertyUsageCode", verbose_name=u"产权及使用状况代码")
    school_unit_level = models.ForeignKey("standard.SchoolUnitLevelCode", verbose_name=u"学校单位层次代码")
    category = models.ForeignKey("standard.BuildingCategoryCode", verbose_name=u"建筑物分类代码")
    structrue = models.ForeignKey("standard.BuildingStructureCode", verbose_name=u"建筑物结构码")
    floor_number = models.PositiveSmallIntegerField("建筑物层数", help_text=u"含地下室，单位：层")
    dtcreated = models.DateField("建成日期")
    invested_money = models.PositiveIntegerField(u"投资总额", help_text=u"指建筑物的投资总金额，单位：元")
    funding_source = models.ForeignKey("standard.FundingSourceCode", verbose_name=u"经费来源")
    using_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=u"使用面积", help_text=u"取二位小数，单位：平方米")
    building_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=u"建筑面积", help_text=u"取二位小数，单位：平方米")
    anti_knock_status = models.SmallIntegerField(u"抗震程度", choices=ANTI_KNOCK_STATUS_CHOICES)
    place = models.CharField(max_length=60, verbose_name=u"建筑物地址")
    place_status = models.SmallIntegerField(choices=PLACE_STATUS_CHOICES, verbose_name=u"建筑物位置状况")
    status = models.ForeignKey("standard.BuildingStatusCode", verbose_name=u"建筑物状况")
    photo = models.ImageField(verbose_name=u"建筑物图片", upload_to="school_building_photo", null=True, blank=True)
    plane_photo = models.ImageField(verbose_name=u"建筑物平面图", upload_to="school_building_plane_photo", null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"建筑物"
        verbose_name_plural = u"建筑物"

class Room(models.Model):
    """房间"""
    uuid = models.CharField(max_length=6, primary_key=True, verbose_name=u"编号")
    building = models.ForeignKey("Building", verbose_name=u"建筑物")
    name = models.CharField(max_length=32, unique=True, verbose_name=u"名称")
    usage = models.ForeignKey("standard.RoomUsageCode", verbose_name=u"房间用途")
    teaching_use_property = models.ForeignKey("standard.TeachingUsePropertyCode", verbose_name=u"教学使用性质")
    floor = models.CharField(u"房间所处楼层", max_length=3, \
                             help_text=u"指房间所在的楼层，地上楼层直接用阿 拉伯数字表示，地下楼层在阿拉伯数字 前加“B”号，如“2”表示地上2层, B2表示地下2层")
    building_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name=u"房间建筑面积", help_text=u"取二位小数，单位：平方米")
    using_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name=u"房间使用面积", help_text=u"取二位小数，单位：平方米")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"房间"
        verbose_name_plural = u"房间"

class Facility(models.Model):
    """设施"""
    USAGE_STATUS_NORMAL = 1
    USAGE_STATUS_ABNORMAL = 0

    USAGE_STATUS_CHOICES = (
        (USAGE_STATUS_NORMAL, U"正常使用"),
        (USAGE_STATUS_ABNORMAL, U"不能正常使用")
    )

    uuid = models.CharField(max_length=6, verbose_name=u"编号")
    name = models.CharField(max_length=32, unique=True, verbose_name=u"名称")
    dtcreated = models.DateField(u"修建日期")
    fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name=u"修建费用", help_text=u"指修建设施的总经费,取二位小数，单位：元")
    usage_status = models.SmallIntegerField(max_length=1, choices=USAGE_STATUS_CHOICES, verbose_name=u"使用状况")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"设施"
        verbose_name_plural = u"设施"

class Department(MP_Node):
    """部门结构树"""
    name = models.CharField(max_length=32, verbose_name=u"部门名称", unique=True)
    hod = models.ForeignKey("person.Person", verbose_name=u"部门负责人", related_name="hods")
    dtstart = models.DateField(verbose_name=u"创建时间")
    dtend = models.DateField(verbose_name=u"取消时间", null=True, blank=True)
    remark = models.TextField(verbose_name=u"备注", blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"部门"
        verbose_name_plural = u"部门"

class DepartmentMember(models.Model):
    """部门人员"""

    department = models.ForeignKey("Department", verbose_name=u"部门")
    person = models.ForeignKey("person.Person", verbose_name=u"人员")
    position = models.ForeignKey("Position", verbose_name=u"职位")
    dtstart = models.DateField(u"开始日期", help_text=u"加入部门的日期")
    dtend = models.DateField(u"结束日期", help_text=u"退出部门的日期", null=True, blank=True)
    remark = models.TextField(verbose_name=u"备注", blank=True)

    def __unicode__(self):
        return u"%s " % self.person.name

    #def save(self, *args, **kwargs):
        #super(Membership, self).save(*args, **kwargs)
        #self.klass.student_number = F("student_number") + 1
        #self.klass.save()

    class Meta:
        verbose_name= u"部门人员"
        verbose_name_plural = u"部门人员"
        ordering = ("-dtstart", "-dtend")

class Position(MP_Node):
    """职位"""
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2

    STATUS_CHOICES = (
        (STATUS_ACTIVE, u"生效"),
        (STATUS_INACTIVE, u"无效"),
    )

    title = models.CharField(max_length=30, unique=True, verbose_name=u"职位名称")
    description = models.TextField(blank=True, verbose_name=u"职位描述")
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, verbose_name=u"状态", default=STATUS_ACTIVE)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"职位"
        verbose_name_plural = u"职位"
