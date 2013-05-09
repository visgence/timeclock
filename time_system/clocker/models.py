from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model


class EmployeeManager(BaseUserManager):
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
        if not isinstance(user, auth_models.User):
            raise TypeError("%s is not an auth user" % str(user))

        if user.is_superuser:
            return True

        return False


    def get_viewable(self, user, filter_args=None):
        '''
        ' Gets all Employees that can be viewed or assigned by a specific AuthUser.
        '
        ' Keyword Arguments:
        '   user - User to filter viewable Employees by.
        '
        ' Return: QuerySet of Employees that can be viewed by specified user.
        '''
        # TODO: Wrapper until we decide to differentiate this from editable.
        return self.get_editable(user, filter_args)


    def get_editable(self, user, filter_args=None):
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
        if not isinstance(user, get_user_model()):
            raise TypeError("%s is not an Auth User" % str(user))
        if user.is_superuser:
            if filter_args is not None:
                return self.filter(**filter_args)
            else:
                return self.all()
        return self.none()

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


    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

    def can_view(self, user):
        '''
        ' Checks if a User instance is allowed to view this object instance or not.
        '
        ' Keyword Arguments:
        '   user - AuthUser to check if they have permissions.
        '
        ' Return: True if user is allowed to view and False otherwise.
        '''

        if not isinstance(user, get_user_model()):
            raise TypeError('%s is not an auth user' % str(user))

        if user.is_superuser or user == self.user:
            return True

        return False

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

class ShiftManager(models.Manager):
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
        AuthUser = get_user_model()
        if not isinstance(user, AuthUser):
            raise TypeError('%s is not an Auth User' % str(user))

        try:
            u = self.get(id=pk)
        except Shift.DoesNotExist:
            raise Shift.DoesNotExist("A Shift does not exist for the primary key %s." % str(pk))

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
        if not isinstance(user, auth_models.User):
            raise TypeError("%s is not an auth user" % str(user))

        if user.is_superuser:
            return True

        return False


    def get_viewable(self, user, filter_args=None):
        '''
        ' Gets all ShiftSummerys that can be viewed or assigned by a specific AuthUser.
        '
        ' Keyword Arguments:
        '   user - User to filter viewable ShiftSummerys by.
        '
        ' Return: QuerySet of ShiftSummerys that can be viewed by specified user.
        '''
        # TODO: Wrapper until we decide to differentiate this from editable.
        return self.get_editable(user, filter_args)


    def get_editable(self, user, filter_args=None):
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
        if not isinstance(user, get_user_model()):
            raise TypeError("%s is not an Auth User" % str(user))
        if user.is_superuser:
            if filter_args is not None:
                return self.filter(**filter_args)
            else:
                return self.all()
        return self.none()


class Shift(models.Model):
    employee = models.ForeignKey('Employee')
    time_in = models.DateTimeField('clock in time')
    time_out = models.DateTimeField('clock out time', null = True, blank=True)
    hours = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=4)

    objects = ShiftManager()
    
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


    def can_view(self, user):
        '''
        ' Checks if a User instance is allowed to view this object instance or not.
        '
        ' Keyword Arguments:
        '   user - AuthUser to check if they have permissions.
        '
        ' Return: True if user is allowed to view and False otherwise.
        '''

        if not isinstance(user, get_user_model()):
            raise TypeError('%s is not an auth user' % str(user))

        if user.is_superuser or user == self.employee.user:
            return True

        return False


class ShiftSummeryManager(models.Manager):
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
        AuthUser = get_user_model()
        if not isinstance(user, AuthUser):
            raise TypeError('%s is not an Auth User' % str(user))

        try:
            u = self.get(id=pk)
        except ShiftSummary.DoesNotExist:
            raise ShiftSummary.DoesNotExist("A ShiftSummary does not exist for the primary key %s." % str(pk))

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
        if not isinstance(user, auth_models.User):
            raise TypeError("%s is not an auth user" % str(user))

        if user.is_superuser:
            return True

        return False


    def get_viewable(self, user, filter_args=None):
        '''
        ' Gets all ShiftSummerys that can be viewed or assigned by a specific AuthUser.
        '
        ' Keyword Arguments:
        '   user - User to filter viewable ShiftSummerys by.
        '
        ' Return: QuerySet of ShiftSummerys that can be viewed by specified user.
        '''
        # TODO: Wrapper until we decide to differentiate this from editable.
        return self.get_editable(user, filter_args)


    def get_editable(self, user, filter_args=None):
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
        if not isinstance(user, get_user_model()):
            raise TypeError("%s is not an Auth User" % str(user))
        if user.is_superuser:
            if filter_args is not None:
                return self.filter(**filter_args)
            else:
                return self.all()
        return self.none()


class ShiftSummary(models.Model):
    job = models.ForeignKey('Job')
    employee = models.ForeignKey('Employee')
    shift = models.ForeignKey('Shift')
    hours = models.IntegerField('total hours')
    miles = models.DecimalField(max_digits = 6, decimal_places = 2, null = True, blank=True)
    note = models.TextField('notes about job')

    objects = ShiftSummeryManager()

    class Meta:
        db_table = 'Shift Summary'
        ordering = ['shift', 'employee', 'job']

    def __unicode__(self):
        data = self.shift.time_in.date().strftime("%Y-%m-%d") + "    EMPLOYEE: " + self.employee.user.first_name + "  " + self.employee.user.last_name + "    JOB: " + self.job.name
        return data


class JobManager(models.Manager):
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
        AuthUser = get_user_model()
        if not isinstance(user, AuthUser):
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
        if not isinstance(user, auth_models.User):
            raise TypeError("%s is not an auth user" % str(user))

        if user.is_superuser:
            return True

        return False


    def get_viewable(self, user, filter_args=None):
        '''
        ' Gets all Jobs that can be viewed or assigned by a specific AuthUser.
        '
        ' Keyword Arguments:
        '   user - User to filter viewable Jobs by.
        '
        ' Return: QuerySet of Jobs that can be viewed by specified user.
        '''
        # TODO: Wrapper until we decide to differentiate this from editable.
        return self.get_editable(user, filter_args)


    def get_editable(self, user, filter_args=None):
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
        if not isinstance(user, get_user_model()):
            raise TypeError("%s is not an Auth User" % str(user))
        if user.is_superuser:
            if filter_args is not None:
                return self.filter(**filter_args)
            else:
                return self.all()
        return self.none()


class Job(models.Model):
    name = models.CharField('job name', max_length = 25)
    description = models.TextField('job description')
    is_active = models.BooleanField() 

    objects = JobManager()

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

        if not isinstance(user, get_user_model()):
            raise TypeError('%s is not an auth user' % str(user))

        if user.is_superuser:
            return True

        return False
