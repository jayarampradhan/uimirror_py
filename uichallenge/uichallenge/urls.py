from django.conf.urls import patterns, include, url

from uichallenge.views.UpdatesView import UpdatesView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uichallenge.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', UpdatesView.as_view(), name='uimirror.challenge.feed.view'),
)
