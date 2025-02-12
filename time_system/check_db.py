#!/usr/bin/python
import os
import re
import sys
import django
from django.core.exceptions import ObjectDoesNotExist
program_path = os.path.realpath(__file__)
APP_PATH = re.sub('settings.py[c]*$', '', program_path)
sys.path.append(os.path.join(APP_PATH, 'time_system'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from clocker.models import Shift, ShiftSummary
from datetime import datetime
from settings import ENABLE_JOBS


def correct_record(record):
    """
    Takes a time record from the database and checks it for errors in the clock in and clock out times.
    If it spots an employee that stayed clocked in past midnight then it will sign them out and delete any related summary.
    """

    if(record.time_out is None):
        end_time = datetime.now()
    else:
        end_time = record.time_out

    # If there is a difference in days then an employee was clocked in past midnight.
    if(end_time.day - record.time_in.day != 0):
        year = record.time_in.year
        month = record.time_in.month
        day = record.time_in.day
        record.time_out=datetime(year, month, day, 23, 59)
        record.save()

        if ENABLE_JOBS:
            try:
                shift_summaries = ShiftSummary.objects.filter(shift_id=record.id)
                shift_summaries.delete()
            except ObjectDoesNotExist:
                pass

def main():

    for record in Shift.objects.all():
        correct_record(record)


if __name__ == "__main__":
    main()
