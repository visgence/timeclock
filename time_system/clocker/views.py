from django.shortcuts import render_to_response
from django.template import RequestContext
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
        start_time = request.POST.get('from')
        end_time = request.POST.get('to')
        user_name = request.POST.get('user_name')
        time_info = {'employee':user_name, 'times':[]}

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

        total_time = datetime.strptime("00:00", '%H:%M')#total time for work period
        period_total = 0 #total time for work period

        #iterate through our date-range
        day_count = (end_date - start_date).days + 1
        for single_date in [d for d in (start_date + timedelta(n) for n in range(day_count)) if d <= end_date]:
            daily_total = 0 #total time worked for a specific day in seconds
            #print "Date: %s" % strftime("%Y-%m-%d", single_date.timetuple())#DEBUG
            #print "Day: %s" % single_date#DEBUG
            #sum_time = datetime.strptime("00:00", '%H:%M')#total time for a specific day

            #find all clock in-outs for this day
            shifts = Time.objects.filter(employee__user__username = user_name).filter(time_in__year = single_date.year).filter(time_in__month = single_date.month).filter(time_in__day = single_date.day)
            #print "time : %s" % time#DEBUG

            #if there is not shifts on this date enter 0 hours.
            if not shifts:
                print "\nNo shifts on %s" % single_date#DEBUG
                time_info['times'].append([datetime.strftime(single_date, "%Y-%m-%d"), '00:00'])

            #else loop through the shifts and calculate total_hours for the day
            else:
                for shift in shifts:
                    time_in = shift.time_in
                    time_out = shift.time_out

                    print "\nshift: %s" % shift#DEBUG
                    #print "total seconds: %s" % shift_in_seconds
                    
                    
                    #hours = abs(time_dif).total_seconds() / 3600.0

                    if(time_in != None and time_out != None):
                        time_dif = time_out - time_in
                        shift_in_seconds = time_dif.days * 86400 + time_dif.seconds

                        #a
                        daily_total += shift_in_seconds
                        period_total += shift_in_seconds
                    
                        
                time_worked_daily= sec_to_shift(daily_total)
                print "time: %s" % time_worked_daily
                time_info['times'].append([datetime.strftime(single_date, "%Y-%m-%d"), '%s:%s' % (time_worked_daily['hours'],time_worked_daily['minutes'])])
            #time_info['times'].append([datetime.strftime(single_date, "%Y-%m-%d"), datetime.strftime(sum_time, "%H:%M")])

            
            #add total time for this day
            #time_info['times'].append([datetime.strftime(single_date, "%Y-%m-%d"),"%s:%s" % (hours,minutes)])

        #calculate total time
        total_time_worked =  sec_to_shift(period_total)
        time_info['total'] = "%s:%s" % (total_time_worked['hours'],total_time_worked['minutes'])
        print "Total time worked for this period: %s" % time_info['total'] 
        return render_to_response('total_hours.html', {'employee_hours':time_info}, context_instance=RequestContext(request))

    return render_to_response('login.html', context_instance=RequestContext(request))

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
        employee = The Employee that is logged in and doing stuff.
        status   = in/out based on whether or not the employee is clocking in/out.  Can be "" if not clocking.
        error    = "" if no error otherwise specific errors based on the main page.

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
        extra['time'] = sec_to_shift(shift.days * 86400 + shift.seconds)
    elif((status == "In" or status == "in") and error == ""):
        extra['error'] = employee.clock_in()
        extra['status'] = "in"
        
        which_clock = Employee.objects.get(user__username=employee.user.username).which_clock()
        shift = datetime.now() - which_clock['max_record'].time_in
        extra['user_status'] = which_clock['status']
        extra['time'] = sec_to_shift(shift.days * 86400 + shift.seconds)
    elif(status == "" and error == "employee_does_not_exist"):
        extra['error'] = "exception"

        which_clock = Employee.objects.get(user__username=employee.user.username).which_clock()

        extra['user_name'] = employee.user.username
        extra['user_status'] = which_clock['status']
    elif(status == "" and error == ""):
        which_clock = Employee.objects.get(user__username=employee.user.username).which_clock()

        extra['user_status'] = which_clock['status']

    return extra


                


#This helper function will take seconds and will return a dictionary with 
#hours and minutes. It will properly round minutes and increment the hour
#if it rounds to 60 min.
#return: dictionary in the form {'hour':hours, 'minutes': minutes}
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

    hours = str(hours);
    minutes = str(minutes);

    if(len(hours) == 1):
        hours = '0' + hours;
    if(len(minutes) == 1):
        minutes = '0' + minutes;

    return {'hours':hours, 'minutes':minutes}








