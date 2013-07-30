from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from clocker.views.management import ManageView


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/timeclock/')),
    url(r'chucho/', include('chucho.urls')),
)

#Timesheet
urlpatterns += patterns('clocker.views.timesheet',
    url(r'^timeclock/hours/$', 'total_hours', name="get-total-hours"),
)

#Management
urlpatterns += patterns('clocker.views.clockEmployee',
    url(r'^timeclock/manage/employees/$', ManageView.as_view(app="clocker", model="Employee"), name="manage-employees"),
    url(r'^timeclock/manage/jobs/$', ManageView.as_view(app="clocker", model="Job"), name="manage-jobs"),
    url(r'^timeclock/manage/summaries/$', ManageView.as_view(app="clocker", model="ShiftSummary"), name="manage-summaries"),
    url(r'^timeclock/manage/shifts/$', ManageView.as_view(app="clocker", model="Shift"), name="manage-shifts"),
)

#Employee clock in/out 
urlpatterns += patterns('clocker.views.clockEmployee',
    url(r'^timeclock/clocker/$', 'clockEmployee', name="clock-employee"),
)

#Main page
urlpatterns += patterns('clocker.views.mainPage',
    url(r'^timeclock/$', 'mainPage', name="render-main-page"),
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

#shift summary stuff
urlpatterns += patterns('clocker.views.shiftSummary',
    url(r'^timeclock/saveSummaries/$', 'summary', name="save-summaries"),
    url(r'^timeclock/summary/(?P<id>\d+)/$', 'renderSummary', name="render-summary"),
)
