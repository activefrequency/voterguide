from django.conf.urls import url

import views

urlpatterns = [
    url(r'^import/$', views.import_candidates, name='import_candidates'),
    url(r'^import-districts/$', views.import_districts, name='import_districts'),
]

urlpatterns += [
    url(r'^$', views.home, name='home'),
    url(r'^local/$', views.district_lookup, name='district_lookup'),
    url(r'^statewide/$', views.statewide, name='statewide'),
    url(r'^list/$', views.candidate_list, name='candidate_list'),
    url(r'^about/$', views.about, name='about'),
    url(r'^placeholder/$', views.placeholder, name='placeholder'),

    # Utils
    url(r'^util/trigger-500/$', views.util_trigger_500, name='util_trigger_500'),
]
