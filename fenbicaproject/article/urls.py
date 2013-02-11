# coding: utf-8
from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('article.views',
    url(r'^index/$', 'index', name="article_index"),
    #url(r'^add/$', 'add_article', name="add_article"),
    url(r'^add/$', 'edit_article', name="add_article"),
    url(r'^category/add/$', 'add_category', name="add_article_category"),
    url(r'^category/(?P<category_pk>\d+)/delete$', 'delete_category', name="delete_article_category"),
    url(r'^my/$', 'my_article', name="my_article"),
    url(r'^latest/$', 'latest_article', name="article_latest_article"),
    url(r'^hottest/$', 'hottest_article', name="article_hottest_article"),
    url(r'^attachment/my/$', 'my_attachment', name="article_my_attachment"),
    url(r'^(?P<article_pk>\d+)/$', 'view_article', name="view_article"),
    url(r'^(?P<pk>\d+)/edit/$', 'edit_article', name="edit_article"),
    url(r'^(?P<article_pk>\d+)/delete/$', 'delete_article', name="delete_article"),
    url(r'^attachment/(?P<attachment_pk>\d+)/delete/$', 'delete_attachment', name="article_delete_attachment"),
    url(r'^category/(?P<category_pk>\d+)/$', 'view_category', name="view_article_category"),
    url(r'^category/default/(?P<author_pk>\d+)$', 'view_category', {"category_pk": None },  name="view_article_category_default"),
    url(r'^category/(?P<category_pk>\d+)/rename$', 'rename_category', name="rename_article_category"),
    url(r'^category/manage$', 'manage_article_category', name="manage_article_category"),
    url(r'^drafts/$', 'draft', name="article_draft_index"),
    url(r'^publish/my/$', 'my_publish', name="my_publish_article"),
    url(r'^attachment/upload/$', 'upload_attachment', name="article_upload_attachment"),
    url(r'^image/upload/$', 'upload_image', name="article_upload_image"),
)
