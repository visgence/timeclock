from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from clocker.models import ShiftSummary, Shift, Employee, Job

try:
    import simplejson as json
except ImportError:
    import json


@require_POST
def summary(request):

    try:
        jsonData = json.loads(request.POST['jsonData'])
    except Exception:
        return HttpResponseServerError("Error getting json data for shift summary")
    
    try:
        employee = Employee.objects.get(id = jsonData['emp_id'])
    except Employee.DoesNotExist:
        return HttpResponseServerError("Error getting employee while creating shift summary")
    
    try:
        shift = Shift.objects.get(id = jsonData['shift_id'], employee=employee)
    except Shift.DoesNotExist:
        return HttpResponseServerError("Error getting shift while creating shift summary for employee %s" % str(employee))
    
    for summary in jsonData['shift_summary']:
        kwargs = {'employee': employee, 'shift': shift}
        kwargs['miles'] = summary['miles']
        kwargs['hours'] = summary['hours']
        kwargs['note'] = summary['notes']
        try:
            kwargs['job'] = Job.objects.get(id = summary['job_id'])
        except Job.DoesNotExist: 
            return HttpResponseServerError("Error getting job while creating shift summary for employee %s" % str(employee))

        shift_summary = ShiftSummary(**kwargs)
        try:
            shift_summary.full_clean(exclude="note")
        except ValidationError as e: 
            msg = "New shift summary didn't pass validation for employee %s: %s" % (str(employee), str(e))
            return HttpResponseServerError(msg)

        shift_summary.save()
    
    return HttpResponseRedirect('/timeclock/')
   

def renderSummary(request, id):

    employee = request.user

    try:
        shift = Shift.objects.get(id=id, employee=employee)
    except Shift.DoesNotExist:
        return HttpResponseServerError('Shift does not exist for id %s' % str(id))
    
    #Only complete shifts can have summaries
    if shift.time_out == None:
        return HttpResponseServerError('You cannot complete any summaries for a shift where you are not clocked out yet.')

    #We only care about tracking time that's at least one minute
    timeDiff = shift.time_out - shift.time_in
    totalTime = roundSeconds(timeDiff.total_seconds())
    if totalTime < 60:
        totalTime = 0

    jobs = Job.objects.filter(is_active=True)

    t = loader.get_template('shiftSummary.html')
    c = RequestContext(request, {
        'totalTime': totalTime,
        'jobs': jobs,
        'shift': shift
    })
    return HttpResponse(t.render(c), content_type="text/html")


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



