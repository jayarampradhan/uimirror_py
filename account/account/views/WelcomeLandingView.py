'''
   This class will be responsible to redirect to the next app home or url based on the state available in
   the state or default it will be navigate to the home screen.
'''

import logging

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import View

from account.constant import Constants
from account.tasks import updateStateCache
from custom_mixins.LoginCheckMixin import LoginCheckMixin


log = logging.getLogger(__name__)
class WelcomeLandingView(LoginCheckMixin, View):
    '''
       This will handle the request coming from welcome process complete page.
       This will handle the next redirect of request to which page, it might be user has requested for some other page
       so it will redirect to that.
       logic:
       get:
          It checks the state of the user and if found and then it will check for the destination if destination not found
          it will check for the app, then it redirect to the page based on the app code, if app is not found then it will
          redirect to the default social page  
    '''
    def get(self, request):
        '''
          Redirect based on the state.
        '''
        # TODO: Currently default navigation is to settings page with default state save
        state = {Constants.OBJECT:'setting', Constants.APP :'1'};
        profile_id = request.session.get(Constants.PRF_ID);
        updateStateCache.delay(state, profile_id); 
        return redirect(reverse('uim.profile.setting'));