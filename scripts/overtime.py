#!/usr/bin/python
#
# a toy program to test overtime computation algorithms
#
# mharris@visgence.com
#
from time import strptime

workdays = []

y = 2014
for m in range(1, 13):
    daysInMonth = 31

    # 30 days have september, april, june, and november
    if m == 9 or m == 4 or m == 6 or m == 11:
        daysInMonth = 30

    # all the rest have 31
    else:
        pass

    # except for February
    if m == 2:
        daysInMonth = 28

    for d in range(1, daysInMonth+1):
        # print "2014-%d-%d" % (m,d) #DEBUG
        t = strptime('%d-%d-%d' % (y, m, d), '%Y-%m-%d')
        workdays.append({
            'h': 8,
            't': t
        })

assert len(workdays) == 365  # working pretty hard this year...
print(workdays[0]['t'])

# regular hours - number of hours worked in a week up to 40
# overtime = number of hours worked above 40 from sunday to monday

overtime = 0
regular = 0

payPeriod_regular = 0
payPeriod_overtime = 0

for i in workdays:
    if i['t'].tm_mday == 1 or i['t'].tm_mday == 16:

        print("regular: %d" % (payPeriod_regular))
        print("overtime: %d" % (payPeriod_overtime))
        print("sub total: %d" % (payPeriod_regular + payPeriod_overtime))
        print("")
        regular += payPeriod_regular
        overtime += payPeriod_overtime
        payPeriod_regular = 0
        payPeriod_overtime = 0

    payPeriod_regular += i['h']
    payPeriod_overtime += 0

    # if ['t'].tm_wday <= 6:

total = 0
for i in workdays:
    total += i['h']

print("================")
print("regular: %d" % (regular))
print("overtime: %d" % (overtime))
print("total: %d" % (total))
print("discrepancy: %d" % (total - (regular+overtime)))
assert regular + overtime == total
