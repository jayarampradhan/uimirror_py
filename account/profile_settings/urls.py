from django.conf.urls import patterns, url
from profile_settings.ProfileSettingsView import ProfileSettingsView

urlpatterns = patterns('',
    url(r'^$', ProfileSettingsView.as_view(), name='uim.profile.setting'),
)