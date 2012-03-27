#!/usr/bin/python

from django.core.management import setup_environ
from clocker.models import *
import settings
setup_environ(settings)
from datetime import datetime, timedelta


def correct_record(record):

    if(record.time_out == None):
        end_time = datetime.now()
    else:
        end_time = record.time_out


    #If there is a difference in days then an employee was clocked in past midnight.  We only consider days and not months as that would be rediculous.
    #Insert new records starting from the time_in and ending at just before midnight and do this for everyday up until time_out
    if(end_time.day - record.time_in.day != 0):
        year = record.time_in.year
        month = record.time_in.month
        day = record.time_in.day
        hour = record.time_in.hour
        minute = record.time_in.minute

        #Insert the first day
        date_time = Time(employee = record.employee,
                         time_in = record.time_in,
                         time_out = datetime(year, month, day, 23, 59))
        date_time.save()

        i = 1
        #Insert the in-between dates
        while (day != end_time.day-1):
            new_date = record.time_in + timedelta(i)
            month = new_date.month
            day = new_date.day
            date_time = Time(employee = record.employee,
                             time_in = datetime(year, month, day, 00, 00),
                             time_out = datetime(year, month, day, 23, 59))
            date_time.save()
            i += 1

            #Insert the last day
            month = end_time.month
            day = end_time.day
            date_time = Time(employee = record.employee,
                             time_in = datetime(year, month, day, 00, 00),
                             time_out = end_time)
            date_time.save()

        record.delete()


def main():

    for record in Time.objects.all():
        correct_record(record)



if __name__ == "__main__":
    main()
