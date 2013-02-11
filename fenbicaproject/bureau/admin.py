#coding: utf-8
from django.contrib import admin
from bureau.models import *

class BureauAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "location_type", "duty_person", "telephone", "responsible_person_name", "competent_name", "statistic_person_name" )


#admin.site.register(Bureau, BureauAdmin)
#admin.site.register(StudentExperience, StudentExperienceAdmin)

#以下动态增加绑定Admin
scope = locals()
for key in scope.keys():
    if key.endswith("Admin") and key is not "Admin":
        admin_model = scope[key]
        model = scope[key[:-5]]
        admin.site.register(model, admin_model)
