#coding: utf-8
from django.contrib import admin
from config.models import *

class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "remark")

admin.site.register(SystemSetting, SystemSettingAdmin)

class UserSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "remark")

admin.site.register(UserSetting, UserSettingAdmin)
