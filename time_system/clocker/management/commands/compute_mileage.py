# compute mileage, this stuff is just the output of an iPython session and needs to be made into a proper command
import logging
logger = logging.getLogger(__name__)

s = Shift.object.all()
s = Shift.objects.all()
s = Shift.objects.all()[0]
s.time_out
s.time_in
s.time_out
s = Shift.objects.all()[-10]
s = Shift.objects.all()[10]
s.time_out
import datetime
datetime.datetime(2015, 7, 16, 0, 0, 0, 0)
start = datetime.datetime(2015, 7, 16, 0, 0, 0, 0)
end = datetime.datetime(2015, 7, 31, 23, 59, 59, 0)
end
ShiftSummary.objects.filter(shift__time_out__gte=start)
summaries = ShiftSummary.objects.filter(shift__time_out__gte=start)
summaries.filter(shift__time_out__lte=end)
summaries = summaries.filter(shift__time_out__lte=end)
summaries[0].shift
summaries[0].shift.employee
summaries[0].miles
for i in summaries:
    logger.info(i.miles)

total_miles = 0
for i in summaries:
    total_miles+=i.miles

total_miles
get_ipython().magic(u'save mileage_calc')
get_ipython().magic(u'save mileage_calc 0-27')

