from django.conf.urls import patterns, include, url
from django.contrib import admin
from uiexpense.views.UpdatesView import UpdatesView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', UpdatesView.as_view(), name='uimirror.challenge.feed.view'),
)
