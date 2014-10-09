from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^import/$', 'voterguide.views.import_candidates', name='import_candidates'),
    url(r'^import-districts/$', 'voterguide.views.import_districts', name='import_districts'),
)

# if we've turned on placeholder mode, insert this before everything else
# (but after /import/, since we still want that to be usable!)
if settings.SHOW_PLACEHOLDER:
    urlpatterns += patterns('',
        url(r'^.*$', 'voterguide.views.placeholder', name='placeholder'),
    )

urlpatterns += patterns('',
    url(r'^$', 'voterguide.views.home', name='home'),
    url(r'^local/$', 'voterguide.views.district_lookup', name='district_lookup'),
    url(r'^statewide/$', 'voterguide.views.statewide', name='statewide'),
    url(r'^list/$', 'voterguide.views.candidate_list', name='candidate_list'),
    url(r'^about/$', 'voterguide.views.about', name='about'),
)
