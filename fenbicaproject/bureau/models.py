#coding: utf-8
from django.db import models

# Create your models here.

class Bureau(models.Model):
    """主管单位信息模型是学校上级主管部门的数据模型。一般为各级教育行政部门或者其他单位。"""
    code = models.CharField(max_length=9, verbose_name=u"主管单位机构代码", help_text="""\
            学校主管部门（教育厅、教委、教育局等中小学的上级主管部门）的唯一标识
            主管单位机构编号  000000  000   (9位、从左到右排序)
            第1--6位  表示省市县行政区划代码 (参见GB/T2260《中华人民共和国行政区划代码》)
            第7--9位  表示所在行政区域内的主管单位机构序号
            """)
    name = models.CharField(max_length=150, verbose_name=u"主管单位名称")
    location = models.ForeignKey("standard.LocationCode", verbose_name=u"所在地行政区划")
    address = models.CharField(max_length=100, blank=True, verbose_name=u"主管单位地址", help_text=u"指包括省（自治区、直辖市）／地（市、区）／县（市、旗）／乡（镇）／街（村）的详细地址")
    location_type = models.ForeignKey("standard.LocationTypeCode", blank=True, verbose_name=u"所在地区类别")
    location_econ = models.ForeignKey("standard.LocationEconCode", blank=True, verbose_name=u"所在地区经济属性")
    location_folk = models.ForeignKey("standard.LocationFolkCode", blank=True, verbose_name=u"所在地区民族属性")
    postal_code = models.CharField(max_length=6, blank=True, verbose_name=u"邮政编码")
    duty_person = models.CharField(max_length=30, blank=True, verbose_name=u"联系人")
    telephone = models.CharField(max_length=30, blank=True, verbose_name=u"联系电话")
    fax = models.CharField(max_length=30, blank=True, verbose_name=u"传真电话")
    email = models.EmailField(max_length=30, blank=True, verbose_name=u"电子信箱")
    homepage = models.CharField(max_length=30, blank=True, verbose_name=u"主页地址")
    responsible_person_name = models.CharField(max_length=30, blank=True, verbose_name=u"局负责人")
    competent_name = models.CharField(max_length=30, blank=True, verbose_name=u"主管负责人")
    statistic_person_name = models.CharField(max_length=30, blank=True, verbose_name=u"统计负责人")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"主管单位"
        verbose_name_plural = u"主管单位"
