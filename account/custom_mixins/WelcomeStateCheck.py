'''
   This will handle the state for the welcome page.
   State Object Common format is {Obj, Step, }
'''
from django.core.cache import cache

from account.constant import Constants
from custom_mixins.LoginWithStateCheckMixin import LoginWithStateCheckMixin
from user_management.UserMixin import findOrUpdateProfileAttribute


class WelcomeStateCheck(LoginWithStateCheckMixin):
    state_presume_failure_path = '';
    
    def presume_and_analyse_state(self, profile_id):
        '''
           On the basics of the profile ID, it will retreive the user record either from the cache
           or WEB Service call.
           Then checks if user attribute if he is really destination suggest to navigate the do the navigation
           then call analyse state to take the routing logic.
        '''
        # TODO: This will be a call to user profile if user really needs the welcome page or not.
        attr, state = findOrUpdateProfileAttribute(profile_id), False;
        if attr.get('age') == 'new':
            state = {Constants.OBJECT:'welcome', Constants.STEP:'1'};
            cache.set(profile_id+Constants.STATE_POST_FIX, state)
        return self.analyse_state(state)
    
    def analyse_state(self, state):
        if state and state.get(Constants.OBJECT) == Constants.WELCOME_OBJ:
            return True;
        else:
            return False;
