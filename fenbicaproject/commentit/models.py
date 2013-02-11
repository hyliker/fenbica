#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.

class Comment(models.Model):
    """简单通用的评论"""
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, null=True, blank=True, verbose_name=u"评论者") #允许匿名评论
    content = models.TextField(max_length=256, verbose_name=u"评论内容")
    dtcommented = models.DateTimeField(auto_now_add=True, verbose_name=u"评论时间")
    ip_address = models.IPAddressField(blank=True, null=True, verbose_name=u"IP地址")

    content_type = models.ForeignKey(ContentType, verbose_name=u"被评论内容类型")
    object_id = models.PositiveIntegerField(verbose_name=u"被评论内容对象编号")

    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return u"%s" % (self.author.username)

    class Meta:
        ordering = ["dtcommented"]
        verbose_name = u"评论"
        verbose_name_plural = u"评论"
