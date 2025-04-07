from django.conf.urls import include, url
from django.views.generic import RedirectView
from clocker.views.management import ManageView

from clocker.views.shift import ShiftsView
from clocker.views.shift import ShiftView

from clocker.views.employee import EmployeesView
from clocker.views.employee import EmployeeView

import clocker.views.timesheet
import clocker.views.clockEmployee
import clocker.views.mainPage
import clocker.views.job
import clocker.views.shiftExport
import clocker.views.password
import clocker.views.login
import clocker.views.shiftSummary

from clocker.views.timesheet import TimesheetsView
from clocker.views.timesheet import TimesheetView
from settings import ENABLE_JOBS

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/timeclock/')),
    url(r'chucho/', include('chucho.urls')),
]

# Timesheet
urlpatterns += [
    url(r'^timeclock/hours/$', clocker.views.timesheet.total_hours, name="get-total-hours"),
    url(r'^timeclock/timesheets/$', TimesheetsView.as_view(), name="timesheet-list"),
    url(r'^timeclock/timesheets/(?P<timesheet_id>\d+)/$', TimesheetView.as_view(), name="timesheet-detail"),
]

# #Management
urlpatterns += [
     url(r'^timeclock/manage/employees/$', ManageView.as_view(app="clocker", model="Employee"), name="manage-employees"),
     url(r'^timeclock/manage/summaries/$', ManageView.as_view(app="clocker", model="ShiftSummary"), name="manage-summaries"),
     url(r'^timeclock/manage/shifts/$', ManageView.as_view(template_name="manageShifts.html"), name="manage-shifts", kwargs={'enable_jobs': ENABLE_JOBS}),
]

if ENABLE_JOBS:
    urlpatterns += [url(r'^timeclock/manage/jobs/$', ManageView.as_view(app="clocker", model="Job"), name="manage-jobs"),]
else:
    urlpatterns += [url(r'^timeclock/manage/jobs/$', RedirectView.as_view(url='/timeclock/')),]

# #Employee clock in/out
urlpatterns += [
    url(r'^timeclock/clocker/$', clocker.views.clockEmployee.clockEmployee, name="clock-employee"),
]

# #Main page
urlpatterns += [
    url(r'^timeclock/$', clocker.views.mainPage.mainPage, name="render-main-page"),
]

# #Jobs
urlpatterns += [
    url(r'^timeclock/jobBreakdown/$', clocker.views.job.jobBreakdown, name="job-breakdown"),
]
# #Shift Export
urlpatterns += [
    url(r'^timeclock/shiftExport/$', clocker.views.shiftExport.shiftExport, name="shift-export"),
]

# #Password views
urlpatterns += [
    url(r'^passwordForm/$', clocker.views.password.renderForm),
    url(r'^changePassword/$', clocker.views.password.changePassword),
]

# #login views
urlpatterns += [

    url(r'^timeclock/login/$', clocker.views.login.renderLogin, name="render-login"),
    url(r'^login/$', clocker.views.login.loginUser, name="login"),
    url(r'^logout/$', clocker.views.login.logoutUser, name="logout"),
    url(r'^login/check/$', clocker.views.login.isLoggedIn, name="check-login"),
]

if ENABLE_JOBS:
    # #Employee summary stuff
    urlpatterns += [
        url(r'^timeclock/saveSummaries/$', clocker.views.shiftSummary.summary, name="save-summaries"),
        url(r'^timeclock/summary/(?P<id>\d+)/$', clocker.views.shiftSummary.renderSummary, name="render-summary"),
    ]
else:
    urlpatterns += [
        url(r'^timeclock/saveSummaries/$', RedirectView.as_view(url='/timeclock/')),
        url(r'^timeclock/summary/(?P<id>\d+)/$', RedirectView.as_view(url='/timeclock/')),
    ]

# #shifts
urlpatterns += [
    url(r'^timeclock/shifts/$', ShiftsView.as_view(), name="shift-list"),
    url(r'^timeclock/shifts/(?P<shift_id>\d+)/$', ShiftView.as_view(), name="shift-detail"),
    url(r'^timeclock/manage/missingshifts/$', ManageView.as_view(template_name="missingShifts.html"), name="manage-missing-shifts"),
    url(r'^timeclock/missingShifts/$', clocker.views.job.missingShifts, name="missing-shifts"),
]

# #employees
urlpatterns += [
    url(r'^timeclock/employees/$', EmployeesView.as_view(), name="employee-list"),
    url(r'^timeclock/employees/(?P<employee_id>\d+)/$', EmployeeView.as_view(), name="employee-detail"),
]
