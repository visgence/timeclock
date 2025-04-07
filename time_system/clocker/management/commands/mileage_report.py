from django.core.management.base import BaseCommand
from clocker.models import Employee
from clocker.models import Shift
from clocker.models import ShiftSummary
from delorean import Delorean
import datetime
from time import gmtime, strftime
import json
from copy import copy
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--start',
            default=False,
            help='Start date. YYYY-MM-DD',
        )
        parser.add_argument(
            '--end',
            default=False,
            help='End date. YYYY-MM-DD',
        )
        parser.add_argument(
            '--timezone',
            default=False,
            help='Timezone to use, defaults to your location',
        )
        parser.add_argument(
            '--rate',
            default=False,
            help='Optional rate, displays miles * rate for each employee',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Displays all employees regardless of milage count.',
        )

    def handle(self, *args, **options):

        if options['start'] is False:
            logger.info("Start required. Use --start=123")
            return
        if options['end'] is False:
            logger.info("End required. Use --end=123")
            return

        startArr = options['start'].split('-')
        endArr = options['end'].split('-')
        startDate = datetime.datetime(int(startArr[0]), int(startArr[1]), int(startArr[2]))
        endDate = datetime.datetime(int(endArr[0]), int(endArr[1]), int(endArr[2]))
        endDate += datetime.timedelta(0, 86399)
        timezone = strftime("%Z", gmtime())
        if options['timezone']:
            timezone = options['timezone']

        start = "{}".format(Delorean(datetime=startDate, timezone=timezone).naive)
        end = "{}".format(Delorean(datetime=endDate, timezone=timezone).naive)

        employees = {}
        for i in Employee.objects.all():
            employees[i.id] = {'name': str(i), 'miles': 0.0}
            if options['rate']:
                employees[i.id]['reimbursement_amount'] = 0.0
        for shift in Shift.objects.filter(time_in__gte=start).filter(time_out__lte=end):
            for shift_summary in ShiftSummary.objects.filter(shift=shift):
                employees[shift_summary.shift.employee.id]['miles'] += float(shift_summary.miles)
                if options['rate']:
                    employees[shift_summary.shift.employee.id]['reimbursement_amount'] += float(options['rate'])*float(shift_summary.miles)
        if not options['all']:
            tempObj = copy(employees)
            for key, value in employees.items():
                if value['miles'] == 0:
                    tempObj.pop(key)
            employees = tempObj
        logger.info(json.dumps(employees, indent=4))
