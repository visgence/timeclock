from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.template.context import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout

def view(request):

    error = ''

    if request.method == 'POST':
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/timeclock/')
            else:
                error = "Account disabled"
        else:
            error = "Invalid login";


    t = loader.get_template('login.html');
    c = RequestContext(request, {'user':request.user,'error':error})
    c.update(csrf(request));
    return HttpResponse(t.render(c))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/timeclock/login/")

