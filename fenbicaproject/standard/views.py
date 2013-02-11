#coding: utf-8
import json
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from standard.models import LocationCode
# Create your views here.

def get_location_children(request):
    """返回中国行政区划信息"""
    pk = request.REQUEST.get("pk", None)
    by = request.REQUEST.get("by", None)
    if by == "province":
        locations = LocationCode.objs.get_children(pk=pk, by=by)
    elif by == "city":
        locations = LocationCode.objs.get_children(pk=pk, by=by)
    res = {"success": True, "data": []}
    for c in locations:
        res["data"].append({"pk": c.code, "name": c.name, "code": c.code, "pinyin": c.pinyin })
    return HttpResponse(json.dumps(res))
