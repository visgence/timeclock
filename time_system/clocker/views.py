from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Employee


def main_page(request):

    if request.method == 'POST':
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

    return render_to_response('main_page.html', context_instance=RequestContext(request))
