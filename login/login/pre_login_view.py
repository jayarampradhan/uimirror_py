from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import View
from ui_utilities.destination_builder import getDestinationByAppCode
import logging

log = logging.getLogger(__name__)
class PreLogin(View):
    '''
        Class will take care about initial request for login request.
        It will validate the request URL and redirect to login page.
        PATH VARIABLES:
           -request: A HttpRequest object which has originated the request.
           -app_code: Application code from which application request has been comes from, default to 1 i.e social.
        GET VARIABLES:
            -nxt: A Next URL to be navigated back.
            -des: A Next URL to be navigated back.
            It will take either one not all.
       LOGIC:
           GET:
               Based on the destination/next URL it will frame the login URL and send back.
               If it doesn't have any then it will be default to social if app-code not present.
    '''
    
    def get(self, request, app_code='1'):
        
        '''
           This will be used for any login request landing for this page.
           It will set the cookie and return back.
           @param request: HttpRequest for the this view
           @param app_code: Application code which made request to login
        '''
        log.info('[START]- Request will be redirected to login page.')
        # First check where user want to navigate after login process
        destination = request.GET.get('nxt', request.GET.get('des')) 
        destination = destination if destination else getDestinationByAppCode(app_code);
        log.info('[END]- URL formation for the login page redirect completed.')
        return redirect('%s?des=%s' %(reverse('uim.login', kwargs={'app_code':app_code}), destination))
