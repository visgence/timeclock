from django.template import RequestContext, loader
from django.http import HttpResponse
from clocker.models import Employee


def mainPage(request):
    
    employee = request.user
    employees = [employee]
    if employee.is_superuser:
        employees = Employee.objects.filter(is_active=True)

    status = employee.isClockedIn()
    recentShift = employee.getCurrentShift()
    timeStamp = recentShift.time_in
    message = "You are clock in. You clocked in at " 
    if not status:
        message = "You are clocked out. You last clocked out at "
        timeStamp = recentShift.time_out
    
    t = loader.get_template('main_page.html')
    c = RequestContext(request, {
        'employee': employee,
        'employees': employees,
        'status': status,
        'message': message,
        'timeStamp': timeStamp
    })

    return HttpResponse(t.render(c), content_type="text/html")
