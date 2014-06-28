from django.conf.urls import patterns, url
from locationservice.LocationView import HandleLocation


urlpatterns = patterns('',
    url(r'^$', HandleLocation.as_view(), name='uim.location'),
)