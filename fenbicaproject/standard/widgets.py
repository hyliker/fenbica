#coding: utf-8
from django import forms
from standard.models import LocationCode
from django.template.loader import render_to_string

class LocationMultiLevelSelect(forms.Widget):
    def render(self, name, value, attrs):
        provinces = LocationCode.objs.provinces
        try:
            value_obj = LocationCode.objects.get(code=value)
        except:
            value_obj = None
        return render_to_string("standard/widgets/LocationMultiLevelSelect.html", {
            "provinces": provinces, "field": name, "value": value, "value_obj": value_obj,
        })
