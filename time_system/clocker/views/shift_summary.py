from django.http import HttpResponseRedirect, HttpResponse
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
        msg = "Error getting json data for shift summary"
        return HttpResponse(json.dumps({'error': msg}), content_type="application/json")
    
    try:
        employee = Employee.objects.get(id = jsonData['emp_id'])
    except Employee.DoesNotExist:
        msg = "Error getting employee while creating shift summary"
        return HttpResponse(json.dumps({'error': msg}), content_type="application/json")
    
    try:
        shift = Shift.objects.get(id = jsonData['shift_id'], employee=employee)
    except Shift.DoesNotExist:
        msg = "Error getting shift while creating shift summary for employee %s" % str(employee)
        return HttpResponse(json.dumps({'error': msg}), content_type="application/json")
    
    for summary in jsonData['shift_summary']:
        kwargs = {'employee': employee, 'shift': shift}
        kwargs['miles'] = summary['miles']
        kwargs['hours'] = summary['hours']
        kwargs['note'] = summary['notes']
        try:
            kwargs['job'] = Job.objects.get(id = summary['job_id'])
        except Job.DoesNotExist:
            msg = "Error getting job while creating shift summary for employee %s" % str(employee)
            return HttpResponse(json.dumps({'error': msg}), content_type="application/json")

        shift_summary = ShiftSummary(**kwargs)
        try:
            shift_summary.full_clean(exclude="note")
        except ValidationError as e:
            msg = "New shift summary didn't pass validation for employee %s: %s" % (str(employee), str(e))
            return HttpResponse(json.dumps({'error': msg}), content_type="application/json")

        shift_summary.save()
    
    return HttpResponseRedirect('/timeclock/')
    
