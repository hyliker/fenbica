# coding:utf-8
import tagging
from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from commentit.models import Comment
import datetime

# Create your models here.

class Article(models.Model):
    """
    文章日志
    """
    STATUS_PUBLISH = 0
    STATUS_DRAFT = 1

    STATUS_CHOICES = (
        (STATUS_PUBLISH, u"发布"),
        (STATUS_DRAFT, u"草稿"),
    )

    author = models.ForeignKey(User, verbose_name=u"作者")
    title = models.CharField(u"标题", max_length=128)
    content = models.TextField(u"内容", blank=True)
    dtcreated = models.DateTimeField(u"创作日期", auto_now_add=True)
    dtmodified = models.DateTimeField(u"最后修改日期", auto_now=True)
    category = models.ForeignKey("ArticleCategory", verbose_name=u"用户文章分类", null=True, blank=True)
    public_category = models.ForeignKey("ArticlePublicCategory", verbose_name=u"公共文章分类", null=True, blank=True, help_text=u"投稿到哪个栏目") 
    dtpublished = models.DateTimeField(u"投稿发布日期", auto_now=True, null=True, blank=True)
    quote = models.CharField(u"文章来源", max_length=256, blank=True)
    status = models.SmallIntegerField(u"保存状态", max_length=16, choices=STATUS_CHOICES, default=STATUS_PUBLISH)
    commented = models.BooleanField(u"是否允许评论", blank=True) 
    comment_count = models.IntegerField(u"评论数", default=0, editable=False)
    read_count =  models.IntegerField(u"浏览数", default=0, editable=False)
    comments = generic.GenericRelation(Comment)

    def summary(self):
        return u"%s ..." % self.content[:200]

    @models.permalink
    def get_absolute_url(self):
        return ("view_article", [str(self.pk)])

    def save(self, *args, **kwargs):
        if not self.pk and self.category:
            self.category.article_count = F("article_count") + 1
            self.category.save()
        if self.public_category:
            self.public_category.article_count = F("article_count") + 1
            self.public_category.save()
            #self.category.article_count += 1
            #self.category.save()
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"文章"
        verbose_name_plural = u"文章"

tagging.register(Article)

class Attachment(models.Model):
    """文章附件"""
    article = models.ForeignKey("Article", verbose_name=u"文章", null=True, blank=True)
    user = models.ForeignKey(User, verbose_name=u"帐号")
    file = models.FileField(upload_to="uploads/article/attachment/%Y/%m/%d", verbose_name=u"附件")
    dtuploaded = models.DateTimeField(auto_now_add=True, verbose_name=u"上传日期")

    def file_basename(self):
        from os.path import basename
        return basename(self.file.name)

    def __unicode__(self):
        print dir(self.file)
        return self.file.name

    class Meta:
        verbose_name = u"文章附件"
        verbose_name_plural = u"文章附件"
        ordering = ["dtuploaded"]

class ArticleCategory(models.Model):
    """用户文章分类"""
    name = models.CharField(u"分类名称", max_length=32)
    author = models.ForeignKey(User, verbose_name=u"作者")
    article_count = models.IntegerField(u"文章数", default=0, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/article/category/%i" % self.id

    class Meta:
        unique_together = ("name", "author")
        verbose_name = u"用户文章分类"
        verbose_name_plural = u"用户文章分类"

class ArticlePublicCategory(models.Model):
    """文章投稿到的公共分类分类"""
    name = models.CharField(u"分类名称", unique=True, max_length=32)
    description = models.TextField(u"分类描述", blank=True)
    article_count = models.IntegerField(u"文章数", default=0, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"公共文章分类"
        verbose_name_plural = u"公共文章分类"
