from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.db import transaction
from clocker.models import ShiftSummary, Shift, Job
from django.shortcuts import render

try:
    import simplejson as json
except ImportError:
    import json


@require_POST
#@transaction.commit_manually
def summary(request):
    '''
    ' Creates new Shift Summaries from the summary page for a shift. If any old summaries exist for that shift
    ' they are deleted first.
    '''

    employee = request.user

    try:
        jsonData = json.loads(request.POST['jsonData'])
    except Exception:
        transaction.rollback()
        return HttpResponseServerError("Error getting json data for shift summary")

    try:
        shift = Shift.objects.get(id = jsonData['shift_id'], employee=employee)
    except Shift.DoesNotExist:
        transaction.rollback()
        return HttpResponseServerError("Error getting shift while creating shift summary for employee %s" % str(employee))

    #Delete previously saved summaries since we're about to replace them
    ShiftSummary.objects.filter(shift=shift).delete()

    for summary in jsonData['shift_summary']:
        kwargs = {'employee': employee, 'shift': shift}
        kwargs['miles'] = summary['miles']
        kwargs['hours'] = summary['hours']
        kwargs['note'] = summary['notes']
        try:
            kwargs['job'] = Job.objects.get(id = summary['job_id'])
        except Job.DoesNotExist:
            transaction.rollback()
            return HttpResponseServerError("Error getting job while creating shift summary for employee %s" % str(employee))

        shift_summary = ShiftSummary(**kwargs)
        try:
            shift_summary.full_clean(exclude="note")
        except ValidationError as e:
            transaction.rollback()
            msg = "New shift summary didn't pass validation for employee %s: %s" % (str(employee), str(e))
            return HttpResponseServerError(msg)

        shift_summary.save()

    transaction.commit()
    return HttpResponseRedirect('/timeclock/')


def renderSummary(request, id):
    '''
    ' Renders the shift summary page. Makes sure to check if the shift for the given id has any
    ' past complete summaries and if so packages them up so the page can pre-fill using their data.
    '
    ' Keyword Args: Id of the Shift we are rendering the summary page for.
    '''
    print "\n\nhello there"
    employee = request.user
    try:
        shift = Shift.objects.get(id=id)
        shiftEmployee = shift.employee
    except Shift.DoesNotExist:
        return HttpResponseServerError('Shift does not exist for id %s' % str(id))

    owner = True
    if not request.user.is_superuser and request.user != shift.employee:
        return HttpResponseForbidden('Permission denied')
    elif request.user != shift.employee:
        owner = False

    #Only complete shifts can have summaries
    if shift.time_out == None:
        return HttpResponseServerError('You cannot complete any summaries for a shift where you are not clocked out yet.')

    #We only care about tracking time that's at least one minute
    timeDiff = shift.time_out - shift.time_in
    totalTime = roundSeconds(timeDiff.total_seconds())
    if totalTime < 60:
        totalTime = 0
        return HttpResponseRedirect('/timeclock/')

    jobs = Job.objects.filter(is_active=True)
    summaries = ShiftSummary.objects.filter(shift=shift, job__in=jobs)

    jobData = []
    for j in jobs:
        job = {'job': j}
        try:
            summary = ShiftSummary.objects.get(shift=shift, job=j)
        except ShiftSummary.DoesNotExist:
            jobData.append(job)
            continue

        job['hours'] = summary.hours
        job['miles'] = summary.miles
        job['note'] = summary.note
        jobData.append(job)

    context = {
        'totalTime': totalTime,
        'jobData': jobData,
        'shift': shift,
        'summaries': summaries,
        'shiftEmployee': shiftEmployee,
        'owner': owner
    }
    return render(request, 'shiftSummary.html', context)


def roundSeconds(seconds):
    '''
    ' Utility method to round a number of seconds given.
    '
    ' Returns: Seconds rounded to the nearest minute by 30 seconds
    '''

    minutes = seconds / 60
    remainder = seconds % 60

    if(remainder >= 30):
        minutes += 1

    return minutes * 60



