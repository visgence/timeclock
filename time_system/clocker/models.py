from django.db import models
from django.contrib.auth import models as auth_models
from datetime import datetime
from decimal import Decimal


class Employee(models.Model):
    user = models.ForeignKey(auth_models.User, unique=True)
    hire_date = models.DateField('date employee was hired')
    has_salary = models.BooleanField()
    hourly_rate = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank=True)
    salary = models.DecimalField(max_digits = 8, decimal_places = 2, null = True, blank=True)

    class Meta:
        db_table = 'Employee'

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

    def clock_in(self):
        """
        Clocks an employee in.  
        
        Returns: 
            The error message "none" if the user clocked in and "in" if the user was not able to clock in
        """

        dictionary = self.which_clock()

        #Employee has never clocked in before or has previously clocked out
        if(dictionary['status'] == "in"):
            return "in"
        else:
            time = Shift(employee=self,
                        time_in=datetime.now())
            time.save()
            return "none"

    def clock_out(self):
        """
        Clocks an employee out.  
        
        Returns: 
            The error message "none" if the user clocked out and "out" if the user was not able to clock out.
        """
        
        dictionary = self.which_clock()

        #Employee has never clocked out before or has not clocked in yet.
        if(dictionary['status'] == "out"):
            return "out"
        else:
            time = Shift(id=dictionary['max_record'].id,
                        employee=dictionary['max_record'].employee,
                        time_in=dictionary['max_record'].time_in,
                        time_out=datetime.now())
            time.save()
            return "none"

    def which_clock(self):
        """
        Checks to see whether an employee is clocked in or out. 

        Returns:
            A dictionary with the status of the employee and the maximum time record that was used to determine this.
            Keys: 'status' 'max_record'
        TODO: It is possible for an admin to never be clocked into our time system. 
        """

        max_id = Shift.objects.filter(employee=self).aggregate(employee=models.Max('id'))

        #print "max: %s" %  max_id #DEBUG

        if(max_id['employee'] == None):
            stuff = {'status':"out", 'max_record':None}
            return stuff

        record = Shift.objects.get(id=max_id['employee'])
        stuff = {
                    'max_record':record
                }

        if(record == None or record.time_out != None):
            stuff['status'] = "out"
            return stuff 
       
        stuff['status'] = "in"
        return stuff 

    def get_current_time(self):

        dictionary = self.which_clock()

        if(dictionary['status'] == "in"):
            time_in = dictionary['max_record'].time_in
            time_now = datetime.now()


class Shift(models.Model):
    employee = models.ForeignKey('Employee')
    time_in = models.DateTimeField('clock in time')
    time_out = models.DateTimeField('clock out time', null = True, blank=True)
    hours = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=4)

    class Meta:
        db_table = 'Shift'
        ordering = ['time_in', 'employee']

    def __unicode__(self):
        data = "TIME_IN: " + self.time_in.strftime("%Y-%m-%d %H:%M") + " TIME_OUT: "
        if(self.time_out != None):
            data += self.time_out.strftime("%Y-%m-%d %H:%M") + " " + self.employee.user.first_name + " " + self.employee.user.last_name
        else:
            data += " " + self.employee.user.first_name + " " + self.employee.user.last_name

        return data

    def save(self, *args, **kwargs):

        if self.time_out is not None:
            diff = self.time_out - self.time_in
            hours = Decimal(diff.total_seconds()/3600).quantize(Decimal('1.00'))
            self.hours = hours
        super(Shift, self).save(*args, **kwargs)



class ShiftSummary(models.Model):
    job = models.ForeignKey('Job')
    employee = models.ForeignKey('Employee')
    shift = models.ForeignKey('Shift')
    hours = models.IntegerField('total hours')
    miles = models.DecimalField(max_digits = 6, decimal_places = 2, null = True, blank=True)
    note = models.TextField('notes about job')

    class Meta:
        db_table = 'Shift Summary'
        ordering = ['shift', 'employee', 'job']

    def __unicode__(self):
        data = self.shift.time_in.date().strftime("%Y-%m-%d") + "    EMPLOYEE: " + self.employee.user.first_name + "  " + self.employee.user.last_name + "    JOB: " + self.job.name
        return data


class Job(models.Model):
    name = models.CharField('job name', max_length = 25)
    description = models.TextField('job description')
    is_active = models.BooleanField() 

    class Meta:
        db_table = 'Job'
        ordering = ['-is_active']

    def __unicode__(self):
        return self.name
