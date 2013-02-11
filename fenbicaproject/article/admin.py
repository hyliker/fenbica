#coding: utf-8
from django.contrib import admin
from article.models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "public_category", "dtcreated", "dtpublished")
    list_filter = ("category",)
    search_fields = ("author__name", "title", "content")
    readonly_fields = ("read_count", "comment_count")
    raw_id_fields = ("category", )
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "article_count")
    readonly_fields = ("article_count",)

class ArticlePublicCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "article_count" )
    readonly_fields = ("article_count",)

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "file", "dtuploaded", )
    raw_id_fields = ("article",)
    search_fields = ("article__title", )

#以下动态增加绑定Admin
scope = locals()
for key in scope.keys():
    if key.endswith("Admin") and key is not "Admin":
        admin_model = scope[key]
        model = scope[key[:-5]]
        admin.site.register(model, admin_model)

