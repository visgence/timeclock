from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from models import Employee, Time
from datetime import timedelta, datetime, time
from check_access import check_access


def total_hours(request):

    if(request.method == 'POST'):
        user_name = request.POST.get('user_name')
        start_time = request.POST.get('from')
        end_time = request.POST.get('to')
        time_info = {'employee':user_name, 'times':[]}

        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d')
        end_time += timedelta(1)
        num_days = end_time - start_time

        time = Time.objects.filter(employee__user__username = user_name).filter(time_in__gte = start_time.date()).filter(time_in__lt = end_time.date())

        if(len(time) > 0):
            total_time = datetime.strptime("00:00:00", '%H:%M:%S')
            #total_time = datetime.time()

            for day in range(num_days.days):
                date = time.filter(time_in__day = start_time.day)
                sum_time = datetime.strptime("00:00:00", '%H:%M:%S')

                for record in date:
                    print record
                    sum_time += record.time_out - record.time_in
                    total_time += record.time_out - record.time_in
                    #print sum_time
                
                #print datetime.strftime(total_time, "%H:%M")

                #time_info['times'][datetime.strftime(start_time, "%Y-%m-%d %H:%M"), datetime.strftime(sum_time, "%H:%M")]
                time_info['times'].append([datetime.strftime(start_time, "%Y-%m-%d %H:%M"), datetime.strftime(sum_time, "%H:%M")])
                start_time += timedelta(1)
            time_info['total'] = datetime.strftime(total_time, "%H:%M")
            print time_info

    return render_to_response('total_hours.html', {'employee_hours':time_info}, context_instance=RequestContext(request))

def main_page(request):
    """
    The clock in page.  Grabs user input data to determine if the user can clock in/out.  Returns back a dictionary
    with information about the success or failure of clocking the employee in/out.
    """

    response = check_access(request)
    if(response):
        return response

    if (request.method == 'POST'):
        user_name = request.POST.get('user_name')
        status = request.POST.get('status')

        try:

            employee = Employee.objects.get(user__username=user_name)
            if(status == "Out" or status == "out"):
                return render_to_response('main_page.html', {'error':employee.clock_out(), 'status':"out"}, context_instance=RequestContext(request))
            elif(status == "In" or status == "in"):
                return render_to_response('main_page.html', {'error':employee.clock_in(), 'status':"in"}, context_instance=RequestContext(request))

        except Employee.DoesNotExist:
            return render_to_response('main_page.html', {'error':"user", 'user_name':user_name}, context_instance=RequestContext(request))

    return render_to_response('main_page.html', {'employee':Employee.objects.all()}, context_instance=RequestContext(request))

