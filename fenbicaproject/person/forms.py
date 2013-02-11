#coding: utf-8
from django import forms
from django.contrib.auth.models import User
from student.models import Student, Person
from standard.models import LocationCode
from standard.widgets import LocationMultiLevelSelect

#def StudentUserChoice():
    #students = User.objects.filter(groups__name=u"学生")
    #choices = [(s.pk, s.username) for s in students]
    #return choices

#class StudentProfileAdminForm(forms.ModelForm):
    #user = forms.ChoiceField(choices = StudentUserChoice())
    #user = forms.ChoiceField()

    #def __init__(self, *args, **kwargs):
        #super(StudentProfileAdminForm, self).__init__(*args, **kwargs)
        #self.fields["user"].choices = StudentUserChoice()

    #def clean_user(self):
        #try:
            #user = User.objects.get(pk=self.cleaned_data["user"])
        #except User.DoesNotExsit:
            #raise forms.ValidationError("This user is not exsit. Please Choose another one.")
        #else:
            #return user

    #class Meta:
        #model = StudentProfile

class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        if instance:
            self.fields["password"].help_text = u"""注意：要修改密码，请不要在此直接修改，请使用<a href="/admin/auth/user/%d/password/">修改密码表单</a>""" % instance.pk
        else:
            self.fields["password"].help_text = u"输入初始化帐号密码"
            self.fields["password"].label = u"初始化密码"

    class Meta:
        model = Person 
        exclude = ("user","identity", "identity_group", "school", "is_valid", "log")

class EditSelfPersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditSelfPersonForm, self).__init__(*args, **kwargs)
        self.fields["born_place"].widget = LocationMultiLevelSelect()
        self.fields["native_place"].widget = LocationMultiLevelSelect()

    class Meta:
        model = Person
        fields = (
            'first_name', 'last_name', 'email', 'name', 'spell_name', 'abbr_name', 'used_name', 
            'id_no', 'gender', 'marriage', 'blood_type', 'birthday', 'diploma', 'born_place', 
            'native_place', 'folk', 'religion', 'emigrant', 'health', 'politics', 'residence_address',
            'domicle_location', 'domicle_type', 'is_floating', 'is_singleton', 'nationality',
            'telephone', 'postal_address', 'postal_code', 'homepage', 'photo', 'fortes', 'interest',
        )
        raw_id_fields = ("residence_address", "folk", "born_place")
