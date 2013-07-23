from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from datetime import datetime
from decimal import Decimal
import re

from chucho.models import ChuchoManager

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
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.now())

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
        """
        Clocks an employee out.  
        
        Returns: 
            The error message "none" if the user clocked out and "out" if the user was not able to clock out.
        """
      
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
        

    def which_clock(self):
        """
        Checks to see whether an employee is clocked in or out. 

        Returns:
            A dictionary with the status of the employee and the maximum time record that was used to determine this.
            Keys: 'status' 'max_record'
        TODO: It is possible for an admin to never be clocked into our time system. 
        """

        shift = Shift.objects.filter(employee=self, time_out=None)
        if(shift.count() > 1):
            raise Exception("Error, you are clocked in more than once!")
        
        #if(shift.employee == None):
        #    stuff = {'status':"out", 'max_record':None}
        #    return stuff

        stuff = {}
        if(shift.count() == 0):
            stuff['status'] = "out"
            max_record = Shift.objects.all().aggregate(models.Max('id'))
            stuff['max_record'] = Shift.objects.get(id=max_record['id__max'])
            return stuff 
       
        stuff['status'] = "in"
        stuff['max_record'] = shift[0]
        return stuff 


    def get_current_time(self):

        dictionary = self.which_clock()

        if(dictionary['status'] == "in"):
            time_in = dictionary['max_record'].time_in
            time_now = datetime.now()


class ShiftManager(ChuchoManager):
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

    objects = ShiftManager()

    column_options = {
        'id': {'grid_column': False}
        }

    # chucho omni search fields
    search_fields = ['employee', 'time_in', 'time_out']

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
    note = models.TextField('notes about job')

    objects = ShiftSummaryManager()

    column_options = {
        'id': {'grid_column': False}
        }

    # chucho omni search fields
    search_fields = ['job', 'employee', 'shift']

    class Meta:
        db_table = 'Shift Summary'
        ordering = ['shift', 'employee', 'job']

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
    name = models.CharField('job name', max_length = 25)
    description = models.TextField('job description')
    is_active = models.BooleanField() 

    objects = JobManager()

    column_options = {
        'id': {'grid_column': False}
        }

    # chucho omni search fields
    search_fields = ['name', 'description']

    class Meta:
        db_table = 'Job'
        ordering = ['-is_active']

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
