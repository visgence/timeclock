
# Django imports
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError

# Local imports
from clocker.models import Shift
from settings import DT_FORMAT

# System imports
try:
	import simplejson as json
except ImportError:
	import json

from datetime import datetime


class ShiftView(View):

    returnData = {
        "errors": []    
    }


    @staticmethod
    def updateClient(shift, jsonData, user):

        try:
            params = json.loads(jsonData)
            assert isinstance(params, dict), 'Request data not a dictionary.'
        except (ValueError, AssertionError) as e:
            error = 'Invalid data: ' + str(e)
            return HttpResponseBadRequest(json.dumps(error), content_type='application/json')

        #Set fields for shift
        for field, value in params.iteritems():
            if field in ['id', 'pk']:
                continue

            if field in ['time_in', 'time_out']:
                value = datetime.strptime(value, DT_FORMAT)

            setattr(shift, field, value)

        try:
            shift.full_clean()
        except ValidationError as e:
            errors = [{x: y} for x, y in e.message_dict.iteritems()]
            return HttpResponseBadRequest(json.dumps(errors), content_type='application/json')

        shift.save()
        success = {'shift': shift.toDict()}
        return HttpResponse(json.dumps(success, indent=4), content_type='applicatin/json')


    def put(self, request, shift_id):

        try:
            shift = Shift.objects.get(id=shift_id, employee=request.user)
        except Shift.DoesNotExist:
            error = 'Shift does not exist for id %s'%str(shift_id)
            return HttpResponseNotFound(json.dumps(error), content_type="application/json")

        return ShiftView.updateClient(shift, request.read(), request.user)

    

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

