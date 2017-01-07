from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from clocker.decorators import login_exempt


@login_exempt
def renderLogin(request, context={}):
    '''
    ' Renders the login page of the app
    '''

    assert isinstance(context, dict)

    user = request.user
    if user.is_authenticated() and user.is_active:
        return HttpResponseRedirect('/timeclock/')

    return render(request, 'login.html', context)


@login_exempt
def loginUser(request):
    '''
    ' Logs a user into the app if they provide the proper username and password
    '''

    #TODO: proper 404 handling
    if request.method != 'POST':
        return HttpResponse('404');

    username = request.POST.get("username", '')
    password = request.POST.get("password", '')
    user = authenticate(username=username, password=password)
    if user is None:
        return renderLogin(request, {'error': "Incorrect username or password"})

    if not user.is_active:
        return renderLogin(request, {'error': "User is deactivated"})

    login(request, user)
    return HttpResponseRedirect('/timeclock/')


@login_exempt
def logoutUser(request):
    '''
    ' Logs a user out of the system and sends them back to the login page
    '''

    logout(request)
    return HttpResponseRedirect("/timeclock/login/")


def isLoggedIn(request):
    '''
    ' Simply returns the text 'yes' if the user is still logged in.  Checkaccess will catch the request before this
    ' they are not.
    '''

    return HttpResponse("yes", content_type="text/html")
