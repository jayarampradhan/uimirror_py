from django.core.cache import cache
from django.shortcuts import redirect
'''
   This mixin is default abstract class for the state presume operation for the different view,
   Different view might have different way of handling the state thats the reason it has left to the implementation people to
   implement according to the the view and logic 
'''
class StateCheckMixin(object):
    state_presume_failure_path = ''  # can be path, url name or reverse_lazy

    def check_state(self, request):
        '''
           This will check the state of the user, if user state found from cookie or session and exists the corresponding details in cache
           then analyse the state if the current request is valid process the response else navigate to the failed path.
           presume state will try to query the user profile and check to see if any default state can be stored.
        '''
        from account.constant import Constants
        prf_id = request.session.get(Constants.PRF_ID);
        state_id = prf_id +Constants.STATE_POST_FIX;
        state = cache.get(state_id)
        if prf_id and state:  
            return self.analyse_state(state)
        else:
            return self.presume_and_analyse_state(prf_id);
    
    def presume_and_analyse_state(self, prf_id):
        return True
    
    def analyse_state(self, state):
        return True

    def do_fail_navigation(self, request, *args, **kwargs):
        return redirect(self.state_presume_failure_path);