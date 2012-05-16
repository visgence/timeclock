from django.shortcuts import render_to_response from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from models import Employee, Time
from datetime import timedelta, datetime, time
from time import strftime
from check_access import check_access


def total_hours(request):
    #make sure the employee is logged in
    response = check_access(request)
    if(response):
        return response

    if(request.method == 'POST'):
        pay_period = {} 
        start_time = request.POST.get('from')
        end_time = request.POST.get('to')
        user_name = request.POST.get('user_name')

        #make sure we have actual date ranges coming in
        if(start_time == "" or end_time == ""):
            start_time = datetime.strftime(datetime.now(), '%Y-%m-%d')
            end_time = datetime.strftime(datetime.now(), '%Y-%m-%d')

        start_date = datetime.strptime(start_time, '%Y-%m-%d')
        end_date = datetime.strptime(end_time, '%Y-%m-%d')

        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d')
        end_time += timedelta(1)
        num_days = end_time - start_time

        period_total = 0 #total time for work period

        #iterate through our date-range
        day_count = (end_date - start_date).days + 1
        for single_date in [d for d in (start_date + timedelta(n) for n in range(day_count)) if d <= end_date]:
            daily_stuff = get_daily_hours(single_date, user_name)
            period_total += daily_stuff['total']

        #calculate total time
        return render_to_response('total_hours.html', {'pay_period':pay_period, 'employee':user_name}, context_instance=RequestContext(request))

    return render_to_response('login.html', context_instance=RequestContext(request))


def get_week_range(begin_date, end_date):




def get_daily_hours(date, user_name):
    '''
    Gets the total hours and minutes worked for a given date.  

    Paremeters: 
        date      = The date we are calculating hours for
        user_name = The employee that we are calculating hours for

    Returns:
        A dictionary with the following keys:
            time_info   = A list with the calculated daily hours for a specific date: [date, hours:minutes]
            daily_total = The total number of seconds for the day worked
    '''

    daily_total = 0
    daily_info = None
    shifts = []
 
    #find all clock in-outs for this day
    shifts = Time.objects.filter(employee__user__username = user_name).filter(time_in__year = date.year).filter(time_in__month = date.month).filter(time_in__day = date.day)

    #No shifts for this day so 00 hours and minutes
    if not shifts:
        daily_info = {'date': date, 'shifts':shifts, 'total':"0.0"}
    else:
        for shift in shifts:
            time_in = shift.time_in
            time_out = shift.time_out

            if(time_in != None and time_out != None):
                time_dif = round_seconds(get_seconds(time_out) - get_seconds(time_in))
                shifts.append({'in':time_in, 'out':time_out, 'total':time_dif}) 
                daily_total += time_dif

        daily_info = {'date': date, 'shifts':shifts, 'total':daily_total}

    return daily_info



def get_seconds(date):
    '''
    returns the number of seconds for a given datetime stamp.

    Parameters:
        date = The datetime object

    Returns:
        0 if date is null or the number of total seconds given for the given datetime object
    '''

    if(date):
        return (date.hour * 3600) + (date.minute * 60) + date.second
    return 0



def main_page(request):

    response = check_access(request)
    if(response):
        return response

    user_name = ""
    employee = None
    
    if(request.user.username != None and request.user.username != ""):
        user_name = request.user.username
    else:
        return render_to_response('login.html', context_instance=RequestContext(request))

    try:
        employee = Employee.objects.get(user__username=user_name)
        
        if (request.method == 'POST'):
            status = request.POST.get('status')
            if(status == "Out" or status == "out"):
                extra = get_extra(employee, "out", "")
                return render_to_response('main_page.html', extra , context_instance=RequestContext(request))
            elif(status == "In" or status == "in"):
                extra = get_extra(employee, "in", "")
                return render_to_response('main_page.html', extra, context_instance=RequestContext(request))

    except Employee.DoesNotExist:
        extra = get_extra(employee, "", "employee_does_not_exists")
        return render_to_response('main_page.html', extra, context_instance=RequestContext(request))

    extra = get_extra(employee, "", "")
    employee.get_current_time()
    return render_to_response('main_page.html', extra, context_instance=RequestContext(request))


def get_extra(employee, status, error):
    '''
    Helper function that based on a status and error message packages up a dictionary of extra stuff needed by the main page request.

    Parameters: 
        employee    = The Employee that is logged in and doing stuff.
        status      = in/out based on whether or not the employee is clocking in/out.  Can be "" if not clocking.
        error       = "" if no error otherwise specific errors based on the main page.

    Returns:
        A dictionary with all the stuff needed by the main page so that it can return.
    '''

    extra = {
                'employee':Employee.objects.all(),
                'is_admin':employee.user.is_staff,
            }

    if((status == "Out" or status == "out") and error == ""):
        extra['error'] = employee.clock_out()
        extra['status'] = "out"

        which_clock = Employee.objects.get(user__username=employee.user.username).which_clock()
        shift = which_clock['max_record'].time_out - which_clock['max_record'].time_in
        extra['user_status'] = which_clock['status']
        #extra['time'] = round_seconds(shift.days * 86400 + shift.seconds)
    elif((status == "In" or status == "in") and error == ""):
        extra['error'] = employee.clock_in()
        extra['status'] = "in"

        which_clock = Employee.objects.get(user__username=employee.user.username).which_clock()
        extra['user_status'] = which_clock['status']
    elif(status == "" and error == "employee_does_not_exist"):
        extra['error'] = "exception"
        extra['user_name'] = employee.user.username

        which_clock = Employee.objects.get(user__username=employee.user.username).which_clock()
        extra['user_status'] = which_clock['status']
    elif(status == "" and error == ""):
        extra['error'] = "none"
        extra['status'] = "none"

        which_clock = Employee.objects.get(user__username=employee.user.username).which_clock()
        shift = datetime.now() - which_clock['max_record'].time_in
        #extra['time'] = round_seconds(shift.days * 86400 + shift.seconds)
        extra['user_status'] = which_clock['status']

    return extra


                

def round_seconds(seconds):
    minutes = seconds / 60
    remainder = seconds % 60 

    if(remainder >= 30):
        minutes += 1

    return minutes * 60

#This helper function will take seconds and will return a dictionary with 
#hours and minutes. It will properly round minutes and increment the hour
#if it rounds to 60 min.
#return: dictionary in the form {'hour':hours, 'minutes': minutes}
'''
def sec_to_shift(seconds):
    hours = seconds / 3600 
    minutes = (seconds - (hours * 3600)) /60

    #rounding minutes to nearest 15
    remainder = minutes % 15

    if(remainder <= 7):
        minutes = minutes - remainder
    else:
        minutes = minutes + (15 - remainder)
        #sum_time = sum_time + timedelta(minutes = (15 - remainder))
        #total_time = total_time + timedelta(minutes = (15 - remainder))

    #handle the case where minutes was rounded to 60 and increment hour
    if minutes >= 60:
        hours +=1
        minutes = 0 

    return (hours * 3600) + (minutes * 60)
'''








