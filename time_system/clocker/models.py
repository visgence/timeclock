
# Django imports
from django.db import models
from django.db import transaction         
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

# System Imports
from datetime import datetime
from decimal import Decimal
import re

# Local imports
from chucho.models import ChuchoManager
from hashMethods import hash64
from settings import DT_FORMAT



class EmployeeManager(BaseUserManager, ChuchoManager):
    def can_edit(self, user):
        '''
        ' Checks if a User is allowed to edit or add instances of this model.
        '
        ' Keyword Arguments:
        '   user - User to check permission for.
        '
        ' Return: True if user is allowed to edit objects of this model and False otherwise.
        '''

        #Validate user object
        if not isinstance(user, Employee):
            raise TypeError("%s is not an auth user" % str(user))

        if user.is_superuser:
            return True

        return False

    def get_viewable(self, user, filter_args=None, omni=None):
        '''
        ' Gets all Employees that can be viewed or assigned by a specific AuthUser.
        '
        ' Keyword Arguments:
        '   user - User to filter viewable Employees by.
        '
        ' Return: QuerySet of Employees that can be viewed by specified user.
        '''
        # TODO: Wrapper until we decide to differentiate this from editable.
        return self.get_editable(user, filter_args, omni)

    def get_editable(self, user, filter_args=None, omni=None):
        ''' 
        ' Gets all the users that can be edited by a specified user.
        '
        ' Right now only superusers can edit.
        '
        ' Keyword Arguments:
        '   user - User to filter editable employees by.
        '
        ' Return: QuerySet of Employees that are viewable by the specified User.
        '''
        if not isinstance(user, Employee):
            raise TypeError("%s is not an Auth User" % str(user))

        if filter_args is not None and len(filter_args) > 0:
            objs = self.advanced_search(**filter_args)
        elif omni is not None:
            objs = self.search(omni)
        else:
            objs = self.all()
        if user.is_superuser:
            return objs

        return objs.filter(username=user.username)

    def get_editable_by_pk(self, user, pk):
        '''
        ' Get's an instance of Employee specified by a pk if the given user is allowed to edit it.
        '
        ' Keyword Arguments: 
        '   user - User to check if the employee can be edited by them.
        '   pk   - Primary key of Employee to get.
        '
        ' Return: Employee identified by pk if user can edit it, otherwise None.
        '''
        
        if not isinstance(user, Employee):
            raise TypeError('%s is not an Auth User' % str(user))

        try:
            u = self.get(id=pk)
        except Employee.DoesNotExist:
            raise Employee.DoesNotExist("An Employee does not exist for the primary key %s." % str(pk))

        if user.is_superuser:
            return u
        return None

    def search(self, search_str, operator=None, column=None):
        '''Overwrite chucho default search for user.'''
        # Regexes to trigger different kinds of searches.
        pattern_name1 = r'^\s*(.+)\s+(.+)\s*$'
        pattern_name2 = r'^\s*(.+),\s*(.+)\s*$'
        pattern_username = r'^\s*(.+)\s*$'
        
        q_list = []
        m = re.match(pattern_name1, search_str, re.I)
        if m is not None:
            q_list.append(Q(first_name__icontains=m.group(1), last_name__icontains=m.group(2)))

        m = re.match(pattern_name2, search_str, re.I)
        if m is not None:
            q_list.append(Q(first_name__icontains=m.group(2), last_name__icontains=m.group(1)))

        m = re.match(pattern_username, search_str, re.I)
        if m is not None:
            q_list.append(Q(username__icontains=m.group(1)))
            q_list.append(Q(first_name__icontains=m.group(1)))
            q_list.append(Q(last_name__icontains=m.group(1)))

        q_all = None
        for q in q_list:
            if q_all is None:
                q_all = q
            else:
                q_all |= q

        if q_all is None:
            return self.none()
        else:
            return self.filter(q_all)


class Employee(AbstractBaseUser):
    hire_date = models.DateField('date employee was hired')
    has_salary = models.BooleanField()
    hourly_rate = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank=True)
    salary = models.DecimalField(max_digits = 8, decimal_places = 2, null = True, blank=True)
    username = models.TextField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.now())
    color = models.CharField(max_length=32, blank=True)
    objects = EmployeeManager()

    USERNAME_FIELD = "username"

    column_options = {
        'id': {'grid_column': False},
        'password': {'_type': 'password', 'grid_column': False},
        'date_joined': {'grid_column': False},
        'last_login': {'grid_column': False, '_editable': False}
        }

    search_fields = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.username = self.username.strip()
        super(Employee, self).save(*args, **kwargs)


    def toDict(self):
        return {
             "id":           self.id
            ,"username":     self.username
            ,"first_name":   self.first_name
            ,"last_name":    self.last_name
            ,"is_superuser": self.is_superuser
            ,"is_active":    self.is_active
        }

    def can_view(self, user):
        '''
        ' Checks if a User instance is allowed to view this object instance or not.
        '
        ' Keyword Arguments:
        '   user - AuthUser to check if they have permissions.
        '
        ' Return: True if user is allowed to view and False otherwise.
        '''

        if not isinstance(user, Employee):
            raise TypeError('%s is not an auth user' % str(user))

        if user.is_superuser or user == self:
            return True

        return False


    def clock_in(self):
        '''
        ' Clocks an employee in.  
        ' 
        ' Returns: The newly saved shift if clocked in successfully.
        '''
      
        assert not self.isClockedIn(), "Error clocking Employee in. Employee is already clocked in."

        shift = Shift(employee=self, time_in=datetime.now())
        try:
            shift.full_clean()
            shift.save()
        except ValidationError as e:
            msg = "An error occured while clocking you in. %s" % str(e)
            raise ValidationError(msg)
        
        return shift
        

    def clock_out(self):
        '''
        ' Clocks an employee out.  
        ' 
        ' Returns: The shift used to clock the employee out with.
        '''
      
        shift = self.getCurrentShift()
        now = datetime.now()
        assert self.isClockedIn(), "Error clocking Employee out. Employee is already clocked out"
        assert shift is not None, "Error clocking Employee out. Employee has never clocked in before."
        assert now >= shift.time_in, "Error clocking Employee out. It appears you are clocked in into the future."
        
        shift.time_out = datetime.now()
        try:
            shift.full_clean()
            shift.save()
        except ValidationError as e:
            msg = "An error occured while clocking you out. %s" % str(e)
            raise ValidationError(msg)
        
        return shift
       

    def getCurrentShift(self):
        '''
        ' Gets the most recent Shift record for an employee clocked in or out.
        '
        ' Returns: Shift object or None if Employee does not have any Shift records
        '''

        try:
            return Shift.objects.get(employee=self, time_out=None)
        except Shift.DoesNotExist:
            pass
        except Shift.MultipleObjectsReturned:
            msg = "It appears you have multiple shifts that say your clocked in.  Please use the Manage Shifts tool to fix this."
            raise Shift.MultipleObjectsReturned(msg)

        try:
            return Shift.objects.filter(employee=self).latest('time_out')
        except Shift.DoesNotExist:
            return None

 
    def isClockedIn(self):
        '''
        ' Check if a user is clocked in or out.
        ' 
        ' Returns: True if clocked in and False otherwise
        '''
        
        try:
            Shift.objects.get(employee=self, time_out=None)
            return True
        except Shift.DoesNotExist:
            return False
        except Shift.MultipleObjectsReturned:
            msg = "It appears you have multiple shifts that say your clocked in.  Please use the Manage Shifts tool to fix this."
            raise Shift.MultipleObjectsReturned(msg)

    
    def getJobHours(self, start, end, job):
        '''
        ' Calculates and returns the total hours worked by the employee for the given job in the timerange
        '
        ' Keyword Args:
        '   start - Datetime object specifying start of time range
        '   end   - Datetime object specifying end of time range
        '   job   - Job to total up hours worked for.
        '
        ' Returns: total hours worked on the job for the time range as a float.
        '''
        
        assert isinstance(job, Job), "%s is not a Job instance"%str(job)

        summaries = ShiftSummary.objects.filter(shift__deleted=False, employee=self, job=job, shift__time_in__lte=end, shift__time_out__gte=start)
        hours = 0.0
        for summary in summaries:
            hours += summary.hours/3600.0

        return hours


class ShiftManager(ChuchoManager):

    def get_query_set(self):
        return super(ShiftManager, self).get_query_set().filter(deleted=False)


    def get_editable_by_pk(self, user, pk):
        '''
        ' Get's an instance of Shift specified by a pk if the given user is allowed to edit it.
        '
        ' Keyword Arguments: 
        '   user - User to check if the user can be edited by them.
        '   pk   - Primary key of Shift to get.
        '
        ' Return: Shift identified by pk if user can edit it, otherwise None.
        '''
        
        if not isinstance(user, Employee):
            raise TypeError('%s is not an Auth User' % str(user))

        try:
            u = self.get(id=pk)
        except Shift.DoesNotExist:
            raise Shift.DoesNotExist("A Shift does not exist for the primary key %s." % str(pk))

        if user.is_superuser or u.employee == user:
            return u
        return None

    def can_edit(self, user):
        '''
        ' Checks if a User is allowed to edit or add instances of this model.
        '
        ' Keyword Arguments:
        '   user - User to check permission for.
        '
        ' Return: True if user is allowed to edit objects of this model and False otherwise.
        '''

        #Validate user object
        if not isinstance(user, Employee):
            raise TypeError("%s is not an auth user" % str(user))

        return True


    def get_viewable(self, user, filter_args=None, omni=None):
        '''
        ' Gets all ShiftSummerys that can be viewed or assigned by a specific AuthUser.
        '
        ' Keyword Arguments:
        '   user - User to filter viewable ShiftSummerys by.
        '
        ' Return: QuerySet of ShiftSummerys that can be viewed by specified user.
        '''
        # TODO: Wrapper until we decide to differentiate this from editable.
        return self.get_editable(user, filter_args, omni)


    def get_editable(self, user, filter_args=None, omni=None):
        ''' 
        ' Gets all the shifts that can be edited by a specified user.
        '
        ' Right now only superusers can edit.
        '
        ' Keyword Arguments:
        '   user - User to filter editable employees by.
        '
        ' Return: QuerySet of Shifts that are viewable by the specified User.
        '''
        if not isinstance(user, Employee):
            raise TypeError("%s is not an Auth User" % str(user))

        if filter_args is not None and len(filter_args) > 0:
            objs = self.advanced_search(**filter_args)
        elif omni is not None:
            objs = self.search(omni)
        else:
            objs = self.all()

        if user.is_superuser:
            return objs
        
        return objs.filter(employee = user)


class Shift(models.Model):
    employee = models.ForeignKey('Employee')
    time_in = models.DateTimeField('clock in time')
    time_out = models.DateTimeField('clock out time', null = True, blank=True)
    hours = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=4)
    deleted = models.BooleanField(default=False)


    objects = ShiftManager()

    column_options = {
        'id': {'grid_column': False}
        }

    # chucho omni search fields
    search_fields = ['id', 'employee', 'time_in', 'time_out']

    class Meta:
        db_table = 'Shift'
        ordering = ['-time_in', 'employee']

    def __unicode__(self):
        data = "TIME_IN: " + self.time_in.strftime("%Y-%m-%d %H:%M") + " TIME_OUT: "
        if(self.time_out != None):
            data += self.time_out.strftime("%Y-%m-%d %H:%M") + " " + self.employee.first_name + " " + self.employee.last_name
        else:
            data += " " + self.employee.first_name + " " + self.employee.last_name

        return data


    def toDict(self):
        
        return {
            "id": self.id
            ,"employee": self.employee.toDict()
            ,"time_in":  self.time_in.strftime(DT_FORMAT)
            ,"time_out": self.time_out.strftime(DT_FORMAT) if self.time_out is not None else self.time_out
            ,"hours":    str(self.hours) if self.hours is not None else self.hours
            ,"deleted":  self.deleted
        }


    def save(self, *args, **kwargs):
        if self.time_out is not None:
            diff = self.time_out - self.time_in
            hours = Decimal(diff.total_seconds()/3600).quantize(Decimal('1.00'))
            self.hours = hours
        else:
            self.hours = None

        super(Shift, self).save(*args, **kwargs)


    def can_view(self, user):
        '''
        ' Checks if a User instance is allowed to view this object instance or not.
        '
        ' Keyword Arguments:
        '   user - AuthUser to check if they have permissions.
        '
        ' Return: True if user is allowed to view and False otherwise.
        '''

        if not isinstance(user, Employee):
            raise TypeError('%s is not an auth user' % str(user))

        if user.is_superuser or user == self.employee:
            return True

        return False


    def can_edit(self, user):
        '''
        ' Checks if a User instance is allowed to edit this object instance or not.
        '
        ' Keyword Arguments:
        '   user - AuthUser to check if they have permissions.
        '
        ' Return: True if user is allowed to edit and False otherwise.
        '''

        if not isinstance(user, Employee):
            raise TypeError('%s is not an Employee' % str(user))

        if user.is_superuser or user == self.employee:
            return True

        return False

class ShiftSummaryManager(ChuchoManager):
    def get_editable_by_pk(self, user, pk):
        '''
        ' Get's an instance of ShiftSummery specified by a pk if the given user is allowed to edit it.
        '
        ' Keyword Arguments: 
        '   user - User to check if the user can be edited by them.
        '   pk   - Primary key of ShiftSummery to get.
        '
        ' Return: ShiftSummery identified by pk if user can edit it, otherwise None.
        '''
        
        if not isinstance(user, Employee):
            raise TypeError('%s is not an Auth User' % str(user))

        try:
            u = self.get(id=pk)
        except ShiftSummary.DoesNotExist:
            raise ShiftSummary.DoesNotExist("A ShiftSummary does not exist for the primary key %s." % str(pk))

        if user.is_superuser or u.employee == user:
            return u
        return None

    def can_edit(self, user):
        '''
        ' Checks if a User is allowed to edit or add instances of this model.
        '
        ' Keyword Arguments:
        '   user - User to check permission for.
        '
        ' Return: True if user is allowed to edit objects of this model and False otherwise.
        '''

        #Validate user object
        if not isinstance(user, Employee):
            raise TypeError("%s is not an auth user" % str(user))

        return True


    def get_viewable(self, user, filter_args=None, omni=None):
        '''
        ' Gets all ShiftSummerys that can be viewed or assigned by a specific AuthUser.
        '
        ' Keyword Arguments:
        '   user - User to filter viewable ShiftSummerys by.
        '
        ' Return: QuerySet of ShiftSummerys that can be viewed by specified user.
        '''
        # TODO: Wrapper until we decide to differentiate this from editable.
        return self.get_editable(user, filter_args, omni)


    def get_editable(self, user, filter_args=None, omni=None):
        ''' 
        ' Gets all the users that can be edited by a specified user.
        '
        ' Right now only superusers can edit.
        '
        ' Keyword Arguments:
        '   user - User to filter editable employees by.
        '
        ' Return: QuerySet of ShiftSummerys that are viewable by the specified User.
        '''
        if not isinstance(user, Employee):
            raise TypeError("%s is not an Auth User" % str(user))
        
        if filter_args is not None and len(filter_args) > 0:
            objs = self.advanced_search(**filter_args)
        elif omni is not None:
            objs = self.search(omni)
        else:
            objs = self.all()

        if user.is_superuser:
            return objs
        
        return objs.filter(employee=user)


class ShiftSummary(models.Model):
    job = models.ForeignKey('Job')
    employee = models.ForeignKey('Employee')
    shift = models.ForeignKey('Shift')
    hours = models.IntegerField('total hours')
    miles = models.DecimalField(max_digits = 6, decimal_places = 2, null = True, blank=True)
    note = models.TextField('notes about job', blank=True)

    objects = ShiftSummaryManager()

    column_options = {
        'id': {'grid_column': False}
        }

    # chucho omni search fields
    search_fields = ['id', 'job', 'employee', 'shift']

    class Meta:
        db_table = 'Shift Summary'
        ordering = ['shift', 'employee', 'job']
        unique_together = ('job', 'shift')

    def __unicode__(self):
        data = self.shift.time_in.date().strftime("%Y-%m-%d") + "    EMPLOYEE: " + self.employee.first_name + "  " + self.employee.last_name + "    JOB: " + self.job.name
        return data


class JobManager(ChuchoManager):
    def get_editable_by_pk(self, user, pk):
        '''
        ' Get's an instance of Job specified by a pk if the given user is allowed to edit it.
        '
        ' Keyword Arguments: 
        '   user - User to check if the user can be edited by them.
        '   pk   - Primary key of Job to get.
        '
        ' Return: Job identified by pk if user can edit it, otherwise None.
        '''
        if not isinstance(user, Employee):
            raise TypeError('%s is not an Auth User' % str(user))

        try:
            u = self.get(id=pk)
        except Job.DoesNotExist:
            raise Job.DoesNotExist("A Job does not exist for the primary key %s." % str(pk))

        if user.is_superuser:
            return u
        return None

    def can_edit(self, user):
        '''
        ' Checks if a User is allowed to edit or add instances of this model.
        '
        ' Keyword Arguments:
        '   user - User to check permission for.
        '
        ' Return: True if user is allowed to edit objects of this model and False otherwise.
        '''

        #Validate user object
        if not isinstance(user, Employee):
            raise TypeError("%s is not an auth user" % str(user))

        if user.is_superuser:
            return True

        return False


    def get_viewable(self, user, filter_args=None, omni=None):
        '''
        ' Gets all Jobs that can be viewed or assigned by a specific AuthUser.
        '
        ' Keyword Arguments:
        '   user - User to filter viewable Jobs by.
        '
        ' Return: QuerySet of Jobs that can be viewed by specified user.
        '''
       
        if not isinstance(user, Employee):
            raise TypeError("%s is not an Auth User" % str(user))
       
        if filter_args is not None:
            objs = self.advanced_search(**filter_args)
        elif omni is not None:
            objs = self.search(omni)
        else:
            objs = self.all()

        return objs.filter(is_active=True)


    def get_editable(self, user, filter_args=None, omni=None):
        ''' 
        ' Gets all the users that can be edited by a specified user.
        '
        ' Right now only superusers can edit.
        '
        ' Keyword Arguments:
        '   user - User to filter editable employees by.
        '
        ' Return: QuerySet of Jobs that are viewable by the specified User.
        '''
        if not isinstance(user, Employee):
            raise TypeError("%s is not an Auth User" % str(user))

        if user.is_superuser:
            if filter_args is not None and len(filter_args) > 0:
                return self.advanced_search(**filter_args)
            elif omni is not None:
                print omni
                return self.search(omni)
            else:
                return self.all()
        return self.none()


class Job(models.Model):
    name = models.TextField('job name')
    description = models.TextField('job description')
    is_active = models.BooleanField() 

    objects = JobManager()

    column_options = {
        'id': {'grid_column': False}
        }

    # chucho omni search fields
    search_fields = ['id', 'name', 'description']

    class Meta:
        db_table = 'Job'
        ordering = ['-is_active', 'name']

    def __unicode__(self):
        return self.name

    def can_view(self, user):
        '''
        ' Checks if a User instance is allowed to view this object instance or not.
        '
        ' Keyword Arguments:
        '   user - AuthUser to check if they have permissions.
        '
        ' Return: True if user is allowed to view and False otherwise.
        '''

        if not isinstance(user, Employee):
            raise TypeError('%s is not an auth user' % str(user))

        return True

    def get_summaries(self, employee, start=None, end=None):

        summaries = self.shiftsummary_set.filter(employee=employee, shift__deleted=False)

        if start is not None:
            summaries = summaries.filter(shift__time_out__gte=start)
        if end is not None:
            summaries = summaries.filter(shift__time_in__lte=end)

        return summaries


class TimesheetManager(models.Manager):

    def get_viewable(self, user):
        
        if not isinstance(user, Employee):
            raise TypeError("%s is not an Auth User" % str(user))

        if user.is_superuser:
            return self.all() 

        return self.filter(employee=user)


    @transaction.atomic
    def create_timesheets(self, data, user):
        newTimesheets = []
        for ts in data:
            newTimesheets.append(self.create_timesheet(ts, user))

        return newTimesheets

    @transaction.atomic
    def create_timesheet(self, data, user):

        ts = Timesheet(**data)
        ts.full_clean()
        ts.save()

        #Need to make sure to encompass the entire day.
        start = datetime.fromtimestamp(ts.start)
        start = start.replace(hour=00)
        start = start.replace(minute=00)
        start = start.replace(second=00)
        
        end = datetime.fromtimestamp(ts.end)
        end = end.replace(hour=23)
        end = end.replace(minute=59)
        end = end.replace(second=59)

        timesheets = Timesheet.objects.filter(start__lte=ts.end, end__gte=ts.start)
        assert timesheets.count() <= 0, "There is already a timesheet for employee %s for this pay period." % str(ts.employee)

        shifts = Shift.objects.filter(time_in__gte=start, time_out__lte=end, deleted=False, employee=ts.employee)
        ts.shifts = shifts

        return ts


class Timesheet(models.Model):

    shifts = models.ManyToManyField('shift')
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    employee = models.ForeignKey('Employee', related_name="timesheet_set")
    signature = models.TextField(blank=True)

    objects = TimesheetManager()

    class Meta:
        ordering = ['-end']


    def toDict(self):
        return {
            "id": self.id,
            "shifts": [s.toDict() for s in self.shifts.all()],
            "start": self.start,
            "end": self.end,
            "employee": self.employee.toDict(),
            "signature": self.signature
        }

    def sign(self, user):
        assert self.employee_id == user.id, "You may only sign your own timesheets."
        assert self.signature == "", "Timesheet is already signed."
        assert self.shifts.all().count() > 0, "There are no shifts belonging to this timesheet."

        strToHash = str(self.start) + str(self.end)
        strToHash += self.employee.username
        strToHash += "".join([s.time_in.strftime('%s')+s.time_out.strftime('%s')+s.employee.username for s in self.shifts.all()]) 
        self.signature = hash64(strToHash);
        self.save()
         



        