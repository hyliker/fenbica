#coding: utf-8
from django.contrib import admin
from person.models import *
from person.forms import *

class PersonAdmin(admin.ModelAdmin):
    date_hierarchy = "date_joined"
    list_display = ( 'username', 'name', 'identity',"uuid", 'gender', "folk", "birthday", "id_no") 
    search_fields = ("username", "name", "spell_name")
    list_filter = ("gender", "identity", "diploma", )
    list_per_page = 25
    search_fields = ("name", "spell_name", "username", "uuid", "id_no")
    form = PersonForm

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get("password", None)
        if not change:
            if password is None:
                obj.set_unusable_password()
            else:
                obj.set_password(password)
        obj.save()

admin.site.register(Person, PersonAdmin)
