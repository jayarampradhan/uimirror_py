import logging
import urllib

from django.conf import settings
from django.http.response import HttpResponse
from django.views.generic.base import View

from ui_utilities.JSONResponseMixin import JSONResponseMixin
from ui_utilities.http_api import RestClient
from useragent.determine_user_agent import UserAgent


log = logging.getLogger(__name__)
class ResendResetMail(View):
    '''
       This class will help to request for re-sending the token mail for the forgot password request process.
       PATH VARIABLES:
           -request: A HttpRequest object which has originated the request.
           -app_code: Application code from which application request has been comes from.
           -mode: Specifies the way user trying to reset the password, either by his own registered mail or by alternative mail.
           -pid: Profile Id of the user
           -rid: Request ID of the user previously created forgot password request
        GET VARIABLES:
            -email: An Email Id, through which a mail will be sent out.
            -alt_email: In case user has opted for the reseting the password through the alternative email.
       LOGIC:
           POST:
               If user has all the valid details, it will be requested for the new token that will be send to his email/alternative email ID.
    '''
    
    def post(self, request, app_code, mode, pid, rid):
        '''
           This will be a post request to re-send the email with link and token for password reset request.
           @param request: A HttpRequest object
           @param app_code: Application from which request initiated
           @param mode: Reset mode 1, for by own registered mail or 2 for by other alternative mail.
           @param pid: Profile Id of the user.
           @param rid: A Valid Request open ID.
           @return: A response message saying delivered link or not.
        '''
        log.info('[START]- Request Received for re-sending the token mail for the password reset process.');
        
        _email, _alt_email = request.GET.get('em'), request.GET.get('alt');
        #If request is not valid stop the request processing
        if not _email or (mode == '2' and not _alt_email):
            log.info('[END]- Request aborting as the entered details are not correct.');
            dic = {};
            dic['CODE'] = '403';
            dic['message'] = 'Sorry your request can\'t be processed now.';
            return self.handelResponse(request, dic);  
        
        #write logic for the request process, then return the response
        #Get user Agent and IP
        USER_AGENT = UserAgent()
        user_ip, user_agent = USER_AGENT.get_client_ip(request), USER_AGENT.get_browser_agent(request);
        #build temporary response to be handel but latter it needs to be web service call
        res =  self.requestForNewToken(app_code, mode, pid, rid, _email, _alt_email, user_ip, user_agent);
        # process for the service call and return back with the response
        dev_mode = getattr(settings, "SKIP_WEB_CALL", 'n');
        log.info('[END]- Request Completed for the re-send token email for forgot password.');
        if dev_mode == 'y':
            return self.handelResponse(request, self.webMockData());
        
        return self.handelResponse(request, res);
    
    def requestForNewToken(self, app_code, mode, pid, rid, _email, _alt_email, user_ip, user_agent):
        '''
           This will make the web-service call to send the new token mail.
           @param app_code: Application Code Where Request came from
           @param mode: The way user tries to reset the password, it might be by his own mail or by alternative email.
           @param pid: Profile Id of the user.
           @param rid: Request ID that has been previously created.
           @param _email: An Email ID, which he has registered
           @param _alt_email: AlterNative Email through which user wants the token.
           @param user_ip: Client IP
           @param user_agent: Client Agent.
           @return: A response message gets from the service call
        '''
        # for the Data Form to be sent over network
        forms = {"mode": mode, "client_meta": user_agent, "ip": user_ip, "email": _email, "alt_email":_alt_email, "pid": pid, 'rid': rid, 'app':app_code}
        data = urllib.urlencode(forms, doseq=True);
        
        # form the URL
        WEB_BASE_URL = getattr(settings, "REST_BASE_URL", None);
        WEB_BASE_URL += 'forgotPassword/re-send/mail'
        # make instance of rest client
        client = RestClient();
        return client.postWithAuthHeader(WEB_BASE_URL, data);
    
    def handelResponse(self, request, response):
        '''
           This will handle the response to be sent over network
           @param request: httpRequest 
           @param response: Response that will be sent over network.
        '''
        if(request.is_ajax()):
            return JSONResponseMixin().render_to_response(response);
        else:
            return HttpResponse(response);
        
    def webMockData(self):
        dic = {};
        dic['RESCD'] = '200';
        dic['MSG'] = 'Sent mail.';
        return dic; 
