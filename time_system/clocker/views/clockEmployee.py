from django.views.decorators.http import require_POST
from django.http import HttpResponseNotFound, HttpResponseRedirect
from clocker.models import Employee


@require_POST
def clockEmployee(request):
    '''
    ' View that clocks an employee in or out depending on the value of "status"
    ' in the POST request.
    '
    ' Returns HttpResponseRedirect to the next view
    '''

    status = request.POST.get('status', None)
    if status is None:
        return HttpResponseNotFound()

    employee = request.user
    if status.lower() == "out" and employee.isClockedIn():
        shift = clockOutEmployee(employee)
        return HttpResponseRedirect('/timeclock/summary/%s/' % shift.id)
    elif status.lower() == "in" and not employee.isClockedIn():
        clockInEmployee(employee)
        return HttpResponseRedirect('/timeclock/')

    return HttpResponseNotFound()


def clockOutEmployee(employee):
    '''
    ' Clocks an employee out.
    '
    ' Returns: Shift used to clock employee out with.
    '''
    
    if not isinstance(employee, Employee):
        return HttpResponseNotFound()

    try:
        return employee.clock_out()
    except Exception as e:
        return HttpResponseNotFound(str(e))


def clockInEmployee(employee):
    '''
    ' Clocks an employee in.
    '
    ' Returns: Shift created to clock employee in with.
    '''

    if not isinstance(employee, Employee):
        return HttpResponseNotFound()
    
    try:
        return employee.clock_in()
    except Exception as e:
        return HttpResponseNotFound(str(e))

