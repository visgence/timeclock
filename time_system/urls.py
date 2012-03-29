from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'time_system.views.home', name='home'),
    # url(r'^time_system/', include('time_system.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^timeclock/$', 'clocker.views.main_page'),
    url(r'^login/$', 'clocker.login.view'),
    url(r'^logout/$', 'clocker.login.logout'),
    url(r'^$', redirect_to, {'url':'/timeclock/'}),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
