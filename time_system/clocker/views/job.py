
# System Imports
from datetime import datetime, timedelta
from decimal import Decimal
from collections import OrderedDict

# Django Imports
from django.template import RequestContext, loader
from django.http import HttpResponse

# Local Imports
from clocker.models import Employee, Job, ShiftSummary

def jobBreakdown(request):

    employees = []
    if not request.user.is_superuser:
        employees.append(request.user.username)
    else:
        employee = request.POST['employee']
        if employee != 'all':
            employees.append(employee)

    start = str(request.POST.get('start', None))
    end = str(request.POST.get('end', None))

    breakdown = getJobsBreakdown(employees, start, end)

    t = loader.get_template('jobBreakdown.html')
    c = RequestContext(request, {'jobsBreakdown': breakdown})
    return HttpResponse(t.render(c))


def getWeekdayRange(start=None, end=None):
    '''
    ' Calculates the work week from a start and end time and returns those as datetime objects.
    ' 
    ' The start and end times will always try to encapsulate a work week if they are not specified.
    ' EX: You specify a date that is a Wednesday for the end time.  Start will then push back to that Monday, the
    '     beginning of that work week. Likewise if you specified that date for the start time instead then the end
    '     time would then extend to that upcoming Sunday if possible, the end of that work week.
    '
    ' Keyword Args:
    '   start     - (optional) Starting time to begin aggregating hours worked from. Should be a string in the format
    '               %Y-%m-%d 
    '   end       - (optional) Ending time to begin aggregating hours worked to. Should be a string in the format 
    '               %Y-%m-%d
    '
    ' Returns: tuple (start, end) containing the start of a work week and the end of a work week
    '''

    dateForm = "%Y-%m-%d"

    if (start is None or start == '') and end is not None and end != '':
        end = datetime.strptime(end, dateForm)
        start = end - timedelta(end.weekday())    
    elif (end is None or end == '') and start is not None and start != '':
        start = datetime.strptime(start, dateForm)
        startOfWeek = start - timedelta(start.weekday())
        end = startOfWeek + timedelta(6)
    elif end is not None and end != '' and start is not None and start != '':
        start = datetime.strptime(start, dateForm)
        end = datetime.strptime(end, dateForm)
    else:
        today = datetime.today()
        start = today - timedelta(today.weekday())
        end = start + timedelta(6)


    start = start.replace(hour=00)
    start = start.replace(minute=00)
    start = start.replace(second=00)
    start = start.replace(microsecond=00)

    end = end.replace(hour=23)
    end = end.replace(minute=59)
    end = end.replace(second=59)
    end = end.replace(microsecond=00)

    assert start <= end, "Start date %s is greater than the end date %s" % (str(start), str(end))
    return (start, end)


def getJobsBreakdown(employees=None, start=None, end=None):
    '''
    ' Calculates the hourly precentages for all jobs within a timerange for an employee or employees.
    ' If no employees are specified then all employees will be used.
    ' 
    ' The start and end times will always try to encapsulate a work week if they are not specified.
    ' EX: You specify a date that is a Wednesday for the end time.  Start will then push back to that Monday, the
    '     beginning of that work week. Likewise if you specified that date for the start time instead then the end
    '     time would then extend to that upcoming Sunday if possible, the end of that work week.
    '
    ' Keyword Args:
    '   employees - (optional) A list of Employees to aggregate their total hours worked on the jobs in the system.
    '   start     - (optional) Starting time to begin aggregating hours worked from. Should be a string in the format
    '               %Y-%m-%d 
    '   end       - (optional) Ending time to begin aggregating hours worked to. Should be a string in the format 
    '               %Y-%m-%d
    '
    ' Returns: A dictionary of jobs and their total percentage of hours that was worked for them.
    '          {
    '             jobs: {
    '                job1: {hours: <total hours>, percentage: <% of total_hours>, active: <True/False>},
    '                job2: {hours: <total hours>, percentage: <% of total_hours>, active: <True/False>},
    '                ...
    '             },
    '             total_hours: <total hours for all jobs>,
    '             employees: [username1, username2, ...]
    '          }
    '''

    start, end = getWeekdayRange(start, end)
    if employees is None or len(employees) <= 0:
        employees = Employee.objects.filter(is_active=True)
    else:
        try:
            e = ''
            employees = [Employee.objects.get(username=e, is_active=True) for e in employees]
        except Employee.DoesNotExist:
            return "No employee with username %s" % str(e)

    jobData = {
        'jobs': OrderedDict()
        ,'total_hours': 0
        ,'employees': []
    }
    
    jobs = Job.objects.all().order_by('name')
    for employee in employees:
        jobData['employees'].append(employee.username)
       
        for job in jobs:
            #initialize data if not in there yet.
            if job.name not in jobData['jobs']:
                jobData['jobs'][job.name] = {
                    'hours': 0.0,
                    'percentage': 0.0,
                    'active': job.is_active,
                    'summaries': [],
                    'percentages': {}
                }



            hours = employee.getJobHours(start, end, job)
            if hours > 0 and employee not in jobData['jobs'][job.name]['percentages']:
                jobData['jobs'][job.name]['percentages'][employee.username] = {
                    "employee": employee,
                    "hours": hours,
                }
            elif hours > 0:
                jobData['jobs'][job.name]['percentages'][employee.username]['hours'] += hours

            jobData['total_hours'] += hours
            jobData['jobs'][job.name]['summaries'].extend(job.get_summaries(employee, start, end))
            jobData['jobs'][job.name]['hours'] += hours


    for job, data in jobData['jobs'].iteritems():
        data['summaries'] = sorted(data['summaries'], key=lambda summary: summary.shift.time_in, reverse=True)

    #Calculate percentages as a Decimal
    for jobN, jobD in jobData['jobs'].iteritems():
        if jobData['total_hours'] > 0:
            jobPercentage = Decimal((jobD['hours']*100) / jobData['total_hours']).quantize(Decimal('1.00'))
            jobD['percentage'] = str(jobPercentage)

        for username, percentageD in jobD['percentages'].iteritems():
            if percentageD['hours'] > 0:
                percentage = str((Decimal((percentageD['hours']*100) / jobData['total_hours'])).quantize(Decimal('1.00')))
                percentageD['percentage'] = percentage

        jobD['hours'] = str(Decimal(jobD['hours']).quantize(Decimal('1.00')))
    

    jobData['total_hours'] = str(Decimal(jobData['total_hours']).quantize(Decimal('1.00')))
    return jobData


