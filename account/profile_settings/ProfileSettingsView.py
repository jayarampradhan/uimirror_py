import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View

from account.constant import Constants
from custom_mixins.LoginCheckMixin import LoginCheckMixin
from user_management.UserMixin import findOrUpdateBasicProfileCache


log = logging.getLogger(__name__)
class ProfileSettingsView(LoginCheckMixin, View):
    
    def get(self, request):
        profile_id = request.session.get(Constants.PRF_ID);
        from django.core.cache import cache
        state = cache.get(profile_id +Constants.STATE_POST_FIX);
        state['usr'] = findOrUpdateBasicProfileCache(profile_id);
        context = RequestContext(request, state);
        log.info('[END]- Welcome View rendered.');
        return render_to_response('profile/settings/social/home.html',context);
        pass
        # TODO: Complete This Functionality with UI 