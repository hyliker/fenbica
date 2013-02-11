from django.conf.urls.defaults import *
from settings import PROJECT_DIR, PROJECT_NAME, MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
admin.site.login_template = "registration/login_admin.html"

urlpatterns = patterns('',
    # Example:
    # (r'^mschool/', include('mschool.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', "index.views.index"),
    (r'^my/$', "index.views.my"),
    (r'^desktop/$', "index.views.desktop"),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    (r'^logout/$', "index.views.logout"),
    (r'^admin/', include(admin.site.urls)),
    (r'^person/', include("person.urls")),
    (r'^settings/', "person.views.settings"),
    (r'^staff/', include("staff.urls")),
    (r'^student/', include("student.urls")),
    (r'^page/', include("page.urls")),
    (r'^exam/', include("exam.urls")),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, "show_indexes": True}, ),
    (r'standard/', include("standard.urls")),
    (r'school/', include("school.urls")),
    (r'article/', include("article.urls")),
    (r'course/', include("course.urls")),
    (r'classgrade/', include("classgrade.urls")),
    (r'dorm/', include("dorm.urls")),
    (r'commentit/', include("commentit.urls")),
    (r'config/', include("config.urls")),
    url(r'^search$', 'index.views.search', name="search"),
    url(r'^manage$', 'index.views.manage', name="manage"),
)
