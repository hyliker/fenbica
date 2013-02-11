#coding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from staff.models import *
from standard.widgets import LocationMultiLevelSelect

class StaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        self.fields["uuid"].label = u"编号(工号)"
        self.fields["uuid"].help_text = u"""<span class="warning">提醒：录入格式如: T20100001, 从左到右排序，第1位为大写字母S, 第2－5位为注册年份, 第6-9位 为注册序号。如果不指定，则由系统自动产生</span>"""
        self.fields["uuid"].validators.append(validators.RegexValidator(regex=r'^T[1-9][0-9]{7}', message=u"请注册编号的格式", code="invalid"))
        if instance:
            self.fields["password"].help_text = u"""注意：要修改密码，请不要在此直接修改，请使用<a href="/admin/auth/user/%d/password/">修改密码表单</a>""" % instance.pk
        else:
            self.fields["password"].help_text = u"输入初始化帐号密码"
            self.fields["password"].label = u"初始化密码"
    class Meta:
        model = Staff 
        exclude = ("user","identity", "identity_group", "school", "log")

class MyStaffForm(forms.ModelForm):
    '''编辑教职工的基本信息表单'''
    #user = forms.ModelChoiceField(label='', queryset=Staff.objects.all(),widget=forms.HiddenInput())
    #identity = forms.ModelChoiceField(label='', queryset=[],widget=forms.HiddenInput())
    #identity_group = forms.ModelChoiceField(label='', queryset=[],widget=forms.HiddenInput())
    #school = forms.ModelChoiceField(label='', queryset=[],widget=forms.HiddenInput())
    #is_valid = forms.BooleanField(label='', widget=forms.HiddenInput())

    class Meta:
        model = Staff
        exclude = ('user','identity', 'identity_group', 'school', 'is_valid', 'log', 'uuid')

class AddStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['user', 'identity', 'identity_group']

class EditStaffForm(forms.ModelForm):
    '''编辑教职工的基本信息表单'''

    class Meta:
        model = Staff
        exclude = ('user','identity', 'identity_group', 'school', 'is_valid', 'log', 'uuid')

class EditExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ("staff", )

class EditDiplomaForm(forms.ModelForm):
    class Meta:
        model = Diploma
        exclude = ("staff", )

class EditSpouseForm(forms.ModelForm):
    class Meta:
        model = Spouse 
        exclude = ("staff", )

class EditFamilyForm(forms.ModelForm):
    class Meta:
        model = Family 
        exclude = ("staff", )

class EditWorkloadForm(forms.ModelForm):
    class Meta:
        model = Workload 
        exclude = ("staff", )

class EditTeachingForm(forms.ModelForm):
    class Meta:
        model = Teaching 
        exclude = ("staff", )

class EditSelfStaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditSelfStaffForm, self).__init__(*args, **kwargs)
        self.fields["born_place"].widget = LocationMultiLevelSelect()
        self.fields["native_place"].widget = LocationMultiLevelSelect()
    class Meta:
        model = Staff
        fields = (
            'first_name', 'last_name', 'email', 'name', 'spell_name', 'abbr_name', 'used_name', 
            'id_no', 'gender', 'marriage', 'blood_type', 'birthday', 'diploma', 'born_place', 
            'native_place', 'folk', 'religion', 'emigrant', 'health', 'politics', 'residence_address',
            'domicle_location', 'domicle_type', 'is_floating', 'is_singleton', 'nationality',
            'telephone', 'postal_address', 'postal_code', 'homepage', 'photo', 'fortes', 'interest',
        )
