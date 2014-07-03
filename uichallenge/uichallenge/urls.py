from django.conf.urls import patterns, include, url

from uichallenge.views.UpdatesView import UpdatesView
from uichallenge.views.ChallengeView import ChallengeView

urlpatterns = patterns('',
    url(r'^$', UpdatesView.as_view(), name='uim.challenge.feed.view'),
    url(r'^ch/rule/(?P<cid>\d+)/(?P<cname>.+)/$', ChallengeView.as_view(), name='uim.challenge.view'),
)
