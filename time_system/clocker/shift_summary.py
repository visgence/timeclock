from django.http import HttpResponseRedirect
from check_access import check_access
from models import ShiftSummary, Shift, Employee, Job
from django.utils import simplejson


def summary(request):

    response = check_access(request)
    if(not isinstance(response, Employee)):
        return response

    if(request.method == 'POST'):
        json = simplejson.loads(request.POST['json'])

        if(json):

            employee = Employee.objects.get(id = json['emp_id'])
            shift = Shift.objects.get(id = json['shift_id'])

            for summary in json['shift_summary']:

                job = Job.objects.get(id = summary['job_id'])
                miles = summary['miles']
                hours = summary['hours']
                note = summary['notes']


                shift_summary = ShiftSummary(job = job,
                                             employee = employee,
                                             shift = shift,
                                             hours = hours,
                                             miles = miles,
                                             note = note)

                shift_summary.save()

    return HttpResponseRedirect('/timeclock/')
    
