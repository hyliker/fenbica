#coding: utf-8
from django.db import models
from django import template
register = template.Library()
from django.db.models.fields.related import ForeignKey, OneToOneField

@register.inclusion_tag('base/generic_object_details.xhtml', takes_context=True)
def generic_object_details(context, obj):
    if isinstance(obj, models.Model):
        all_fields = obj._meta.fields
        try:
            exclude_fields = obj.Template.exclude
        except:
            exclude_fields = []
        render_fields = []
        for f in all_fields:
            if f.name not in exclude_fields:
                if not isinstance(f, OneToOneField):
                    if f.choices:
                        value = getattr(obj, 'get_%s_display' % f.name)()
                    else:
                        value = getattr(obj, f.name)
                    render_fields.append({"key": f.verbose_name, "value": value})
        return {"fields": render_fields}
