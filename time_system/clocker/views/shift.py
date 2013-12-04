
# Django imports
from django.views.generic.base import View
from django.http import HttpResponse

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

		shifts = Shift.objects.filter(employee=request.user).order_by('-time_in')
		self.returnData['shifts'] = [s.toDict() for s in shifts]
		return HttpResponse(json.dumps(self.returnData, indent=4), content_type="application/json")
