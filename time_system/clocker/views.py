from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from models import Employee
import check_access


def main_page(request):
    """
    The clock in page.  Grabs user input data to determine if the user can clock in/out.  Returns back a dictionary
    with information about the success or failure of clocking the employee in/out.
    """

    #response = check_access(request)
    #if(response):
    #    return response

    if (request.method == 'POST'):
        user_name = request.POST.get('user_name')
        status = request.POST.get('status')

        #base cases for when the use simply hits submit with no user name
        if(user_name == ''):
            return render_to_response('main_page.html', {'error':"empty"}, context_instance=RequestContext(request))

        try:

            employee = Employee.objects.get(user__username=user_name)
            if(status == "Out" or status == "out"):
                return render_to_response('main_page.html', {'error':employee.clock_out(), 'status':"out"}, context_instance=RequestContext(request))
            elif(status == "In" or status == "in"):
                return render_to_response('main_page.html', {'error':employee.clock_in(), 'status':"in"}, context_instance=RequestContext(request))

        except Employee.DoesNotExist:
            return render_to_response('main_page.html', {'error':"user", 'user_name':user_name}, context_instance=RequestContext(request))

    return render_to_response('main_page.html', context_instance=RequestContext(request))

