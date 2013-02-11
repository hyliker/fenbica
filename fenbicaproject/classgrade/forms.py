#coding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from classgrade.models import * 

class ClassmateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClassmateForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        #if instance:
            #self.fields["uuid"].help_text = u"""这是你的所在班级内的学生编号"""
        #else:
            #self.fields["uuid"].help_text = u"班级内的学生编号"
            #self.fields["uuid"].label = u"班级内的学生编号"
    #def clean(self):
        #cleaned_data = self.cleaned_data
        #klass = cleaned_data.get("klass")
        #uuid = cleaned_data.get("uuid")
        #uuid_reg = r"^%s[0-9]{2}[1-9]$" % klass
        #if not re.match(uuid_reg, uuid):
            #raise forms.ValidationError(u"班学号格式不符号规定的格式")
        #return cleaned_data

    class Meta:
        model = Classmate

#class CourseInlineForm(forms.ModelForm):
    #class Meta:
        #model = Course
        #exclude = ("remark", )

class ClassmateInlineForm(forms.ModelForm):
    class Meta:
        model = Classmate
        exclude = ("remark", )
