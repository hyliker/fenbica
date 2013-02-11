#coding: utf-8
from django.db import models

# Create your models here.

class Gallery(models.Model):
    """照片库"""
    title = models.CharField(u"标题", max_length=120)
    description = models.TextField(u"描述", blank=True)
    photos = models.ManyToManyField('Photo', verbose_name=u"照片", related_name='galleries')
    dtcreated = models.DateTimeField(u"创建日期", auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name=u"是否发布")

class Photo(models.Model):
    """照片"""
    image = StdImageField(upload_to="page_scenery", size=(800,600), thumbnail_size=(200,130), verbose_name=u"照片")
    title = models.CharField(max_length=75, verbose_name=u"标题")
    description = models.TextField(blank=True, verbose_name=u"描述")
    dtcreated = models.DateTimeField(auto_now_add=True, verbose_name=u"日期")
    display_order = models.IntegerField(default=0, verbose_name=u"显示顺序")
    is_published = models.BooleanField(default=True, verbose_name=u"是否发布")

class Category(models.Model):
    """分类"""
    pass
