from django.shortcuts import render_to_response 
from django.template import RequestContext
from clocker.models import Employee, Shift
from datetime import timedelta, datetime, date
from decimal import Decimal
import check_db

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
    pay_period = {'weekly_info':[], 'period_total':0, 'period_adjusted':0, 'period_overtime':0,'period_regular':0} 
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


    week = {'weekly_total':Decimal(0.0), 'weekly_adjusted': Decimal(0.0), 'weekly_overtime': Decimal(0.0), 'days':[]}

    #iterate through our date-range
    day_count = (period_end - period_begin).days + 1

    for single_date in [d for d in (period_begin + timedelta(n) for n in range(day_count)) if d <= end_date]:
        
        single_date = date(single_date.year, single_date.month, single_date.day) 

        daily_info = get_daily_hours(single_date, start_date, end_date, user_name)
        week['weekly_adjusted'] += daily_info['daily_adjusted']
        week['weekly_total'] += daily_info['daily_total']
        week['days'].append(daily_info)
        week['week_start'] = week_begin
        week['week_end'] = week_end
        pay_period['period_total'] += daily_info['daily_total']
        pay_period['period_adjusted'] += daily_info['daily_adjusted']

        if(single_date >= week_end or single_date >= end_date.date()):
            if(week['weekly_adjusted'] > Decimal(40.0)):
                week['weekly_regular_hours'] = Decimal(40.0)
            else:
                week['weekly_regular_hours'] = week['weekly_adjusted']

            if(week['weekly_total'] > Decimal(40.0)):
                weekly_overtime = week['weekly_total'] - Decimal(40.0)
               
                week['weekly_overtime'] = weekly_overtime
                pay_period['period_overtime'] += weekly_overtime
            
            pay_period['period_regular'] += week['weekly_regular_hours']
            pay_period['weekly_info'].append(week)
            week_begin = week_end + timedelta(days = 1)
            week_end = week_begin + timedelta(days = 6)
            week = {'weekly_total': Decimal(0.0), 'weekly_adjusted':Decimal(0.0),'weekly_regular_hours': Decimal(0.0), 'weekly_overtime': Decimal(0.0), 'week_start':week_begin, 'week_end':week_end, 'days':[]}
    
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


