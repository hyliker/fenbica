#coding: utf-8
from django.db import models

# Create your models here.

class Article(models.Model):
    "文章"
    author = models.ForeignKey(User, verbose_name=u"作者")
    title = models.CharField(u"标题", max_length=128)
    content = models.TextField(u"内容")
    dtcreated = models.DateTimeField(u"创建日期", auto_now_add=True)
    dtmodified = models.DateTimeField(u"最后修改日期", auto_now=True)
    category = models.ForeignKey("ArticleCategory", verbose_name=u"用户文章分类", default=0)
    dtpublished = models.DateTimeField(u"投稿发布日期", auto_now=True, null=True, blank=True)
    quote = models.CharField(u"来源", max_length=256, blank=True)
    status = models.CharField(u"状态", max_length=16, choices=ARTICLE_STATUS)
    commented = models.BooleanField(u"是否允许评论", blank=True) 
    published = models.BooleanField(u"是否投稿", blank=True) 
    comment_count = models.IntegerField(u"评论数", default=0)
    read_count =  models.IntegerField(u"浏览数", default=0)

    def summary(self):
        if len(self.content) > 100:
            return u"%s ..." % self.content[:100]

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"文章"
        verbose_name_plural = u"文章"

tagging.register(Article)

class ArticleCategory(models.Model):
    """期刊分类"""
    name = models.CharField(u"分类名称", max_length=32)
    description = models.TextField(u"分类描述", blank=True)
    author = models.ForeignKey(User, verbose_name=u"作者")
    article_count = models.IntegerField(u"文章数", null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"用户文章分类"
        verbose_name_plural = u"用户文章分类"

class Periodical(models.Model):
    """期刊"""
    period = models.CharField(u"哪一期")
    dtpublished = models.DateTimeField(u"出版日期", auto_now=True, null=True, blank=True)
