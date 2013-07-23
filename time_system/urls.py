from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#normal views
urlpatterns = patterns('clocker.views.views',
    # Examples:
    # url(r'^$', 'time_system.views.home', name='home'),
    # url(r'^time_system/', include('time_system.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^timeclock/$', 'main_page'),
    url(r'^timeclock/hours/$', 'total_hours'),
    url(r'^$', RedirectView.as_view(url='/timeclock/')),


    # Uncomment the next line to enable the admin:
    url(r'chucho/', include('chucho.urls')),                                                                                                                                                
)

urlpatterns += patterns('clocker.views.password',

    url(r'^passwordForm/$', 'renderForm'),
    url(r'^changePassword/$', 'changePassword'),

)

#login views
urlpatterns += patterns('clocker.views.login',
    url(r'^timeclock/login/$', 'view'),
    url(r'^logout/$', 'logout'),
)

#shift_summary stuff
urlpatterns += patterns('clocker.views.shift_summary',
    url(r'^timeclock/shift_summary/$', 'summary'),
)
