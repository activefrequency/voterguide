from django.conf.urls import patterns, include, url

# import .views

urlpatterns = patterns('',
    url(r'^$', 'voterguide.views.home', name='home'),
    url(r'^lookup/$', 'voterguide.views.district_lookup', name='district_lookup'),
)
