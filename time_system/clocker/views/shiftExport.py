from django.http import HttpResponse
from clocker.views.job import getWeekdayRange

# Local Imports
from clocker.models import Employee, Job
from settings import ENABLE_JOBS


def shiftExport(request):
    # If not super user only do for current employee
    employee = request.user
    employees = [employee]

    if employee.is_superuser:
        employees = Employee.objects.filter(is_active=True)

    start_str = str(request.GET.get('start', None))
    end_str = str(request.GET.get('end', None))

    if start_str == 'None':
        start_str = None

    if end_str == 'None':
        end_str = None

    start, end = getWeekdayRange(start_str, end_str)
    jobs = Job.objects.all().order_by('name')
    output = []
    for employee in employees:
        for job in jobs:
            summaries = job.get_summaries(employee, start, end)
            for summary in summaries:
                data = []
                data.append(summary.shift.time_in.strftime("%Y-%m-%d %H:%M:%S"))
                data.append(summary.shift.time_out.strftime("%Y-%m-%d %H:%M:%S"))
                data.append('"{} {}"'.format(employee.first_name, employee.last_name))
                if ENABLE_JOBS:
                    data.append('"{}"'.format(job.name))
                data.append("{:.2f}".format(summary.hours/3600.0))
                if ENABLE_JOBS:
                    data.append("{:.2f}".format(summary.miles if summary.miles else 0.00))
                data.append('"{}"'.format(summary.note.replace("\n", "")))
                output.append(",".join(data))
    output.sort()
    if len(output) == 0:
        output = [(f"No Results for {start} through {end}")]
    return HttpResponse("\n".join(output), content_type="text/plain")
