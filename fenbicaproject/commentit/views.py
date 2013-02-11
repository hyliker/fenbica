#coding: utf-8
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from commentit.models import Comment

def add_comment(request):
    content_type_id = request.POST.get("content_type_id", 0)
    content_type = ContentType.objects.get(pk=content_type_id)
    object_id = request.POST.get("object_id", "")
    content = request.POST.get("content", "")
    ip_address = request.META.get("REMOTE_ADDR", None)
    if request.user.is_authenticated():
        author = request.user
    else:
        author = None
    try:
        comment = Comment(
            author = author,
            content = content,
            ip_address = ip_address,
            content_type = content_type,
            object_id = object_id
        )
        comment.save()
    except Exception,e:
        return HttpResponse(e)
    else:
        referer = request.META.get("HTTP_REFERER", None)
        if referer:
            referer = "%s#submit-comment" % referer
        else:
            referer = "/"
        return HttpResponseRedirect(referer)
