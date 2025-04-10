from clocker.models import Employee
from clocker.views.timesheet import getPayPeriod
from datetime import date, timedelta
from time import gmtime, strftime
from django.shortcuts import render
from find_missing import findMissing
from settings import ENABLE_JOBS


def mainPage(request):

    employee = request.user
    employees = [employee]
    if employee.is_superuser:
        employees = Employee.objects.filter(is_active=True)

    status = employee.isClockedIn()
    recentShift = employee.getCurrentShift()

    timeStamp = ''
    message = "It appears that you have never clocked in before.\
                Please clock in to start using Timeclock!"

    if recentShift is not None:
        timeStamp = "{} ({})".format(recentShift.time_in.strftime('%B %d, %Y, %I:%M %p'), strftime("%Z", gmtime()))
        message = "You are clocked in. You clocked in at "
    if recentShift is not None and not status:
        message = "You are clocked out. You last clocked out at "
        timeStamp = "{} ({})".format(recentShift.time_out.strftime('%B %d, %Y, %I:%M %p'), strftime("%Z", gmtime()))

    today = date.today()
    start_week = today - timedelta(today.weekday())
    end_week = start_week + timedelta(7)
    periodData = getPayPeriod(start_week.strftime('%Y-%m-%d'), end_week.strftime('%Y-%m-%d'), employee.username)

    missingShifts = []
    if ENABLE_JOBS:
        for i in findMissing():
            if employee.toDict()['id'] == i.toDict()['employee']['id']:
                missingShifts.append({
                    "link": i.toDict()['id'],
                    "date": i.toDict()['time_out']
                })

    context = {
        'employee': employee,
        'employees': employees,
        'status': status,
        'message': message,
        'timeStamp': timeStamp,
        'start_week': date.strftime(start_week, '%Y-%m-%d'),
        'today': date.strftime(today, '%Y-%m-%d'),
        'weekly_regular': periodData['pay_period']['period_regular'],
        'weekly_overtime': periodData['pay_period']['period_overtime'],
        'missing_shifts': missingShifts,
        'enable_jobs': ENABLE_JOBS
    }

    return render(request, 'mainPage.html', context)
