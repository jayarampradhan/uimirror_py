import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View

from account.constant import Constants
from custom_mixins.LoginCheckMixin import LoginCheckMixin
from user_management.UserMixin import findOrUpdateBasicProfileCache, \
    findOrUpdateProfileSettingsCache


log = logging.getLogger(__name__)
class ProfileSettingsView(LoginCheckMixin, View):
    
    def get(self, request, app = 'social'):
        log.info('[START]- Request Received for the settings Page');
        tab = request.GET.get('ref', self.determineDefaultTab(app));
        profile_id = request.session.get(Constants.PRF_ID);
        # TODO: Get the user settings by app name and tab DO smart guess fo tab, if no tab then get all result for that app
        res = {}
        res['usr'] = findOrUpdateBasicProfileCache(profile_id);
        tab_data = {}
        tab_data[tab] = findOrUpdateProfileSettingsCache(profile_id, app, tab)
        res[app] = tab_data
        log.debug('Response Getting Send is  %s',res); 
        context = RequestContext(request, res);
        log.info('[START]- Request Rendered for the settings Page');
        return render_to_response('profile/settings/social/home.html',context);
        # TODO: Complete This Functionality with UI
        
    def determineDefaultTab(self, appname):
        if appname == 'social':
            return 'chat'; 