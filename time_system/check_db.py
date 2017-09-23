#!/usr/bin/python

from clocker.models import Shift
from datetime import datetime, timedelta


def correct_record(record):
    """
    Takes a time record from the database and checks it for errors in the clock in and clock out times.
    If it spots an employee that stayed clocked in past midnight then it will delete that record
    and inserts time records that have the employee clocked out before midnight each day and clocked in right after midnight the next day.  It will recognize that an employee is still clocked in and
    simply make the last inserted record not have a clock out time so that the employee can do so.
    """

    if(record.time_out is None):
        end_time = datetime.now()
    else:
        end_time = record.time_out

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

        record.delete()


def main():

    for record in Shift.objects.all():
        correct_record(record)


if __name__ == "__main__":
    main()
