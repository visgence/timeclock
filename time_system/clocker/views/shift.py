
# Django imports
from django.views.generic.base import View
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Local imports
from clocker.models import Shift

# System imports
try:
	import simplejson as json
except ImportError:
	import json


class ShiftView(View):

    pass

class ShiftsView(View):
	
    returnData = {
        "errors": []	
    }

    def get(self, request):

        shifts = Shift.objects.filter(employee=request.user).order_by( '-time_in', 'id')

        # break the data into pages 
        if 'page' in request.GET and 'per_page' in request.GET:
            paginator = Paginator(shifts, request.GET['per_page'])
            try:
                shifts = paginator.page(request.GET['page'])
            except pagenotaninteger:
                shifts = paginator.page(1)
            except emptypage:
                shifts = paginator.page(paginator.num_pages)

            self.returnData.update({
                 'shifts':     [s.toDict() for s in shifts]
                ,'totalPages': paginator.num_pages
                ,'page':       shifts.number
            })
        else:
            self.returnData['shifts'] = [s.toDict() for s in shifts]

        return HttpResponse(json.dumps(self.returnData, indent=4), content_type="application/json")
