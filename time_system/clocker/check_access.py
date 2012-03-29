# Create your views here.
from models import *
from django.http import HttpResponse
from django.core import serializers
from django.template import Context, loader
from django.http import HttpResponseRedirect

def check_access(request):

    if(request.user.username == ''):
        return HttpResponseRedirect("/login/?next=%s" % (request.path))

    t = loader.get_template('login.html');


    if(not request.user.is_active):
        c = Context({'user':request.user,'access_error':'User is not active'});
        return HttpResponse(t.render(c))

    return 0;
