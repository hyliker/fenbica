#coding: utf-8
import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import never_cache
from utils.django_snippets import render_to, HttpResponseRedirectView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from config.models import SystemSetting

REDIRECT_FIELD_NAME = 'next'
# Create your views here.

@login_required
def edit_systemsetting(request):
    key = request.REQUEST.get("key", "")
    value = request.REQUEST.get("value", "")
    try:
        ss = SystemSetting.objects.get(key=key)
        ss.value = value
        ss.save()
    except Exception, e:
        res = json.dumps({"success": False})
    else:
        res = json.dumps({"success": True})
    return HttpResponse(res)
