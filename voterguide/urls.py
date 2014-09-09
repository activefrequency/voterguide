from django.conf.urls import patterns, include, url

# import .views

urlpatterns = patterns('',
    url(r'^.*$', 'voterguide.views.placeholder', name='placeholder'),

    url(r'^$', 'voterguide.views.home', name='home'),
    url(r'^local/$', 'voterguide.views.district_lookup', name='district_lookup'),
    url(r'^statewide/$', 'voterguide.views.statewide', name='statewide'),
    url(r'^list/$', 'voterguide.views.candidate_list', name='candidate_list'),
    url(r'^about/$', 'voterguide.views.about', name='about'),
    url(r'^import/$', 'voterguide.views.import_candidates', name='import_candidates'),
)
