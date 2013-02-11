#coding: utf-8
from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import available_attrs
from config.models import SystemSetting

def system_required(key, errors=u"此功能暂不开放"):
    def decorator(func):
        def _wrapper(request, *args, **kwargs):
            try:
                cfg = SystemSetting.objects.get(key=key)
                if not cfg.value.lower() in ["yes", "1"]:
                    return HttpResponseForbidden(errors)
            except Exception,e:
                print e
            return func(request, *args, **kwargs)
        return wraps(func, assigned=available_attrs(func))(_wrapper)
    return decorator
