from django.conf.urls import url
from django.conf import settings

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
]
