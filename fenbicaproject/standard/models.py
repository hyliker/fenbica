#coding: utf-8
from django.db import models
from django.db.models import Q

# Create your models here.

class Code(models.Model):
    """国家标准代码"""
    #code= models.CharField(max_length=12, verbose_name=u"代码")
    #name = models.CharField(max_length=64, verbose_name=u"名称")
    remark = models.TextField(blank=True,verbose_name=u"备注")

    class Meta:
        abstract = True

class LocationCodeManager(models.Manager):
    def get_province(self, pk=None, code=None):
        return super(LocationCodeManager, self).get_query_set().filter(code__endswith="0000")
    def get_children(self, pk=None, by=None):
        if by == "province":
            province = self.model.objects.get(pk=pk)
            qs = Q(code__startswith=province.code[0:2]) & \
                 Q(code__endswith=province.code[4:])
            cities = self.model.objects.filter(qs).exclude(code=province.code)
            return cities
        elif by == "city":
            city = self.model.objects.get(pk=pk)
            qs = Q(code__startswith=city.code[0:4])
            countries = self.model.objects.filter(qs).exclude(code=city.code)
            return countries

    provinces = property(get_province)

class NationalityCode(models.Model):
    """ 世界各国地区和名称代码/国别码"""
    code=  models.CharField(primary_key=True, max_length=3, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(blank=True,verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"世界各国地区和名称代码"
        verbose_name_plural = u"世界各国地区和名称代码"
        ordering = ["code"]

class SocialJobCode(models.Model):
    """ 社会兼职代码"""
    code=  models.CharField(primary_key=True, max_length=4, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(blank=True,verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"社会兼职代码"
        verbose_name_plural = u"社会兼职代码"
        ordering = ["code"]

class LocationCode(models.Model):
    """GB/T2260-2007     《中华人民共和国行政区划代码》"""
    code= models.CharField(primary_key=True, max_length=6, unique=True, verbose_name=u"代码")
    name = models.CharField(max_length=32, verbose_name=u"名称")
    pinyin = models.CharField(max_length=32, verbose_name=u"罗马字母拼音")
    letter_code = models.CharField(max_length=3, verbose_name=u"字母码")
    remark = models.TextField(verbose_name=u"备注")

    objects = models.Manager()
    objs = LocationCodeManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"中华人民共和国行政区划代码"
        verbose_name_plural = u"中华人民共和国行政区划代码"
        ordering = ["code"]

class GenderCode(models.Model):
    """◆  GB/T2261.1-2003《人的性别代码》"""
    code=  models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(blank=True,verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"人的性别代码"
        verbose_name_plural = u"人的性别代码"

class FolkCode(models.Model):
    """GB/T3304《中国各民族名称和代码》"""
    code= models.CharField(primary_key=True, max_length=6, unique=True, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    pinyin = models.CharField(max_length=32, verbose_name=u"罗马字母拼音")
    letter_code = models.CharField(max_length=3, verbose_name=u"字母码")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"中国各民族名称和代码"
        verbose_name_plural = u"中国各民族名称和代码"
        ordering = ["code"]

class RelationCode(models.Model):
    """GB 4761-84《家庭关系代码》"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"家庭关系代码"
        verbose_name_plural = u"家庭关系代码"
        ordering=["code"]

class PoliticsCode(models.Model):
    """GB 4762-84 《政治面貌代码》"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"政治面貌代码"
        verbose_name_plural = u"政治面貌代码"

class CadrePostCode(models.Model):
    """干部职务"""
    code= models.CharField(primary_key=True, max_length=4, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"党政干部职务"
        verbose_name_plural = u"党政干部职务"
        ordering = ("code",)

class CadrePostLevelCode(models.Model):
    """干部职务级别"""
    code = models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"干部职务级别"
        verbose_name_plural = u"干部职务级别"
        ordering = ("code",)

class TechnicalPostCode(models.Model):
    """技术职务"""
    code= models.CharField(primary_key=True, max_length=3, verbose_name=u"代码")
    name = models.CharField(max_length=32, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"技术职务"
        verbose_name_plural = u"技术职务"
        ordering = ("code",)

class MarriageCode(models.Model):
    """GB/T2261.2-2003《婚姻状况代码》"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"婚姻状况代码"
        verbose_name_plural = u"婚姻状况代码"

class HealthCode(models.Model):
    """GB/T2261.2-2003《健康代码》"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"健康代码"
        verbose_name_plural = u"健康代码"

class LocationTypeCode(models.Model):
    """" DM—SZDLB 《学校所在地区类别代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=6, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学校所在地区类别代码"
        verbose_name_plural = u"学校所在地区类别代码"

class LocationEconCode(models.Model):
    """DM—SZDJJSX《学校所在地区经济属性代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学校所在地区经济属性代码"
        verbose_name_plural = u"学校所在地区经济属性代码"

class SchoolHostCode(models.Model):
    """DM—XXBB《学校办别代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学校办别代码"
        verbose_name_plural = u"学校办别代码"

class SchoolTypeCode(models.Model):
    """DM—XXBB《学校类别代码》"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学校类别代码"
        verbose_name_plural = u"学校类别代码"


class StudentTypeCode(models.Model):
    """ DM—XSLB《学生类别代码》"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学生类别代码"
        verbose_name_plural = u"学生类别代码"

class ClassTypeCode(models.Model):
    """DM—BJLX《班级类型代码》"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"班级类型代码"
        verbose_name_plural = u"班级类型代码"

#class ClassCode(models.Model):
    #"""DM—BJLX《班级类型代码》"""
    #code= models.CharField(max_length=2, verbose_name=u"代码")
    #name = models.CharField(max_length=32, verbose_name=u"名称")
    #remark = models.TextField(verbose_name=u"备注")

class BloodTypeCode(models.Model):
    """DM—XX《血型代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"血型代码"
        verbose_name_plural = u"血型代码"

class EmigrantCode(models.Model):
    """ DM—GATQ 《港澳台侨外代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")
    remark = models.TextField(verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"港澳台侨外代码"
        verbose_name_plural = u"港澳台侨外代码"

class ExamModeCode(Code):
    """DM—KSFS《考试方式代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"考试方式代码"
        verbose_name_plural = u"考试方式代码"

class ExamTypeCode(Code):
    """DM—KSLB《考试类别代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"考试类别代码"
        verbose_name_plural = u"考试类别代码"

class RewardsTypeCode(Code):
    """DM—XSHJLB《学生获奖类别代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学生获奖类别代码"
        verbose_name_plural = u"学生获奖类别代码"

class RewardsLevelCode(Code):
    """DM—JLJB《奖励级别代码》"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"奖励级别代码"
        verbose_name_plural = u"奖励级别代码"

class PunishmentNameCode(Code):
    """DM—CFMC《处分名称代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"奖励级别代码"
        verbose_name_plural = u"奖励级别代码"

class EnrollmentTypeCode(Code):
    """DM—RXFS《入学方式代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"入学方式代码"
        verbose_name_plural = u"入学方式代码"

class SourceTypeCode(Code):
    """DM—XSLY《学生来源代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学生来源代码"
        verbose_name_plural = u"学生来源代码"

class AttendanceTypeCode(Code):
    """DM—JDFS《就读方式代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"就读方式代码"
        verbose_name_plural = u"就读方式代码"

class EducationResultCode(Code):
    """DM—JYJG《教育结果代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"教育结果代码"
        verbose_name_plural = u"教育结果代码"

class TransferTypeCode(Code):
    """DM—YDLB《学籍异动类别代码》"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["code"]
        verbose_name = u"学籍异动类别代码"
        verbose_name_plural = u"学籍异动类别代码"

class LevelScoreCode(Code):
    """DM—DJFS《等级分数代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"等级分数代码"
        verbose_name_plural = u"等级分数代码"

class FloatingCode(Code):
    """DM—LDRKZK《流动人口状况代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"流动人口状况代码"
        verbose_name_plural = u"流动人口状况代码"

class SingletonCode(Code):
    """DM—DSZN《独生子女状况代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"独生子女状况代码"
        verbose_name_plural = u"独生子女状况代码"

class LocationFolkCode(Code):
    """DM—MZZZX《民族自治县状况代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"民族自治县状况代码"
        verbose_name_plural = u"民族自治县状况代码"

class RegisterStatusCode(Code):
    """参见DM—XSZCZK《学生注册状况代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学生注册状况代码"
        verbose_name_plural = u"学生注册状况代码"

class TransferStatusCode(Code):
    """DM－XJBDCLZT《学籍变动处理状态代码》"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学籍变动处理状态代码"
        verbose_name_plural = u"学籍变动处理状态代码"

class LearningStageCode(Code):
    """学段代码"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学段代码"
        verbose_name_plural = u"学段代码"
        ordering = ["code"]

class SemesterCode(Code):
    """学期代码"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学期代码"
        verbose_name_plural = u"学期代码"
        ordering = ["code"]

class GradeCode(Code):
    """年级代码"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"年级代码"
        verbose_name_plural = u"年级代码"
        ordering = ["code"]

class LearningModeCode(Code):
    """学习形式码"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学习形式码"
        verbose_name_plural = u"学习形式码"

class LearningWayCode(Code):
    """学习方式代"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学习方式代"
        verbose_name_plural = u"学习方式代"

class GraduateDirectionCode(Code):
    """毕业去向代码"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering=["code"]
        verbose_name = u"毕业去向代码"
        verbose_name_plural = u"毕业去向代码"

class GraduateDirectionCode(Code):
    """毕业去向代码"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    class Meta:
        verbose_name = u"毕业去向代码"
        verbose_name_plural = u"毕业去向代码"

class PostOccupationCode(Code):
    """岗位职业代码"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"岗位职业代码"
        verbose_name_plural = u"岗位职业代码"

class OccupationCode(Code):
    """职业分类代码"""
    code= models.CharField(primary_key=True, max_length=3, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=128, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["code"]
        verbose_name = u"职业分类代码"
        verbose_name_plural = u"职业分类代码"

class DegreeCode(Code):
    """学位代码"""
    code= models.CharField(primary_key=True, max_length=3, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"学位代码"
        verbose_name_plural = u"学位代码"


class DiplomaCode(Code):
    """文化程度码"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=64, verbose_name=u"名称")
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"文化程度码"
        verbose_name_plural = u"文化程度码"

class DomicleTypeCode(Code):
    """户口性质"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"户口性质"
        verbose_name_plural = u"户口性质"

class StaffTypeCode(Code):
    """员工编制"""
    code= models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"文化程度码"
        verbose_name_plural = u"文化程度码"

class TeachingTypeCode(Code):
    """教学类型码"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=24, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["code"]
        verbose_name = u"教学类型码"
        verbose_name_plural = u"教学类型码"

class TeachingRoleCode(Code):
    """任课角色类型码"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["code"]
        verbose_name = u"任课角色型码"
        verbose_name_plural = u"任课角色型码"

class TeachingModeCode(Code):
    """授课方式码"""
    code= models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=12, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["code"]
        verbose_name = u"任课角色型码"
        verbose_name_plural = u"任课角色型码"

class SubjectCode(Code):
    """学科代码，非国家标准"""
    #参考 http://www.being.org.cn/ncs/code.htm

    code= models.CharField(primary_key=True, max_length=6, unique=True, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    pinyin = models.CharField(max_length=32, verbose_name=u"罗马字母拼音")
    english_name = models.CharField(max_length=32, verbose_name=u"英文名称")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["code"]
        verbose_name = u"学科代码"
        verbose_name_plural = u"学科代码"

class RoomUsageCode(models.Model):
    """房间用途代码"""
    code = models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

class TeachingUsePropertyCode(models.Model):
    """教学使用性质"""
    code = models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

class PropertyUsageCode(models.Model):
    """产权及使用状况代码"""
    code = models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")

    def __unicode__(self):
        return self.name

class SchoolUnitLevelCode(models.Model):
    """学校单位层次代码"""
    code = models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    def __unicode__(self):
        return self.name

class BuildingCategoryCode(models.Model):
    """建筑物分类代码"""
    code = models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    def __unicode__(self):
        return self.name

class BuildingStructureCode(models.Model):
    """建筑物结构码"""
    code = models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    def __unicode__(self):
        return self.name

class FundingSourceCode(models.Model):
    """经费来源"""
    code = models.CharField(primary_key=True, max_length=1, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    def __unicode__(self):
        return self.name

class BuildingStatusCode(models.Model):
    """建筑物状况码"""
    code = models.CharField(primary_key=True, max_length=2, verbose_name=u"代码")
    name = models.CharField(unique=True, max_length=32, verbose_name=u"名称")
    def __unicode__(self):
        return self.name
