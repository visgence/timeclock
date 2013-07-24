from django.views.decorators.http import require_POST
from django.http import HttpResponseNotFound


@require_POST
def clockEmployee(request):
    
    status = request.POST.get('status', None)
    if status is None:
        return HttpResponseNotFound()

    employee = request.user
    if status.lower() == "out" and not employee.isClockedIn():
        return clockOutEmployee(employee)
    elif status.lower() == "in" and employee.isClockedIn():
        return clockInEmployee(employee)

    return "something nasty"


def clockOutEmployee(employee):
    
    pass


def clockInEmployee(employee):

    employee.clock_in()
