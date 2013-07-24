from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
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
    
