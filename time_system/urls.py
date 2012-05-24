from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#normal views
urlpatterns = patterns('clocker.views',
    # Examples:
    # url(r'^$', 'time_system.views.home', name='home'),
    # url(r'^time_system/', include('time_system.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^timeclock/$', 'main_page'),
    url(r'^timeclock/hours/$', 'total_hours'),
    url(r'^$', redirect_to, {'url':'/timeclock/'}),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#login views
urlpatterns += patterns('clocker.login',
    url(r'^login/$', 'view'),
    url(r'^logout/$', 'logout'),
)

#shift_summary stuff
urlpatterns += patterns('clocker.shift_summary',
    url(r'^timeclock/shift_summary/$', 'summary'),
)
