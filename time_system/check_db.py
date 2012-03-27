#!/usr/bin/python

from django.core.management import setup_environ
from clocker.models import *
import settings
setup_environ(settings)
import datetime

def main():

    for record in Time.objects.all():

        if (record.time_out == None):
            print "clock out kumquat!!"

        else:

            #If there is a difference in days then an employee was clocked in past midnight.  We only consider days and not months as that would be rediculous.
            #In a list [time_in, in-between datetime objects, time_out] which will allow to iterate through and clock the employee in and out on each respective day.
            if(record.time_out.day - record.time_in.day != 0):
                year = record.time_in.year
                month = record.time_in.month
                day = record.time_in.day
                hour = record.time_in.hour
                minute = record.time_in.minute
                date_time = Time(employee = record.employee,
                                 time_in = record.time_in,
                                 time_out = datetime(
                day = record.time_in.day
                i = 1

                #Get the in-between datetimes
                while (day != record.time_out.day-1):
                    dates.append(record.time_in + datetime.timedelta(i))
                    day = dates[i].day
                    i += 1
                dates.append(record.time_out)

                record.delete()


if __name__ == "__main__":
    main()
