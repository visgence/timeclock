from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#normal views
urlpatterns = patterns('clocker.views.views',

    url(r'^$', RedirectView.as_view(url='/timeclock/')),
    url(r'^timeclock/hours/$', 'total_hours', name="get-total-hours"),
    url(r'chucho/', include('chucho.urls')),
)


urlpatterns += patterns('clocker.views.clockEmployee',
    url(r'^timeclock/clocker/$', 'clockEmployee', name="clock-employee"),
)


urlpatterns += patterns('clocker.views.mainPage',
    url(r'^timeclock/$', 'mainPage', name="render-main-page"),
)

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

#shift_summary stuff
urlpatterns += patterns('clocker.views.shiftSummary',
    url(r'^timeclock/saveSummaries/$', 'summary', name="save-summaries"),
    url(r'^timeclock/summary/(?P<id>\d+)/$', 'renderSummary', name="render-summary"),
)
