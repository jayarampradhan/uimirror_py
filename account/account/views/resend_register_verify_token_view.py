import logging
from django.conf import settings
from django.views.generic.base import View
from custom_mixins.sendajaxresponsemixin import sendResponse


log = logging.getLogger(__name__)
class ResendVrfyEmailView(View):
    '''
       This class will help to request for re-sending the token mail for the Recently Registered User For Verification.
       PATH VARIABLES:
           -request: A HttpRequest object which has originated the request.
           -tpid: Profile Id of the user
        GET VARIABLES:
            -email: An Email Id, through which a mail will be sent out.
       LOGIC:
           POST:
               If user has all the valid details, it will be requested for the new token that will be send to his email ID.
    '''
    
    def post(self, request, tpid):
        '''
           This will be handleing for any re-send verification mail.
           @param request: HttpRequest of client
           @param tpid: Temporary Created Profile Id.
        '''
        log.info('[START]- Request Received for re-sending the token mail for the Recent Register Verification process.');
        
        _email = request.GET.get('em');
        #If request is not valid stop the request processing
        if not _email:
            log.info('[END]- Request aborting as the entered details are not correct.');
            dic = {};
            dic['CODE'] = '403';
            dic['message'] = 'Sorry your request can\'t be processed now.';
            return sendResponse(request, dic);
        
        #write logic for the request process, then return the response
        #Get user Agent and IP
        from useragent.determine_user_agent import UserAgent
        USER_AGENT = UserAgent()
        user_ip, user_agent = USER_AGENT.get_client_ip(request), USER_AGENT.get_browser_agent(request);
        #build temporary response to be handel but latter it needs to be web service call
        res =  self.requestForNewToken(tpid, _email, user_ip, user_agent);
        # process for the service call and return back with the response
        dev_mode = getattr(settings, "SKIP_WEB_CALL", 'n');
        log.info('[END]- Request Completed for the re-send token email for forgot password.');
        if dev_mode == 'y':
            return sendResponse(request, self.webMockData());
        
        return sendResponse(request, res);
    
    def requestForNewToken(self, tpid, _email, user_ip, user_agent):
        '''
           This will Re-send verify email user by calling the service.
           @param request: HttpRequest object submitted by user.
           @param form: Register form submitted by user.
        '''
        # for the Data Form to be sent over network
        form = {"pid": tpid, "client_meta": user_agent, "ip": user_ip, "email": _email}
        WEB_BASE_URL = getattr(settings, "REST_BASE_URL", None);
        WEB_BASE_URL += 'resendlinktoken';
        import urllib
        data = urllib.urlencode(form, doseq=True);
        #make instance of rest client
        from ui_utilities.http_api import RestClient
        client = RestClient();
        return client.postWithAuthHeader(WEB_BASE_URL, data);
    
        
    def webMockData(self):
        dic = {};
        dic['RESCD'] = '200';
        dic['EMAIL'] = 'jayaramimca@gmail.com';
        return dic;
        
