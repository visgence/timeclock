from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from check_access import check_access
from models import ShiftSummary, Shift, Employee, Job


def summary(request):

    response = check_access(request)
    if(response):
        return response

    if(request.method == 'POST'):

        summaries = request.POST.get('json')

        if(summaries):

            for summary in summaries:

                job = Job.objects.get(id = summary['job_id'])
                employee = Employee.objects.get(id = summary['emp_id'])
                shift = Shift.objects.get(id = summary['shift_id'])
                miles = summary['miles']
                hours = summary['hours']
                note = summary['note']

                shift_summary = ShiftSummary(job = job,
                                             employee = employee,
                                             shift = shift,
                                             hours = hours,
                                             note = note)
                shift_summary.save()

    return HttpResponseRedirect('/timeclock/')
    
