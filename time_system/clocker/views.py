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
                    
                    
#                    hours = abs(time_dif).total_seconds() / 3600.0

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
        
        """ 
        #TODO Not calculating correct hours
        #Get all Time records for the given time range
        time = Time.objects.filter(employee__user__username = user_name).filter(time_in__gte = start_time.date()).filter(time_in__lt = end_time.date())
        #print time

        if(len(time) > 0):
            total_time = datetime.strptime("00:00", '%H:%M')
            #total_time = datetime.time()

            #print num_days
            for day in range(num_days.days):
                #print "Day: %s" % day
                date = time.filter(time_in__day = start_time.day).filter(time_in__month = start_time.month).filter(time_in__year = start_time.year)
                #print date
                #print "Day: %s" % date
                sum_time = datetime.strptime("00:00", '%H:%M')

                #Sum the times for a given day
                for record in date:
                    #print record
                    if(record.time_out != None and record.time_out != ''):
                        #print "record time-out, %s" % record.time_out
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
            """
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


#This helper function will take seconds and will return a dictionary with 
#hours and minutes. It will properly round minutes and increment the hour
#if it rounds to 60 min.
#return: dictionary in the form {'hour':hours, 'minutes': minutes}
def sec_to_shift(seconds):
    hours = seconds / 3600 
    minutes = (seconds - (hours * 3600)) /60
    print "Hours for the day %s" % hours
    print "Minutes for the day %s" % minutes 

    #rounding minutes to nearest 15
    remainder = minutes % 15
    print "remainder: %s" % remainder

    if(remainder <= 7):
        minutes = minutes - remainder
    else:
        minutes = minutes + (15 - remainder)
        #sum_time = sum_time + timedelta(minutes = (15 - remainder))
        #total_time = total_time + timedelta(minutes = (15 - remainder))

    #print "Hours after rounding %s" % hours
    print "Minutes after rounding %s" % minutes 


    #handle the case where minutes was rounded to 60 and increment hour
    if minutes >= 60:
        hours +=1
        minutes = 0 
        print "New adjusted hour: %s" % hours
        print "New adjusted minute: %s" % minutes

    hours = str(hours);
    minutes = str(minutes);

    if(len(hours) == 1):
        hours = '0' + hours;
    if(len(minutes) == 1):
        minutes = '0' + minutes;

    return {'hours':hours, 'minutes':minutes}








