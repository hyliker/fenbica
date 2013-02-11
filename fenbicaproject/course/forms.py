#coding: utf-8
from django import forms
from django.contrib.auth.models import User
from course.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course

class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ("teacher", )
