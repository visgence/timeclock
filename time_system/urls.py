from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from clocker.views.management import ManageView

from clocker.views.shift import ShiftsView
from clocker.views.shift import ShiftView

from clocker.views.employee import EmployeesView
from clocker.views.employee import EmployeeView

from clocker.views.timesheet import TimesheetsView
from clocker.views.timesheet import TimesheetView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/timeclock/')),
    url(r'chucho/', include('chucho.urls')),
)

#Timesheet
urlpatterns += patterns('clocker.views.timesheet',
    url(r'^timeclock/hours/$', 'total_hours', name="get-total-hours"),
    url(r'^timeclock/timesheets/$', TimesheetsView.as_view(), name="timesheet-list"),
    url(r'^timeclock/timesheets/(?P<timesheet_id>)/$', TimesheetView.as_view(), name="timesheet-detail"),
)

#Management
urlpatterns += patterns('clocker.views.clockEmployee',
    url(r'^timeclock/manage/employees/$', ManageView.as_view(app="clocker", model="Employee"), name="manage-employees"),
    url(r'^timeclock/manage/jobs/$', ManageView.as_view(app="clocker", model="Job"), name="manage-jobs"),
    url(r'^timeclock/manage/summaries/$', ManageView.as_view(app="clocker", model="ShiftSummary"), name="manage-summaries"),
    url(r'^timeclock/manage/shifts/$', ManageView.as_view(template_name="manageShifts.html"), name="manage-shifts"),
)

#Employee clock in/out 
urlpatterns += patterns('clocker.views.clockEmployee',
    url(r'^timeclock/clocker/$', 'clockEmployee', name="clock-employee"),
)

#Main page
urlpatterns += patterns('clocker.views.mainPage',
    url(r'^timeclock/$', 'mainPage', name="render-main-page"),
)

#Jobs
urlpatterns += patterns('clocker.views.job',
    url(r'^timeclock/jobBreakdown/$', 'jobBreakdown', name="job-breakdown"),
)

#Password views
urlpatterns += patterns('clocker.views.password',
    url(r'^passwordForm/$', 'renderForm'),
    url(r'^changePassword/$', 'changePassword'),
)

#login views
urlpatterns += patterns('clocker.views.login',

    url(r'^timeclock/login/$', 'renderLogin', name="render-login"),
    url(r'^login/$', 'loginUser', name="login"),
    url(r'^logout/$', 'logoutUser', name="logout"),
)

#Employee summary stuff
urlpatterns += patterns('clocker.views.shiftSummary',
    url(r'^timeclock/saveSummaries/$', 'summary', name="save-summaries"),
    url(r'^timeclock/summary/(?P<id>\d+)/$', 'renderSummary', name="render-summary"),
)

#shifts
urlpatterns += patterns('clocker.views.shift',
    url(r'^timeclock/shifts/$', ShiftsView.as_view(), name="shift-list"),
    url(r'^timeclock/shifts/(?P<shift_id>\d+)/$', ShiftView.as_view(), name="shift-detail"),
)

#employees
urlpatterns += patterns('clocker.views.employee',
    url(r'^timeclock/employees/$', EmployeesView.as_view(), name="employee-list"),
    url(r'^timeclock/employees/(?P<employee_id>\d+)/$', EmployeeView.as_view(), name="employee-detail"),
)
