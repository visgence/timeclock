
# Django imports
from django.views.generic.base import View
from django.http import HttpResponse

# Local imports
from clocker.models import Employee

# System imports
try:
    import simplejson as json
except ImportError:
    import json


class EmployeeView(View):

    returnData = {
        "errors": []
    }

    # Place holder view until we need it


class EmployeesView(View):

    returnData = {
        "errors": []
    }

    def get(self, request):

        employees = Employee.objects.get_editable(request.user)
        self.returnData['employees'] = [e.toDict() for e in employees]

        return HttpResponse(json.dumps(self.returnData, indent=4), content_type="application/json")
