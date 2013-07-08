from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from dajaxice.core import dajaxice_config, dajaxice_autodiscover
from settings import APP_PATH, DEBUG
admin.autodiscover()
dajaxice_autodiscover()

#normal views
urlpatterns = patterns('clocker.views',
    # Examples:
    # url(r'^$', 'time_system.views.home', name='home'),
    # url(r'^time_system/', include('time_system.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^timeclock/$', 'main_page'),
    url(r'^timeclock/hours/$', 'total_hours'),
    url(r'^$', RedirectView.as_view(url='/timeclock/')),


    # Uncomment the next line to enable the admin:
    url(r'(?i)^utilities/', include('chucho.urls')),                                                                                                                                                
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += patterns('clocker.password',

    url(r'^passwordForm/$', 'renderForm'),
    url(r'^changePassword/$', 'changePassword'),

)

if DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^images\/(?P<path>.+)$', 'django.views.static.serve', {
            'document_root': APP_PATH + 'chucho/static/plugins/slickGrid/images'})
    )

#login views
urlpatterns += patterns('clocker.login',
    url(r'^timeclock/login/$', 'view'),
    url(r'^logout/$', 'logout'),
)

#shift_summary stuff
urlpatterns += patterns('clocker.shift_summary',
    url(r'^timeclock/shift_summary/$', 'summary'),
)
