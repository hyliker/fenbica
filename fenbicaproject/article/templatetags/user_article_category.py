#coding: utf-8
from django.db import models
from django import template
from article.models import Article, ArticleCategory
register = template.Library()

@register.inclusion_tag('article/templatetags/user_article_category.html', takes_context=True)
def user_article_category(context, user, active_category):
    category_list = user.articlecategory_set.all()
    default_category_count = Article.objects.filter(author=user, category__isnull=True).count()

    if isinstance(active_category, ArticleCategory):
        active_category = active_category.pk

    return {
        "category_list": category_list, 
        "default_category_count": default_category_count, 
        "user": user,
        "active_category": active_category,
    }
