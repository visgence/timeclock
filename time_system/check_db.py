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
from datetime import datetime, timedelta


def correct_record(record):
    """
    Takes a time record from the database and checks it for errors in the clock in and clock out times.
    If it spots an employee that stayed clocked in past midnight then it will delete that record
    and inserts time records that have the employee clocked out before midnight each day and clocked in right after midnight the next day.
    It will recognize that an employee is still clocked in and simply make the last inserted record not have a clock out time so that the employee can do so.
    """

    if(record.time_out is None):
        end_time = datetime.now()
        shift_summary = None
    else:
        end_time = record.time_out
        try:
            shift_summary = ShiftSummary.objects.get(shift_id=record.id)
        except ObjectDoesNotExist:
            shift_summary = None

    # If there is a difference in days then an employee was clocked in past midnight.  We only consider days and not months as that would be rediculous.
    # Insert new records starting from the time_in and ending at just before midnight and do this for everyday up until time_out
    if(end_time.day - record.time_in.day != 0):
        year = record.time_in.year
        month = record.time_in.month
        day = record.time_in.day
        # hour = record.time_in.hour
        # minute = record.time_in.minute

        # Insert the first day
        date_time = Shift(
            employee=record.employee,
            time_in=record.time_in,
            time_out=datetime(year, month, day, 23, 59)
        )
        date_time.save()
        if shift_summary is not None:
            time_difference: timedelta = datetime(year, month, day, 23, 59) - record.time_in
            seconds_difference: float = time_difference.total_seconds()
            new_summary = ShiftSummary(hours=seconds_difference, miles=shift_summary.miles, note=shift_summary.note,
                                employee_id=shift_summary.employee_id, job_id=shift_summary.job_id, shift_id=date_time.id)
            new_summary.save()

        i = 1
        # Insert the in-between dates
        while (day != (end_time - timedelta(1)).day):
            new_date = record.time_in + timedelta(i)
            month = new_date.month
            day = new_date.day
            date_time = Shift(
                employee=record.employee,
                time_in=datetime(year, month, day, 00, 00),
                time_out=datetime(year, month, day, 23, 59)
            )
            date_time.save()
            if shift_summary is not None:
                new_summary = ShiftSummary(hours=86400, miles=shift_summary.miles, note=shift_summary.note,
                                    employee_id=shift_summary.employee_id, job_id=shift_summary.job_id, shift_id=date_time.id)
                new_summary.save()
            i += 1

        # Insert the last day and make sure to keep the employee clocked in if they were when this started.
        end_year = end_time.year
        end_month = end_time.month
        end_day = end_time.day
        if(record.time_out is None):
            date_time = Shift(
                employee=record.employee,
                time_in=datetime(end_year, end_month, end_day, 00, 00),
                time_out=None)
        else:
            date_time = Shift(
                employee=record.employee,
                time_in=datetime(end_year, end_month, end_day, 00, 00),
                time_out=end_time
            )
        date_time.save()
        if shift_summary is not None:
            time_difference: timedelta = end_time - datetime(end_year, end_month, end_day, 00, 00)
            seconds_difference: float = time_difference.total_seconds()
            new_summary = ShiftSummary(hours=seconds_difference, miles=shift_summary.miles, note=shift_summary.note,
                                employee_id=shift_summary.employee_id, job_id=shift_summary.job_id, shift_id=date_time.id)
            new_summary.save()
            shift_summary.delete()

        record.delete()


def main():

    for record in Shift.objects.all():
        correct_record(record)


if __name__ == "__main__":
    main()
