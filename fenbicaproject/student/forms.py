#coding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from student.models import * 
from standard.widgets import LocationMultiLevelSelect

class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields["uuid"].help_text = u"""<span class="warning">提醒：录入格式如: S20100001, 从左到右排序，第1位为大写字母S, 第2－5位为注册年份, 第6-9位 为注册序号。如果不指定，则由系统自动产生</span>"""
        self.fields["uuid"].validators.append(validators.RegexValidator(regex=r'^S[1-9][0-9]{7}'))
        self.fields["uuid"].label = u"编号(学号)"
        instance = kwargs.get("instance", None)
        if instance:
            self.fields["password"].help_text = u"""注意：要修改密码，请不要在此直接修改，请使用<a href="/admin/auth/user/%d/password/">修改密码表单</a>""" % instance.pk
        else:
            self.fields["password"].help_text = u"输入初始化帐号密码"
            self.fields["password"].label = u"初始化密码"
    
    def clean_uuid(self):
        uuid = self.cleaned_data["uuid"]
        if not uuid:
            return None
        return uuid
    class Meta:
        model = Student
        exclude = ("log", )

class MyStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ("user","identity", "identity_group", "school", "is_valid", "log", "uuid")

class EditStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ("user","identity", "identity_group", "school", "is_valid", "log")

class AddStudentForm(forms.ModelForm):
    password = forms.CharField(label=u"密码", help_text=u"初始化帐号密码")
    class Meta:
        model = Student
        exclude = ("user","identity", "identity_group", "school", "is_valid", "log")

class EditSelfStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditSelfStudentForm, self).__init__(*args, **kwargs)
        self.fields["born_place"].widget = LocationMultiLevelSelect()
        self.fields["native_place"].widget = LocationMultiLevelSelect()

    class Meta:
        model = Student
        fields = (
            'first_name', 'last_name', 'email', 'name', 'spell_name', 'abbr_name', 'used_name', 
            'id_no', 'gender', 'marriage', 'blood_type', 'birthday', 'diploma', 'born_place', 
            'native_place', 'folk', 'religion', 'emigrant', 'health', 'politics', 'residence_address',
            'domicle_location', 'domicle_type', 'is_floating', 'is_singleton', 'nationality',
            'telephone', 'postal_address', 'postal_code', 'homepage', 'photo', 'fortes', 'interest',
        )

class EditExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ("student", )

class EditKeeperForm(forms.ModelForm):
    class Meta:
        model = Keeper
        exclude = ("student", )

class EditFamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        exclude = ("student", )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

class CommentByMasterForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("learning_stage", "learning_year", "semester", "comment")
