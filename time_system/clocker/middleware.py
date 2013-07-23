from django.http import HttpResponseRedirect, HttpResponse
from settings import SESSION_TIMEOUT

try:
    import simplejson as json
except ImportError:
    import json

class CheckAccess():
    '''
    ' Middleware that validates that a user is logged into the app and is active.
    '''

    def process_view(self, request, view_func, args, kwargs):
      
        #If there are decorators then make sure none of them are
        #'login_exempt' before continueing
        if hasattr(view_func, '_decorators'):
            for dec in view_func._decorators:
                if dec.__name__ == "login_exempt":
                    return None
        
        #Boot back to login page
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/timeclock/login/')

        #Give custom page telling them they are no longer active
        if not request.user.is_active:
            return HttpResponse("user no longer active!")
        
        request.session.set_expiry(SESSION_TIMEOUT)
        return None


    def process_response(self, request, response):
        
        if request.is_ajax():
            
            if response.status_code == 302:
                dump = {'status': 302, 'location': response['location']}
                resp = HttpResponse(json.dumps(dump), content_type="application/json")
                response = resp 

        return response
