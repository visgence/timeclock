#!/usr/bin/env python
import os
import re
import sys
import time
from datetime import datetime
import django

# local imports
from clocker.models import Shift, ShiftSummary

program_path = os.path.realpath(__file__)
APP_PATH = re.sub('settings.py[c]*$', '', program_path)
sys.path.append(os.path.join(APP_PATH, 'time_system'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()


def findMissing():
    month = 3600*24*31
    start = datetime.fromtimestamp(time.time()-month)
    shifts = Shift.objects.filter(time_in__gte=start).exclude(time_out=None)
    shiftsArr = []
    for s in shifts:
        if len(ShiftSummary.objects.filter(shift=s)) == 0:
            print(s)
            shiftsArr.append(s)
    return shiftsArr


if __name__ == "__main__":
    findMissing()
