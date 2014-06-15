import logging
from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from account.constant import Constants
from custom_mixins.WelcomeStateCheck import WelcomeStateCheck

log = logging.getLogger(__name__)

class WelcomeView(WelcomeStateCheck, View):
    '''
       This will be responsible to render the welcome page with some steps which user needs to fill up.
       Before Coming to this user must be authenticated.
       It has get method to show the screen and post call responsible for rendering the page.
       PATH VARIABLES:
           -request: A HttpRequest object which has originated the request.
        GET VARIABLES:
            -des: A destination to which it will be redirected back in case request completed successfully.
       LOGIC:
           GET:
               User should be logged in and user should have a state which says to render this page.
               This will get the state, user details and redirect to the UI.
           POST:
               NA
    '''
    def get(self, request):
        '''
           This will be used for any Register request landing for this page.
           This will load the first time steps page with face book profile import.
           @param request: HttpRequest made by the user.
        '''
        # First Get the session Details 
        log.info('[START]- Request Received for the Welcome View')
        profile_id = request.session.get(Constants.PRF_ID);
        state = cache.get(profile_id +Constants.STATE_POST_FIX);
        log.info('[INTERIM]- User State Restored and doing the fresh render.');
        state.pop(Constants.OBJECT, None);
        from user_management.UserMixin import findOrUpdateBasicProfileCache
        state['usr'] = findOrUpdateBasicProfileCache(profile_id);
        if(state.get(Constants.STEP) == '3' or state.get(Constants.STEP) == 3):
            state['contacts'] = cache.get(profile_id+Constants.CH_IMPORTED_KEY+state.get(Constants.IMPORT_SERVICE_PRVOVIDER));
        context = RequestContext(request, state);
        log.info('[END]- Welcome View rendered.');
        return render_to_response('welcome/steps.html',context);
        
if __name__ == '__main__':
    pass
