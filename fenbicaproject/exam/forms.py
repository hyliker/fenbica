#coding: utf-8
from django import forms
from django.contrib.auth.models import User
from exam.models import *

class ExamForm(forms.ModelForm):
    """学校举行的考试信息"""
    class Meta:
        model = Exam
        exclude = ["school"]

class AddExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = ["school"]

class EditExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = ["school"]

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)

    def clean_score(self):
        cleaned_data = self.cleaned_data
        score = cleaned_data["score"]
        subject = cleaned_data["subject"]
        if score < 0 or score > subject.full_score:
            raise forms.ValidationError(u"你输入的分数不在允许的 [0, %d] 范围之内" % subject.full_score)
        return score

class SubjectForm(forms.ModelForm):
    def __init__(self, school, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['exam'].queryset = Exam.objects.filter(school=school)
    class Meta:
        model = Subject

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ["exam"]

class EditSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ["exam"]
