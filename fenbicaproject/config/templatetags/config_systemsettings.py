#coding: utf-8
import re
from django import template
from config.models import SystemSetting
register = template.Library()

class SystemSettingNode(template.Node):
    def __init__(self, key_name, var_name):
        self._key_name = key_name
        self._var_name = var_name
    def render(self, context):
        try:
            ss = SystemSetting.objects.get(key=self._key_name)
            if ss.value.lower() in ["yes", "true", "1"]:
                ss = True
            else:
                ss = False
        except:
            ss = False
        print ss
        context[self._var_name] = ss
        return ''


@register.tag
def get_system_setting(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    key_str, var_name = m.groups()
    if not (key_str[0] == key_str[-1] and key_str[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return SystemSettingNode(key_str[1:-1], var_name)
