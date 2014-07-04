from django.conf.urls import patterns, include, url

from uichallenge.views.UpdatesView import UpdatesView
from uichallenge.views.ChallengeView import ChallengeView
from uichallenge.views.ChallengeApearView import ChallengeAppearView
from uichallenge.views.ProfileView import ProfileView

urlpatterns = patterns('',
    url(r'^$', UpdatesView.as_view(), name='uim.challenge.feed.view'),
    url(r'^ch/rule/(?P<cid>\d+)/(?P<cname>.+)/$', ChallengeView.as_view(), name='uim.challenge.view'),
    url(r'^ch/appear/(?P<cid>\d+)/(?P<cname>.+)/$', ChallengeAppearView.as_view(), name='uim.challenge.appear'),
    url(r'^users/(?P<pid>\d+)/(?P<name>.+)/$', ProfileView.as_view(), name='uim.challenge.profile'),
)
