from django.views.decorators.http import require_POST
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError
from django.core.exceptions import ValidationError
from django.db import transaction
from clocker.models import Employee, Shift, ShiftSummary, Job
from settings import ENABLE_JOBS


@require_POST
def clockEmployee(request):
    """
    ' View that clocks an employee in or out depending on the value of "status" in the POST request.
    '
    ' Returns HttpResponseRedirect to the next view
    """

    status = request.POST.get('status', None)
    if status is None:
        return HttpResponseNotFound()

    employee = request.user
    if status.lower() == "out" and employee.isClockedIn():
        shift = clockOutEmployee(employee)
        if not isinstance(shift, Shift):
            return shift

        return HttpResponseRedirect('/timeclock/summary/%s/' % shift.id)
    elif status.lower() == "in" and not employee.isClockedIn():
        clockInEmployee(employee)
        return HttpResponseRedirect('/timeclock/')

    return HttpResponseNotFound()


def clockOutEmployee(employee):
    """
    ' Clocks an employee out.
    '
    ' Returns: Shift used to clock employee out with.
    """

    if not isinstance(employee, Employee):
        return HttpResponseNotFound()

    try:
        if ENABLE_JOBS:
            return employee.clock_out()

        shift = employee.clock_out()
        kwargs = {'employee': shift.employee, 'shift': shift, 'hours': int(shift.hours * 60 * 60)}
        kwargs['miles'] = 0.00
        kwargs['note'] = 'default job'
        kwargs['job'] = Job.objects.get(id=1)
        shift_summary = ShiftSummary(**kwargs)
        try:
            shift_summary.full_clean()
        except ValidationError as e:
            print(e)
            transaction.rollback()
            msg = "New shift summary didn't pass validation for employee %s: %s" % (str(employee), str(e))
            return HttpResponseServerError(msg)
        shift_summary.save()
        transaction.commit()
        return shift
    except Exception as e:
        print(e)
        return HttpResponseNotFound(str(e))


def clockInEmployee(employee):
    """
    ' Clocks an employee in.
    '
    ' Returns: Shift created to clock employee in with.
    """

    if not isinstance(employee, Employee):
        return HttpResponseNotFound()

    try:
        return employee.clock_in()
    except Exception as e:
        return HttpResponseNotFound(str(e))
