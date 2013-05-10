from django.http import HttpResponseRedirect
from settings import SESSION_TIMEOUT

def check_access(request):
    request.session.set_expiry(SESSION_TIMEOUT)
        
    if request.user.is_authenticated():
        if request.user.is_active:
            return request.user
        else:
            return HttpResponseRedirect('/timeclock/login/')
    else:
        return HttpResponseRedirect('/timeclock/login/')

