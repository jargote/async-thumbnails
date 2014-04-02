from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Available API urls in the images server.
urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.create_images', name='download_images'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
