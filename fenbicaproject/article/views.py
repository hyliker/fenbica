#coding: utf-8
import json
import datetime
from collections import defaultdict
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.db.models import get_model
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from article.models import ArticlePublicCategory, Article, ArticleCategory, Attachment
from django.db import IntegrityError
from django.db.models import F, Count, Q
from person.models import Person
from django.views.decorators.cache import cache_page
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
import settings
from article.decorators import flash_login_required
from utils.django_snippets import render_to, HttpResponseRedirectView
from article.forms import ArticleForm
from django.contrib.auth.models import User

#@cache_page(60*15)
def index(request):
    """日志首页"""
    SHOW_LATEST_ARTITLES_NUMBER = 20
    SHOW_HOTTEST_ARTITLES_NUMBER = 20
    SHOW_HOTTEST_AUTHORS_NUMBER = 20

    latest_artitles = Article.objects.filter(status=Article.STATUS_PUBLISH).order_by("-dtcreated")[:SHOW_LATEST_ARTITLES_NUMBER]
    hottest_artitles = Article.objects.filter(status=Article.STATUS_PUBLISH).order_by("-read_count")[:SHOW_HOTTEST_ARTITLES_NUMBER]

    hottest_authors = Article.objects.values("author").annotate(article_count=Count("author"))
    hottest_persons = Person.objects.in_bulk(list(hottest_authors.values_list("author", flat=True)))
    hottest_authors = hottest_authors.order_by("-article_count")[:SHOW_HOTTEST_AUTHORS_NUMBER] # 注意， order_by 返回一个新的排序的結果，并不改变原結果
    print hottest_authors
    for a in hottest_authors:
        a["author"] = hottest_persons.get(a["author"])

    return render_to_response("article/index.xhtml", {
        "latest_artitles": latest_artitles,
        "hottest_artitles": hottest_artitles,
        "hottest_authors": hottest_authors,
    }, context_instance = RequestContext(request))

def my_article(request):
    """我的文章"""
    q = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    filter = Q(title__icontains=q)
    if q:
        articles = request.user.person.article_set.filter(filter).order_by("-dtcreated")
    else:
        articles = request.user.person.article_set.order_by("-dtcreated")

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(articles, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("article/my_article.xhtml", {
        "articles": pages.cur_page.object_list,
        "pages":  pages,
        "q": q,
    }, context_instance = RequestContext(request))

def view_article(request, article_pk):
    """查看某一篇文章"""
    article = get_object_or_404(Article, pk=article_pk)
    article.read_count = F("read_count") + 1
    article.save()
    article = get_object_or_404(Article, pk=article_pk)

    content_type = ContentType.objects.get_for_model(article)
    comments = article.comments.all()

    attachment_list = article.attachment_set.all()
    return render_to_response("article/view_article.xhtml", {
        "article": article,
        "content_type": content_type,
        "comments": comments,
        "attachment_list": attachment_list,
    }, context_instance = RequestContext(request))

def manage_article_category(request):
    """管理自己的日志分类"""
    categories = request.user.person.articlecategory_set.all()
    return render_to_response("article/manage_article_category.xhtml", {
        "categories": categories,
    }, context_instance = RequestContext(request))

@login_required
def add_category(request):
    """增加新的用户日志分类"""
    category_name = request.POST.get("category_name", "")
    try:
        new_category = ArticleCategory(
            author = request.user.person,
            name = category_name,
        )
        new_category.save()
        is_success = True
    except IntegrityError,e:
        print e
        is_success = False

    if request.is_ajax():
        if is_success:
            res = {"success": is_success, "data": {"id": new_category.pk, "category_name": new_category.name}}
        else:
            res = {"success": is_success}
        return HttpResponse(json.dumps(res))
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def delete_category(request, category_pk):
    """删除用户日志分类"""
    category = get_object_or_404(ArticleCategory, pk=category_pk)
    if category.author.pk != request.user.pk:
        return HttpResponseForbidden(u"无权限")
    category.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def view_category(request, category_pk=None, author_pk=None):
    """浏览用户某一日志分类文章"""
    page = request.GET.get("page", 1)
    if category_pk:
        category = get_object_or_404(ArticleCategory, pk=category_pk)
        author  = category.author
        articles = category.article_set.filter(category=category_pk).order_by("-dtcreated")
    elif author_pk:
        author = get_object_or_404(User, pk=author_pk)
        articles = Article.objects.filter(category__isnull=True, author=author).order_by("-dtcreated")

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for q in query_part:
        if not q.startswith("page="):
            new_query_parts.append(q)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(articles, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    if category_pk is not None:
        category_pk = int(category_pk)

    return render_to_response("article/view_article_category.xhtml", {
        "articles": pages.cur_page.object_list,
        "pages":  pages,
        "author": author,
        "category_pk": category_pk,
    }, context_instance = RequestContext(request))

@login_required
def rename_category(request, category_pk):
    """重命名用户日志分类"""
    try:
        category = ArticleCategory.objects.get(pk=category_pk)
        if category.author.pk != request.user.pk:
            return HttpResponseForbidden(u"无权限")

        category_name = request.POST.get("category_name", "")
        if not category_name:
            return HttpResponse(json.dumps({"success": False}))
        category.name = category_name
        category.save()
    except:
        return HttpResponse(json.dumps({"success": False}))
    return HttpResponse(json.dumps({"success": True}))

@login_required
@render_to("article/edit_article.html")
def edit_article(request, pk=None, template=None):
    """编辑日志"""
    if pk:
        article = get_object_or_404(Article, pk=pk)
        if article.author != request.user:
            return HttpResponseForbidden(u"你没有权限编辑别人的文章")
    else:
        article = Article(author=request.user)

    form = ArticleForm(request.user, request.POST or None, instance=article)
    if form.is_valid():
        new_article = form.save()

        attachment = request.POST.get("attachment", None)
        try:
            attachment_pk_list = attachment.split(",")
            attachment_list = Attachment.objects.filter(pk__in=attachment_pk_list)
            new_article.attachment_set.add(*attachment_list)
        except:
            pass

        redirect_url = reverse("view_article", args=[new_article.pk])
        return HttpResponseRedirect(redirect_url)
    return {"form": form}, template

@login_required
def draft(request):
    """列出草稿文章"""
    categories = request.user.person.articlecategory_set.all()
    articles = request.user.person.article_set.filter(status=Article.STATUS_DRAFT).order_by("-dtmodified")

    page = request.GET.get("page", 1)
    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for q in query_part:
        if not q.startswith("page="):
            new_query_parts.append(q)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(articles, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return render_to_response("article/drafts.xhtml", {
        "categories": categories,
        "articles": pages.cur_page.object_list,
        "pages":  pages,
    }, context_instance = RequestContext(request))

@login_required
def my_publish(request):
    """我发表的文章列表"""
    categories = ArticlePublicCategory.objects.all()
    query = Q(status = Article.STATUS_PUBLISH) & Q(public_category__isnull=False)
    articles = request.user.person.article_set.filter(query).order_by("-dtmodified")

    page = request.GET.get("page", 1)
    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for q in query_part:
        if not q.startswith("page="):
            new_query_parts.append(q)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(articles, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return render_to_response("article/my_publish_article.xhtml", {
        "categories": categories,
        "articles": pages.cur_page.object_list,
        "pages":  pages,
    }, context_instance = RequestContext(request))

@login_required
def delete_article(request, article_pk):
    """
    删除文章
    """
    article = get_object_or_404(Article, pk=article_pk)
    if article.author != request.user:
        return HttpResponseForbidden(u"你没有权限删除别人的文章")
    try:
        article.delete()
    except:
        res = {"success": False}
    else:
        res = {"success": True}
    return HttpResponse(json.dumps(res))

def search(request):
    """搜索页面"""
    context = request.GET.get("context")
    q = request.GET.get("q","")
    page = request.GET.get("page", 1)

    import time
    qstart = time.time()
    if context == "article":
        filter = Q(title__icontains=q)
        #filter = Q(title__icontains=q) | \
                 #Q(author__user__username__icontains=q) |\
                 #Q(author__name__icontains=q) |\
                 #Q(author__spell_name__icontains=q)
        articles = Article.objects.filter(filter)
        
    qend = time.time()
    qtime = qend - qstart
    
    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(articles, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("article/search.html", {
        "site": u"搜索",
        "articles": pages.cur_page.object_list,
        "q": q,
        "qtime": qtime,
        "pages":  pages,
        "context": context,
    }, context_instance=RequestContext(request))

#@login_required
@csrf_exempt
@flash_login_required
def upload_attachment(request):
    """上传文章附件"""
    if request.method == "POST" and "file" in request.FILES:
        try:
            file = request.FILES["file"]
            from article.forms import AttachmentForm
            form = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                _form = form.save(commit=False)
                _form.user = request.user
                _form.save()

                article_pk = request.POST.get("article_pk", None)
                try:
                    article = Article.objects.get(pk=article_pk)
                except Article.DoesNotExist,e:
                    article = None

                if article:
                    _form.article = article
                    _form.save()

                print _form.file.url
                res  = json.dumps({
                    "success": True,
                    "data": {
                        "uploaded_file_url": request.build_absolute_uri(_form.file.url),
                        "attachment_pk": _form.pk
                    }
                })
            else:
                res  = json.dumps({
                    "success": False,
                })
            return HttpResponse(res)
        except Exception,e:
            res  = json.dumps({
                "success": False,
            })
            return HttpResponse(res)

@csrf_exempt
def upload_image(request):
    """上传文章图片， 专门针对kindeditor 的图片上传"""
    if request.method == "POST" and "imgFile" in request.FILES:
        try:
            file = request.FILES["imgFile"]
            request.FILES["file"] = file
            from article.forms import AttachmentForm
            form = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                _form = form.save(commit=False)
                _form.user = request.user
                _form.save()

                article_pk = request.POST.get("article_pk", None)
                try:
                    article = Article.objects.get(pk=article_pk)
                except Article.DoesNotExist,e:
                    article = None

                if article:
                    _form.article = article
                    _form.save()

                print _form.file.url
                res  = json.dumps({
                    "error": 0,
                    "url": _form.file.url,
                })
            else:
                res  = json.dumps({
                    "error": 1,
                })
            print res
            return HttpResponse(res)
        except Exception,e:
            res  = json.dumps({ "error": 1 })
            return HttpResponse(res)


@login_required
def delete_attachment(request, attachment_pk):
    """删除文章附件"""
    attachment = get_object_or_404(Attachment, pk=attachment_pk)
    if attachment.user == request.user:
        try:
            attachment.delete()
        except:
            return HttpResponse(json.dumps({"success": False}))
        else:
            return HttpResponse(json.dumps({"success": True, "data": {"attachment_pk": attachment_pk }}))

    return HttpResponse(json.dumps({"success": False}))


@login_required
@render_to("article/my_attachment.html")
def my_attachment(request, template=None):
    """我的附件管理"""
    q = request.GET.get("q", "")
    page = request.GET.get("page", 1)

    filter = Q(user=request.user)
    if q:
        filter = Q(article__title__icontains=q) | Q(file__icontains=q) & filter
    attachment_list = Attachment.objects.filter(filter)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(attachment_list, 20)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return {
        "attachment_list": pages.cur_page.object_list,
        "pages": pages,
        "q": q,
    }, template


def latest_article(request):
    """最新的日志列表"""
    q = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    filter = Q(title__icontains=q)

    filter = Q(status=Article.STATUS_PUBLISH)
    if q:
        filter = filter & Q(title__icontains=q)

    articles = Article.objects.filter(filter).order_by("-dtcreated")

    #作者排行榜
    SHOW_HOTTEST_AUTHORS_NUMBER = 20
    hottest_authors = Article.objects.values("author").annotate(article_count=Count("author"))
    hottest_persons = Person.objects.in_bulk(list(hottest_authors.values_list("author", flat=True)))
    hottest_authors = hottest_authors.order_by("-article_count")[:SHOW_HOTTEST_AUTHORS_NUMBER] # 注意， order_by 返回一个新的排序的結果，并不改变原結果
    print hottest_authors
    for a in hottest_authors:
        a["author"] = hottest_persons.get(a["author"])

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(articles, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("article/latest_article.html", {
        "articles": pages.cur_page.object_list,
        "pages":  pages,
        "q": q,
        "hottest_authors": hottest_authors,
    }, context_instance = RequestContext(request))

def hottest_article(request):
    """最热门的日志列表"""
    q = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    filter = Q(title__icontains=q)

    filter = Q(status=Article.STATUS_PUBLISH)
    if q:
        filter = filter & Q(title__icontains=q)

    articles = Article.objects.filter(filter).order_by("-read_count")

    #作者排行榜
    SHOW_HOTTEST_AUTHORS_NUMBER = 20
    hottest_authors = Article.objects.values("author").annotate(article_count=Count("author"))
    hottest_persons = Person.objects.in_bulk(list(hottest_authors.values_list("author", flat=True)))
    hottest_authors = hottest_authors.order_by("-article_count")[:SHOW_HOTTEST_AUTHORS_NUMBER] # 注意， order_by 返回一个新的排序的結果，并不改变原結果
    print hottest_authors
    for a in hottest_authors:
        a["author"] = hottest_persons.get(a["author"])

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(articles, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("article/hottest_article.html", {
        "articles": pages.cur_page.object_list,
        "pages":  pages,
        "q": q,
        "hottest_authors": hottest_authors,
    }, context_instance = RequestContext(request))
