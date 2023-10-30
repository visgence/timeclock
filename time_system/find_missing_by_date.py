#!/usr/bin/env python
import os
import re
import sys
import django

# local imports
from clocker.models import Shift, ShiftSummary

program_path = os.path.realpath(__file__)
APP_PATH = re.sub('settings.py[c]*$', '', program_path)
sys.path.append(os.path.join(APP_PATH, 'time_system'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()


def findMissingByDate(start, end):
    """Find shifts missing summary"""
    shifts = Shift.objects.filter(time_in__gte=start, time_in__lte=end).exclude(time_out=None) #, time_in__lte=end
    shifts_arr = []
    for shift in shifts:
        if len(ShiftSummary.objects.filter(shift=shift)) == 0:
            shifts_arr.append(shift)
    return shifts_arr
