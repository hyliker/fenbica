#coding: utf-8
#http://djangosnippets.org/snippets/976/
from django.db import connection
from django.conf import settings
import os

#from django.conf import settings
from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    
    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        #if self.exists(name):
            #os.remove(os.path.join(settings.MEDIA_ROOT, name))
        #return name
        self.delete(name)
        return name

def terminal_width():
    """
    Function to compute the terminal width.
    WARNING: This is not my code, but I've been using it forever and
    I don't remember where it came from.
    """
    width = 0
    try:
        import struct, fcntl, termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]
    except:
        pass
    if width <= 0:
        try:
            width = int(os.environ['COLUMNS'])
        except:
            pass
    if width <= 0:
        width = 80
    return width

class SqlPrintingMiddleware(object):
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed.  This is only useful for debugging.
    """
    def process_response(self, request, response):
        indentation = 2
        if len(connection.queries) > 0 and settings.DEBUG:
            width = terminal_width()
            total_time = 0.0
            for query in connection.queries:
                nice_sql = query['sql'].replace('"', '').replace(',',', ')
                sql = "\033[1;31m[%s]\033[0m %s" % (query['time'], nice_sql)
                total_time = total_time + float(query['time'])
                while len(sql) > width-indentation:
                    print "%s%s" % (" "*indentation, sql[:width-indentation])
                    sql = sql[width-indentation:]
                print "%s%s\n" % (" "*indentation, sql)
            replace_tuple = (" "*indentation, str(total_time))
            print "%s\033[1;32m[TOTAL TIME: %s seconds]\033[0m" % replace_tuple
        return response


def render_to(template):
    """
    http://djangosnippets.org/snippets/821/
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from functools import wraps
    def renderer(func):
        @wraps(func)
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                if not output[1] and template:
                    return render_to_response(template, output[0], RequestContext(request))
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer


from django.core.serializers import json, serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import simplejson

class JsonResponse(HttpResponse):
    """
    http://djangosnippets.org/snippets/154/
    A subclass of HttpResponse useful as a shortcut in views; 
    it chooses the correct JSON serializer based on whether or not it is passed a QuerySet.
    """
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = simplejson.dumps(
                object, indent=2, cls=json.DjangoJSONEncoder,
                ensure_ascii=False)
        super(JsonResponse, self).__init__(
            content, content_type='application/json')



from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class HttpResponseRedirectView(HttpResponseRedirect):
    """
        This response directs to a view by reversing the url
    
        e.g. return HttpResponseRedirectView('org.myself.views.myview') 
        or use the view object e.g.
             from org.myself.views import myview
             return HttpResponseRedirectView(myview)
        
        You can also pass the url arguments to the constructor e.g.
        return HttpResponseRedirectView('org.myself.views.myview', year=2008, colour='orange')
    """
    def __init__(self, view, *args, **kwargs):
        viewurl = reverse(view, args=args, kwargs=kwargs)
        HttpResponseRedirect.__init__(self, viewurl)


def flash_login_required(function):
    """
    Decorator to recognize a user  by its session.
    Used for Flash-Uploading.
    """

    def decorator(request, *args, **kwargs):
        try:
            engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        except:
            import django.contrib.sessions.backends.db
            engine = django.contrib.sessions.backends.db
        print request.POST
        session_data = engine.SessionStore(request.POST.get('session_key'))
        user_id = session_data['_auth_user_id']
        # will return 404 if the session ID does not resolve to a valid user
        request.user = get_object_or_404(User, pk=user_id)
        return function(request, *args, **kwargs)
    return decorator
