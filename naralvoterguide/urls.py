from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('voterguide.urls')),
    url(r'^tools/', include(admin.site.urls)),
    url(r'^front-edit/', include('front.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico'), name='favicon'),
)

urlpatterns += staticfiles_urlpatterns()
