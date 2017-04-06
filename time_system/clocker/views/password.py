from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
try:
    import simplejson as json
except ImportError:
    import json



def renderForm(request):

    t = loader.get_template('passwordForm.html')
    c = RequestContext(request, {})
    return HttpResponse(json.dumps({'html': t.render(c)}), content_type="application/json")


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

    employee = request.user

    try:
        jsonData = json.loads(request.POST['jsonData'])
    except Exception as e:
        return HttpResponse(json.dumps({'errors': 'JSON Exception: %s: %s' % (type(e), e.message)}), content_type="application/json")

    try:
        oldPassword = jsonData['oldPassword']
        newPassword = jsonData['newPassword']
    except KeyError as e:
        return HttpResponse(json.dumps({'errors': 'KeyError: %s' % e.message}), content_type="application/json")

    # Make sure old password is valid
    user = authenticate(username=employee.get_username(), password=oldPassword)
    if user is None or user != employee:
        return HttpResponse(json.dumps({'errors': 'Authentication Error: Username and password are not correct'}), content_type="application/json")
    elif not user.is_active:
        error = 'Authentication Error: User is not active.  You must be active to change password.'
        return HttpResponse(json.dumps({'errors': error}), content_type="application/json")

    # Change the password
    employee.set_password(newPassword)
    employee.save()
    return HttpResponse(json.dumps({'success': 'Password successfully changed!'}), content_type="application/json")



