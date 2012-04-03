from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from models import Employee, Time
from datetime import timedelta, datetime, time
from check_access import check_access


def total_hours(request):
    #make sure the employee is logged in
    response = check_access(request)
    if(response):
        return response

    if(request.method == 'POST'):
        start_time = request.POST.get('from')
        end_time = request.POST.get('to')
        user_name = request.POST.get('user_name')
        time_info = {'employee':user_name, 'times':[]}


        #make sure we have actual date ranges coming in
        if(start_time == "" or end_time == ""):
            start_time = datetime.strftime(datetime.now(), '%Y-%m-%d')
            end_time = datetime.strftime(datetime.now(), '%Y-%m-%d')

        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d')
        end_time += timedelta(1)
        num_days = end_time - start_time

        #Get all Time records for the given time range
        time = Time.objects.filter(employee__user__username = user_name).filter(time_in__gte = start_time.date()).filter(time_in__lt = end_time.date())
        #print time

        if(len(time) > 0):
            total_time = datetime.strptime("00:00", '%H:%M')
            #total_time = datetime.time()

            #print num_days
            for day in range(num_days.days):
                #print day
                date = time.filter(time_in__day = start_time.day).filter(time_in__month = start_time.month).filter(time_in__year = start_time.year)
                print date
                sum_time = datetime.strptime("00:00", '%H:%M')

                #Sum the times for a given day
                for record in date:
                    #print record
                    if(record.time_out != None and record.time_out != ''):
                        print "record time-out, %s" % record.time_out
                        sum_time += record.time_out - record.time_in
                        total_time += record.time_out - record.time_in

                #print datetime.strftime(total_time, "%H:%M") #DEBUG

                if(len(date) > 0):
                    #rounding minutes to nearest 15
                    remainder = sum_time.minute % 15

                    if(remainder <= 7):
                        sum_time = sum_time - timedelta(minutes = remainder)
                        total_time = total_time - timedelta(minutes = remainder)
                    else:
                        sum_time = sum_time + timedelta(minutes = (15 - remainder))
                        total_time = total_time + timedelta(minutes = (15 - remainder))

                    time_info['times'].append([datetime.strftime(start_time, "%Y-%m-%d"), datetime.strftime(sum_time, "%H:%M")])
                start_time += timedelta(1)

            time_info['total'] = datetime.strftime(total_time, "%H:%M")

        return render_to_response('total_hours.html', {'employee_hours':time_info}, context_instance=RequestContext(request))

    return render_to_response('login.html', context_instance=RequestContext(request))

def main_page(request):

    response = check_access(request)
    if(response):
        return response

    user_name = ""
    if(request.user.username != None and request.user.username != ""):
        user_name = request.user.username
    else:
        return render_to_response('login.html', context_instance=RequestContext(request))

    if (request.method == 'POST'):
        status = request.POST.get('status')
        try:
            employee = Employee.objects.get(user__username=user_name)

            if(status == "Out" or status == "out"):
                extra = {'employee':Employee.objects.all(), 'is_admin':request.user.is_staff, 'error':employee.clock_out(), 'status':"out"}
                return render_to_response('main_page.html', extra , context_instance=RequestContext(request))
            elif(status == "In" or status == "in"):
                extra = {'employee':Employee.objects.all(), 'is_admin':request.user.is_staff, 'error':employee.clock_in(), 'status':"in"}
                return render_to_response('main_page.html', extra, context_instance=RequestContext(request))

        except Employee.DoesNotExist:
            extra = {'employee':Employee.objects.all(), 'is_admin':request.user.is_staff, 'error':"exception", 'user_name':user_name}
            return render_to_response('main_page.html', extra, context_instance=RequestContext(request))

    extra = {'employee':Employee.objects.all(), 'is_admin':request.user.is_staff}
    return render_to_response('main_page.html', extra, context_instance=RequestContext(request))

