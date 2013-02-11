#coding: utf-8
from django.contrib import admin
from commentit.models import *
from django.contrib.contenttypes.models import ContentType


class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "dtcommented"
    list_display = ("author", "content", "dtcommented", "ip_address", "content_type", "object_id", "object_link")
    list_filter = ("dtcommented",)
    search_fields = ("author__name", "content", )

    def object_link(self, obj):
        model = obj.content_type.model_class()
        object = model.objects.get(pk=obj.object_id)
        try:
            return u'<a href="%s">被评论内容</a>' % object.get_absolute_url()
        except:
            return ""
    object_link.short_description = u"对象详情"
    object_link.allow_tags = True

admin.site.register(Comment, CommentAdmin)
