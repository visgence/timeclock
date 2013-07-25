#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.core.exceptions import ValidationError
from clocker.models import ShiftSummary



def main():

    for s in ShiftSummary.objects.all():
        try:
            s.full_clean()
        except ValidationError as e:
            print "*******************   ERROR  *********************"
            print '; '.join(e.messages) + ' for owner %s' % str(s.employee)
            print "Id = %s;  Job Id = %s;  Shift Id = %s" % (s.id, s.job.id, s.shift.id)
            print
            print

if __name__ == "__main__":
    main()
