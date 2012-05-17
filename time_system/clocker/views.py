from django.shortcuts import render_to_response 
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from models import Employee, Time
from datetime import timedelta, datetime, time
from time import strftime
from check_access import check_access
from decimal import *


def total_hours(request):
    #make sure the employee is logged in
    response = check_access(request)
    if(response):
        return response

    if(request.method == 'POST'):
        pay_period = {'weekly_info':[], 'period_total':0, 'period_adjusted':0, 'period_overtime':0} 
        start_time = request.POST.get('from')
        end_time = request.POST.get('to')
        user_name = request.POST.get('user_name')
        
        #make sure we have actual date ranges coming in
        if(start_time == "" or end_time == ""):
            start_time = datetime.strftime(datetime.now(), '%Y-%m-%d')
            end_time = datetime.strftime(datetime.now(), '%Y-%m-%d')

        start_date = datetime.strptime(start_time, '%Y-%m-%d')
        end_date = datetime.strptime(end_time + " 23:59:59", '%Y-%m-%d %H:%M:%S')

        print end_date

        #Get weekly period for our start and end range
        period_range = get_week_range(start_date, end_date)
        period_begin = period_range['begin']
        period_end = period_range['end']
        week_begin = period_begin
        week_end = week_begin + timedelta(days = 6)
        #print "beginning period %s" % period_begin #DEBUG 
        #print "ending period %s" % period_end 


        period_total = 0 #total time for work period
        period_adjusted = 0
        week = {'weekly_total':0, 'weekly_adjusted':0, 'weekly_overtime':0, 'days':[]}

        #iterate through our date-range
        day_count = (period_end - period_begin).days + 1

        for single_date in [d for d in (period_begin + timedelta(n) for n in range(day_count)) if d <= period_end]:
            
            daily_info = get_daily_hours(single_date, start_date, end_date, user_name)
            week['weekly_adjusted'] += daily_info['daily_adjusted']
            week['weekly_total'] += daily_info['daily_total']
            week['days'].append(daily_info)
            week['week_start'] = week_begin
            week['week_end'] = week_end
            pay_period['period_total'] += daily_info['daily_total']
            pay_period['period_adjusted'] += daily_info['daily_adjusted']

            
            if(single_date >= week_end):
                if((week['weekly_total'] / 3600) > 40):
                   weekly_overtime = ((week['weekly_total'] / 3600) - 40) * 3600
                   week['weekly_overtime'] = weekly_overtime
                   pay_period['period_overtime'] += weekly_overtime

                pay_period['weekly_info'].append(week)
                week_begin = week_end
                week_end = week_begin + timedelta(days = 6)
                week = {'weekly_total':0, 'weekly_adjusted':0, 'weekly_overtime':0, 'week_start':week_begin, 'week_end':week_end, 'days':[]}

    

        return render_to_response('total_hours.html', {'pay_period':pay_period, 'employee':user_name}
                , context_instance=RequestContext(request))

    return render_to_response('login.html', context_instance=RequestContext(request))


def get_week_range(begin_date, end_date):
    
    new_begin = begin_date - timedelta(days = begin_date.weekday())
    new_end = end_date + timedelta(days = (6 - end_date.weekday()))
    return {'begin':new_begin, 'end':new_end}



def get_daily_hours(date, start, end, user_name):
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
    adjusted_time = 0 
    daily_info = None
    shift_info = []
 
    #find all clock in-outs for this day
    shifts = Time.objects.filter(employee__user__username = user_name).filter(time_in__year = date.year).filter(time_in__month = date.month).filter(time_in__day = date.day)

    #No shifts for this day so 00 hours and minutes
    if not shifts:
        daily_info = {'date':  datetime.strftime(date, '%Y-%m-%d'), 'shifts':shift_info, 'daily_total':0, 'daily_adjusted':0}
    else:
        for shift in shifts:
            time_in = shift.time_in
            time_out = shift.time_out

            print shift

            if(time_in != None and time_out != None):
                time_dif = round_seconds(get_seconds(time_out) - get_seconds(time_in))

                time_calc = Decimal(time_dif)/3600
                print "time calculation: %s" % time_calc    

                if(time_in >= start and time_out <= end):
                    shift_info.append({'in':time_in, 'out':time_out, 'total':time_dif, 'display_flag':True}) 
                    adjusted_time += time_dif
                else:
                    shift_info.append({'in':time_in, 'out':time_out, 'total':time_dif, 'display_flag':False}) 

                daily_total += time_dif

        daily_info = {'date': date, 'shifts':shift_info, 'daily_total':daily_total, 'daily_adjusted':adjusted_time}

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









