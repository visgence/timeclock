

# Django imports
from django.shortcuts import render_to_response 
from django.template import RequestContext
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext, loader
from django.core.exceptions import ValidationError

# Local imports
from clocker.models import Employee, Shift, Timesheet
import check_db

# System imports
from datetime import timedelta, datetime, date
from decimal import Decimal
from copy import deepcopy
try:
    import simplejson as json
except ImportError:
    import json


class TimesheetsView(View):

    def get(self, request):

        accept = request.META['HTTP_ACCEPT']
        user = request.user

        if 'application/json' in accept:
            timesheets = [t.toDict() for t in Timesheet.objects.get_viewable(user)]
            return HttpResponse(json.dumps({'timesheetList': timesheets}), content_type="application/json")

        employees = Employee.objects.filter(is_active=True)
        t = loader.get_template('manageTimesheets.html')
        c = RequestContext(request, {
            "employees": employees
        })
        return HttpResponse(t.render(c), content_type="text/html")


    def post(self, request):
        user = request.user

        try:
            params = json.loads(request.read())
        except (ValueError, AssertionError) as e:
            error = 'Invalid data: ' + str(e)
            return HttpResponseBadRequest(json.dumps(error), content_type='application/json')

        try:
            employee = Employee.objects.get(id=params['employee'])
            params['employee'] = employee
        except Employee.DoesNotExist:
            return HttpResponseBadRequest(json.dumps("Employee %s does not exist" % str(params['employee'])), content_type='application/json')

        try:
            timesheet = Timesheet.objects.create_timesheet(params, user)
        except ValidationError as e:
            errors = [{x: y} for x, y in e.message_dict.iteritems()]
            return HttpResponseBadRequest(json.dumps(errors), content_type='application/json')

        return HttpResponse(json.dumps(timesheet.toDict(), indent=4), content_type="application/json")            


class TimesheetView(View):

    @staticmethod
    def updateTimesheet(timesheet, data, user):
        pass


    def put(self, request, timesheet_id):
        user = request.user

        try:
            params = json.loads(request.read())
        except (ValueError, AssertionError) as e:
            error = 'Invalid data: ' + str(e)
            return HttpResponseBadRequest(json.dumps(error), content_type='application/json')

        try:
            timesheet = Timesheet.objects.get(id=timesheet_id)
        except Timesheet.DoesNotExist:
            return HttpResponseBadRequest(json.dumps("Timesheet %s does not exist" % str(params['employee'])), content_type='application/json')

        try:
            timesheet.sign(user)
        except AssertionError as e:
            return HttpResponseBadRequest(json.dumps("Problem signing timesheet: %s" % str(e)), content_type='application/json')

        return HttpResponse(json.dumps(timesheet.toDict(), indent=4), content_type="application/json")            


def total_hours(request):

    if(request.method == 'POST'):
        check_db.main()

        start_time = request.POST.get('from')
        end_time = request.POST.get('to')
        user_name = request.POST.get('user_name')
        
        pay_data = getPayPeriod(start_time, end_time, user_name)
        return render_to_response('total_hours.html', pay_data, context_instance=RequestContext(request))
       
    return render_to_response('login.html', context_instance=RequestContext(request))


def getPayPeriod(start_time, end_time, user_name):

    employee = Employee.objects.get(username = user_name)
    #make sure we have actual date ranges coming in
    if(start_time == "" or end_time == ""):
        start_time = datetime.strftime(datetime.now(), '%Y-%m-%d')
        end_time = datetime.strftime(datetime.now(), '%Y-%m-%d')

    start_date = datetime.strptime(start_time, '%Y-%m-%d')
    end_date = datetime.strptime(end_time + " 23:59:59", '%Y-%m-%d %H:%M:%S')

    #Get weekly period for our start and end range
    period_range = get_week_range(start_date, end_date)
    period_begin = period_range['begin']
    period_end = period_range['end']
    week_begin = date(period_begin.year, period_begin.month, period_begin.day)
    week_end = week_begin + timedelta(days = 6)

    pay_period = {
        'weekly_info': [],
        'period_total': Decimal(0.0),
        'period_adjusted': Decimal(0.0), 
        'period_overtime': Decimal(0.0),
        'period_regular': Decimal(0.0)
    } 
        
    weekDefaults = {
        'weekly_total': Decimal(0.0), 
        'weekly_adjusted': Decimal(0.0), 
        'weekly_regular_hours': Decimal(0.0), 
        'weekly_overtime': Decimal(0.0),
        'days': []
    }

    #iterate through our date-range
    day_count = (period_end - period_begin).days + 1
    week = deepcopy(weekDefaults)
    week['week_start'] = week_begin
    week['week_end'] = week_end
    for single_date in [d for d in (period_begin + timedelta(n) for n in range(day_count)) if d <= end_date]:
        
        single_date = date(single_date.year, single_date.month, single_date.day) 
        daily_info = get_daily_hours(single_date, start_date, end_date, user_name)

        #If we just now will breach 40 hours seperate the hours leading up to 40 and the hours past 40 accordingly
        if week['weekly_total'] < Decimal(40.0) and week['weekly_total']+daily_info['daily_adjusted'] >= Decimal(40.0):
            adjusted = Decimal(40.0) - week['weekly_total']
            week['weekly_regular_hours'] += adjusted
            pay_period['period_regular'] += adjusted
           
            overtime =  (week['weekly_total']+daily_info['daily_adjusted']) - Decimal(40.0)
            week['weekly_overtime'] += overtime
            pay_period['period_overtime'] += overtime
        #If we're already in overtime just store it.
        elif week['weekly_total'] >= Decimal(40.0):
            week['weekly_overtime'] += daily_info['daily_adjusted']
            pay_period['period_overtime'] += daily_info['daily_adjusted']
        else:
            week['weekly_regular_hours'] += daily_info['daily_adjusted']
            pay_period['period_regular'] += daily_info['daily_adjusted']

        week['weekly_total'] += daily_info['daily_total']
        week['days'].append(daily_info)
        pay_period['period_total'] += daily_info['daily_total']

        if(single_date >= week_end or single_date >= end_date.date()):
            pay_period['weekly_info'].append(week)
            week_begin = week_end + timedelta(days = 1)
            week_end = week_begin + timedelta(days = 6)
            week = deepcopy(weekDefaults)
            week['week_start'] = week_begin
            week['week_end'] = week_end
    
    pay_period['period_adjusted'] = pay_period['period_adjusted'] - pay_period['period_overtime'] 
    overtime_pay = employee.hourly_rate + (employee.hourly_rate / Decimal(2.0))

    pay_period['total_regular'] = (pay_period['period_regular'] * employee.hourly_rate).quantize(Decimal('1.00'))
    pay_period['total_overtime'] = (pay_period['period_overtime'] * overtime_pay).quantize(Decimal('1.00'))
    total = (Decimal(pay_period['total_overtime'])+Decimal(pay_period['total_regular'])).quantize(Decimal('1.00'))

    return {'pay_period':pay_period, 'period_begin':start_time, 'period_end':end_time, 'employee':employee, 'overtime_pay': overtime_pay, 'total': total, 'employee': employee}



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

    daily_total = Decimal(0.0)
    adjusted_time = Decimal(0.0)
    daily_info = None
    shift_info = []
 
    #find all clock in-outs for this day
    shifts = Shift.objects.filter(employee__username = user_name).filter(time_in__year = date.year).filter(time_in__month = date.month).filter(time_in__day = date.day).exclude(time_in = None).exclude(time_out = None).order_by('time_in')

    #No shifts for this day so 00 hours and minutes
    if not shifts:
        daily_info = {'date':  date, 'shifts':shift_info, 'daily_total':Decimal(0.0), 'daily_adjusted':Decimal(0.0)}
    else:
        for shift in shifts:
            time_in = shift.time_in
            time_out = shift.time_out
          
            hours = shift.hours

            str_time_in = time_in.strftime('%I:%M %p') 
            str_time_out = time_out.strftime('%I:%M %p') 

            if(time_in >= start and time_out <= end):
                shift_info.append({'in':str_time_in, 'out':str_time_out, 'total':hours, 'display_flag':'True'}) 
                adjusted_time += hours
            else:
                shift_info.append({'in':str_time_in, 'out':str_time_out, 'total':hours, 'display_flag':'False'}) 

            daily_total += hours
            if daily_total > Decimal(24.0):
                raise Exception('A daily total is greater than 24 hours on the date '+str(date.month)+"-"+str(date.day)+"-"+str(date.year))
                
        if(date >= start.date() and date <= end.date()):
            daily_info = {'date': date, 'shifts':shift_info, 'daily_total':daily_total, 'daily_adjusted':adjusted_time, 'display_flag':'True'}
        else:
            daily_info = {'date': date, 'shifts':shift_info, 'daily_total':daily_total, 'daily_adjusted':adjusted_time, 'display_flag':'False'}

    return daily_info


