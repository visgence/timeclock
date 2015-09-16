from django.core.management.base import BaseCommand, CommandError
from clocker.models import Employee
from clocker.models import Shift
from clocker.models import ShiftSummary
import datetime

import json

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if len(args) < 2:
            print "start and end required"
            return

        # TODO: do we need to be timezone-aware?
        start = datetime.datetime.fromtimestamp(int(args[0]))
        end = datetime.datetime.fromtimestamp(int(args[1]))
    
        employees = {}
        for i in Employee.objects.all():
            employees[i.id] = {'name': str(i),
                               'miles': 0.0
                               }
        #print employees
        for shift in Shift.objects.filter(time_in__gte=start).filter(time_out__lte=end):
            for shift_summary in ShiftSummary.objects.filter(shift=shift):
                employees[shift_summary.shift.employee.id]['miles'] += float(shift_summary.miles)

        print json.dumps(employees, indent=4)

