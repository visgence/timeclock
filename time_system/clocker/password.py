from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
try:
    import simplejson as json
except ImportError:
    import json

from check_access import check_access
from clocker.models import Employee



def renderForm(request):

    response = check_access(request)
    if(not isinstance(response, Employee)):
        error = "Sorry but you do not have permission to access this part of the site"
        return HttpResponse(json.dumps({'accessError': error}), mimetype="application/json")

    t = loader.get_template('passwordForm.html')
    c = RequestContext(request, {})
    return HttpResponse(json.dumps({'html': t.render(c)}), mimetype="application/json")


@require_POST
def changePassword(request):
    '''
    ' This view will allow a user to change their password.
    '
    ' POST arguments:
    '   jsonData - JSON data containing:
    '              oldPassword - string containing user's current password.
    '              newPassword - string containing password to change to.
    '''

    employee = check_access(request)
    if(not isinstance(employee, Employee)):
        error = "Sorry but you do not have permission to access this part of the site"
        return HttpResponse(json.dumps({'accessError': error}), mimetype="application/json")

    jsonData = request.REQUEST.get('jsonData', None)

    try:
        jsonData = json.loads(jsonData)
    except Exception as e:
        return HttpResponse(json.dumps({'errors': 'JSON Exception: %s: %s' % (type(e), e.message)}), mimetype="application/json")

    try:
        oldPassword = jsonData['oldPassword']
        newPassword = jsonData['newPassword']
    except KeyError as e:
        return HttpResponse(json.dumps({'errors': 'KeyError: %s' % e.message}), mimetype="application/json")

    # Make sure old password is valid
    user = authenticate(username=employee.get_username(), password=oldPassword)
    if user is None or user != employee:
        return HttpResponse(json.dumps({'errors': 'Authentication Error: Username and password are not correct'}), mimetype="application/json")
    elif not user.is_active:
        error = 'Authentication Error: User is not active.  You must be active to change password.'
        return HttpResponse(json.dumps({'errors': error}), mimetype="application/json")

    # Change the password
    employee.set_password(newPassword)
    employee.save()
    return HttpResponse(json.dumps({'success': 'Password successfully changed!'}), mimetype="application/json")



