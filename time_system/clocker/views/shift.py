
# Django imports
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

# Local imports
from clocker.models import Shift, Employee
from settings import DT_FORMAT
import logging
logger = logging.getLogger(__name__)

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

        # Set fields for shift
        for field, value in params.items():
            if field in ['id', 'pk', 'employee']:
                continue

            if field in ['time_in', 'time_out'] and value is not None:
                if value == '':
                    value = None
                else:
                    value = datetime.strptime(value, DT_FORMAT)

            setattr(shift, field, value)

        try:
            shift.full_clean()
        except ValidationError as e:
            errors = [{x: y} for x, y in e.message_dict.items()]
            return HttpResponseBadRequest(json.dumps(errors), content_type='application/json')

        shift.save()
        success = {'shift': shift.toDict()}
        return HttpResponse(json.dumps(success, indent=4), content_type='applicatin/json')

    def put(self, request, shift_id):

        try:
            shift = Shift.objects.get(id=shift_id)
        except Shift.DoesNotExist:
            error = 'Shift does not exist for id %s' % str(shift_id)
            return HttpResponseNotFound(json.dumps(error), content_type="application/json")
        else:
            if not shift.can_edit(request.user):
                error = 'You do not have permission to edit this Shift'
                return HttpResponseForbidden(json.dumps(error), content_type="application/json")

        return ShiftView.updateClient(shift, request.read(), request.user)

    def delete(self, request, shift_id):

        try:
            shift = Shift.objects.get(id=shift_id)
        except Shift.DoesNotExist:
            error = 'Shift does not exist for id %s' % str(shift_id)
            return HttpResponseNotFound(json.dumps(error), content_type="application/json")
        else:
            if not shift.can_edit(request.user):
                error = 'You do not have permission to delete this Shift'
                return HttpResponseForbidden(json.dumps(error), content_type="application/json")

        shift.deleted = True

        try:
            shift.full_clean()
        except ValidationError as e:
            errors = [{x: y} for x, y in e.message_dict.items()]
            return HttpResponseBadRequest(json.dumps(errors), content_type='application/json')

        shift.save()
        self.returnData['success'] = "Shift %s successfully deleted." % str(shift_id)
        return HttpResponse(json.dumps(self.returnData, indent=4), content_type="application/json")


class ShiftsView(View):

    returnData = {
        "errors": []
    }

    def get(self, request):

        employee = request.user
        if 'employee' in request.GET:
            emp_id = request.GET['employee']
            try:
                employee = Employee.objects.get(id=emp_id)
            except Employee.DoesNotExist:
                self.returnData['errors'].append('Employee with id %s does not exist' % str(emp_id))
                return HttpResponseNotFound(json.dumps(self.returnData, indent=4), content_type="application/json")

        if not request.user.is_superuser and request.user != employee:
            self.returnData['errors'].append('Invalid permissions')
            return HttpResponseForbidden(json.dumps(self.returnData, indent=4), content_type="application/json")

        if('first_shift' in request.GET) :
            first_shift = Shift.objects.filter(employee=employee).order_by('time_in')[0]



        if 'starting_timestamp' in request.GET and 'ending_timestamp' in request.GET:
            try:
                first_shift = Shift.objects.filter(employee=employee).order_by('time_in')[0]
            except Exception:
                self.returnData.update({
                    'shifts': [],
                    'first_shift': str(datetime.now())
                })
            else:
                starting_date = datetime.fromtimestamp(int(request.GET['starting_timestamp'])).strftime('%Y-%m-%d %H:%S')
                ending_date = datetime.fromtimestamp(int(request.GET['ending_timestamp'])).strftime('%Y-%m-%d %H:%S')
                shifts = Shift.objects.filter(employee=employee, time_in__range=[starting_date, ending_date]).order_by('-time_in')
                self.returnData.update({
                    'shifts': [s.toDict() for s in shifts],
                    'first_shift' : first_shift.toDict()['time_in']
                
                })

        # break the data into pages
        elif 'page' in request.GET and 'per_page' in request.GET:
            shifts = Shift.objects.filter(employee=employee).order_by('-time_in', 'id')
            paginator = Paginator(shifts, request.GET['per_page'])
            try:
                shifts = paginator.page(request.GET['page'])
            except Exception as pagenotaninteger:
                logger.debug(pagenotaninteger)
                shifts = paginator.page(1)
            except Exception as emptypage:
                logger.debug(emptypage)
                shifts = paginator.page(paginator.num_pages)

            self.returnData.update({
                'shifts':     [s.toDict() for s in shifts],
                'totalPages': paginator.num_pages,
                'page':       shifts.number
            })
        else:
            self.returnData['shifts'] = [s.toDict() for s in shifts]

        return HttpResponse(json.dumps(self.returnData, indent=4), content_type="application/json")
