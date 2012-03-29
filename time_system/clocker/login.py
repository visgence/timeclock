from models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.template import Context, loader
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
import urlparse

def view(request):

    error = ''

    #Read next url to be redirected to
    try:
        redirect_to = request.REQUEST["next"]
    except KeyError:
        redirect_to = "../"

    if request.method == 'POST':
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
                error = "Account disabled"
        else:
            error = "Invalid login";


    t = loader.get_template('login.html');
    c = Context({'user':request.user,'error':error,"redirect_to":redirect_to})
    c.update(csrf(request));
    return HttpResponse(t.render(c))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("login/")

