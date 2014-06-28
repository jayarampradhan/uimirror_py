from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from ui_utilities.dsutilities import DSUtility
from useragent.determine_user_agent import UserAgent
import logging

log = logging.getLogger(__name__)
    
class VerifyView(View):
    '''
       This will be responsible to Verify the User who is recently registered.
       It has get method to show the screen and post call responsible for verify the registration.
       PATH VARIABLES:
           -request: A HttpRequest object which has originated the request.
           -tpid: A temporary created profile id of the user.
        GET VARIABLES:
            -em: Email Id that has been used for the register process.
            -src: It specifies either request from email or form.
            -des: After Verification Where It will be navigated
            -app: Application Code
       LOGIC:
           GET:
               It first look into the get parameter, and if the request came from the web form, then it will render the verify page.
               else it will do process the verification process and redirect to the next view i.e complete the information page.
               if any of the get parameters are not present then it will be redirected to the register page, with exception details.
               If user has clicked the link from the email, it will validate the token sent, if the token is not a active one(i.e already used)
               It will check for the next screen as first step if that is also completed will be redirected to the destination directly.
               if destination is not known it will redirect to the home page of the app code else default to social.
           POST:
               Once User has key in the token details it will go for the validation and permanently register the user.
               If the user entered token already used via link one, then it will redirect to the destination or app home page or default to social.
    '''
    def get(self, request, tpid):
        '''
           This will be used for any Verification request landing for this page.
           Verification form page will be handled by this.
           @param request: HttpRequest of client
           @param tpid: Profile Id created for this user.
        '''
        log.info('[START]- Request Received For the Verification Process.')
        email, source, destination, token, app = request.GET.get('em', None), request.GET.get('src', 'email'), request.GET.get('des', None), request.GET.get('dt', None), request.GET.get('app', '1')
        if token and email:
            #Process the link verification
            log.info('[INTERIM]- Serving Request for verification through email link.');
            USER_AGENT = UserAgent()
            ip, client_meta = USER_AGENT.get_client_ip(request), USER_AGENT.get_browser_agent(request);
            return self.processVerifiCation(self, token, tpid, source, ip, client_meta, request, email, app, destination)  
        elif email and not token:
            log.info('[END]- Request For Verification process assumes, user will key in the token so returning him to the tokn page.')
            return self.renderPage(tpid, email, 'form', app, destination, request);
        else:
            # As no creteria match for the account verification redirect back to the register screen to register again
            #Redirect to the register page
            log.info('[END]- Request For Verification can\'t determine the process to take, so redirecting to register page.')
            return self.redirectToRegister(app, destination, '2');
        
    def renderPage(self, tempProfileId, email, source, app, destination, request, _errors = {}):
        '''
           This will render the request of verify page screen. If there is no error user will be rendered with the required 
           details map.
           @param tempProfileId: Temporarily Profile Id of the user.
           @param email: Email Id which was user's registered email.
           @param source:  Source from where page rendering request comes from.
           @param request: An HttpRequest which generated this call
           @param app: Application Code
           @param destination: Destination URL.
           @param _errors: if it has any error it will render.
           @return: response for the verify 
        '''
        from ui_utilities.verify_helper import buildVerifyPageContext
        _data = buildVerifyPageContext(tempProfileId, email, source, app, destination, _errors);
        context = RequestContext(request,_data);
        response = render_to_response('verify/verify_user.html', context)
        return response
        
    
    def redirectToRegister(self, app = None, destination = None, issues = None):
        '''
           This will redirect to the register page assuming something issue happened.
           @param app: Application Code where request has been generated.
           @param destination: A destination where it will be navigated. 
        '''
        from ui_utilities.reg_helper import buildRegisterViewGetArguments
        if (app and destination and issues) or (app and destination) or (app and issues):
            return redirect('%s?%s' % (reverse('uim.register.create.with.path.app'
                                               , kwargs={'app_code':app}), buildRegisterViewGetArguments(destination, issues)));
        elif (destination and issues) or issues:
            return redirect('%s?%s' % (reverse('uim.register.create.home'), buildRegisterViewGetArguments(destination, issues)));
    
    def post(self, request, tpid):
        '''
           This will be used for the verification process from the form by using token.
           The required attributes are profile id, token, user_ip, clinet_meta, app_code and destination
           @param request: HttpRequest of client
           @param tpid: Profile Id created for this user.
           
        '''
        log.info('[START]- Verifying the token submitted from the verify screen for user verifications.')
        #populate User submitted form in a map
        email, token, destination, app = request.GET.get('em', None), request.POST.get('token', None), request.GET.get('des', None), request.GET.get('app', '1');
        source = 'form';
        if not token:
            #add Context and return to the page
            log.info('[END]- Some Entered details are invalid so sending user the warnings and error to rectify.')
            from ui_utilities.dic_builder import buildValidationErrorDic
            errors = buildValidationErrorDic('token', 'Entered Token is not valid!!!', 'Please enter the token you received in your mail.');
            return self.renderPage(tpid, email, source, app, destination, request, errors);
        log.info('[INTERIM]- Verifying the token submitted from the verify screen for user verifications.')
        USER_AGENT = UserAgent()
        ip, client_meta = USER_AGENT.get_client_ip(request), USER_AGENT.get_browser_agent(request);
        return self.processVerifiCation(token, tpid, source, ip, client_meta, request, email, app, destination);
    
    def processVerifiCation(self, token, tpid, source, ip, client_meta, request, email, app, destination):
        '''
           This will handle the verification process.
               -First form the form
               -validate the form
               -Make web call
               -parse response
        '''
        form = self.buildVerifyForm(token, tpid, source, ip, client_meta);
        response = self.verifyForm(form)
        dev_mode = getattr(settings, "SKIP_WEB_CALL", 'n');
        if dev_mode == 'y':
            # TODO: Remove This on production
            response = self.buildWebMockData()
        return self.parseResponse(response, source, token, tpid, email, request, app, destination);
        
    def parseResponse(self, sr_response, source, token, tpid, email, request, app, destination):
        '''
           This will parse the response received from the web call and do the necessary re routing.
        '''
        res_code = DSUtility().getlistitem(sr_response, 'RESCD');
        if res_code == "200" or res_code == 200:
            res_msg = DSUtility().getlistitem(sr_response, 'MSG');
            #Verification success possibly redirect to the destination or login page
            self.handelSucessResponse(res_msg);
        elif res_code == "406" or res_code == 406:
            #Invalid Field
            #check source if it is form then send him back to re enter the token, else send him to the register page saying we are working fine
            if source == 'form':
                return self.renderPage(tpid, email, source, app, destination, request);
            else:
                return self.redirectToRegister(app, destination, '1');
                
        elif res_code == "400" or res_code == 400:
            # redirect User to the register screen saying we are working to fix it
            #Web service didn't receive any input
            return self.redirectToRegister(app, destination, '1');
        elif res_code == "440" or res_code == 440:
            #Token Already Used
            # redirect User to the login page with the destination
            self.redirectToLoginPage(app, destination, '2');
        else:
            # If Response Was not obvious: redirect User to the register screen saying we are working to fix it
            return self.redirectToRegister(app, destination, '1');
    
    def buildVerifyForm(self, token, tpid, source, ip, client_meta):
        '''
           This builds the map that will be sent to web service call to handle the verification process.
           All the parameters shouldn't be empty or None
           @param token: Token sent to the user
           @param tpid: Temporary Profile ID created by the user.
           @param source: Source from where request is orginated.
           @param ip: IP Address of the user
           @param client_meta: User Browser Details.
           @return: A Dictionary with the necessary map details. 
        '''
        form = {};
        form["prfid"] = tpid;
        form["src"] = source;
        form["token"] = token;
        form["ip"] = ip;
        form["client_meta"] = client_meta; 
        return form;
        
    
    def verifyForm(self, form):
        '''
           This will verify email user by calling the service.
           @param request: HttpRequest object submitted by user.
           @param form: Register form submitted by user.
        '''
        WEB_BASE_URL = getattr(settings, "REST_BASE_URL", None);
        WEB_BASE_URL += 'verify';
        import urllib
        data = urllib.urlencode(form, doseq=True);
        #make instance of rest client
        from ui_utilities.http_api import RestClient
        client = RestClient();
        return client.postWithAuthHeader(WEB_BASE_URL, data);
    
    def redirectToLoginPage(self, app_code, destination = None, _issues = None):
        '''
           This will redirect to login page, when ever it sees any issues or any suspicious activity happened.
           @param app_code: Application code from which the request has been landing here
           @param destination: Destination Endpoint to keep track of.
           @return: The login page and error message on that. 
        '''
        from ui_utilities.lgn_helper import buildLoginGetArguments
        return redirect('%s?%s' % (reverse('uim.login', kwargs={'app_code':app_code}), buildLoginGetArguments(destination, _issues)))
    
    def handelSucessResponse(self, response):
        '''
           This will handle the success response received from the WEB call.
        '''
        profile_id =  DSUtility().getlistitem(response, 'prfid');
        app_code = DSUtility().getlistitem(response, 'app');
        destination = DSUtility().getlistitem(response, 'des');
        auth_rs = DSUtility().getlistitem(response, 'auth');
        if auth_rs:
            self.logSession(auth_rs, profile_id);
            # TODO: Redirect To the next View
        else:
            self.redirectToLoginPage(app_code, destination);

    def logSession(self, auth_rs, profileId):
        '''
           This will save the temporary session details to the cookie.
        '''
        from encryption.uiencrypt import EncryptionUtil
        auth_id = DSUtility().getlistitem(auth_rs, 'authid');
        authIdApi = EncryptionUtil(getattr(settings, "PRV_ENC_KEY", None));
        auth_id = authIdApi.encryptText(auth_id);
        #Second Prev AUth ID
        prv_auth_id =  DSUtility().getlistitem(auth_rs, 'prvauthid');
        prv_auth_id = authIdApi.encryptText(prv_auth_id);

        #3 Token
        token = DSUtility().getlistitem(auth_rs, 'token');
        token = authIdApi.encryptText(token);
        #4 Prev Token
        prv_token = DSUtility().getlistitem(auth_rs, 'prvtoken');
        prv_token = authIdApi.encryptText(prv_token);
        #5 Profile ID
        prf_id = authIdApi.encryptText(profileId);
        #set into cookie and return
        response = HttpResponseRedirect(reverse('account.uiwelcome'))
        time_out = DSUtility().getlistitem(auth_rs, 'interval');
        from account.constant import Constants
        response.set_cookie(Constants.AUTH_ID, auth_id, max_age=time_out, httponly=True)
        response.set_cookie(Constants.PREV_AUTH_ID, prv_auth_id, max_age=time_out, httponly=True)
        response.set_cookie(Constants.TOKEN, token, max_age=time_out, httponly=True)
        response.set_cookie(Constants.PREV_TOKEN, prv_token, max_age=time_out, httponly=True)
        response.set_cookie(Constants.PRF_ID, prf_id, max_age=time_out, httponly=True)
        
    def buildWebMockData(self):
        '''
           This builds the sample test data to work in eb flow with out web service.
        '''
        rs_msg = {};
        rs_msg['prfid'] = '1234';
        rs_msg['app'] = '1';
        rs_msg['des'] = 'http://uimirror.com';
        rs = {}
        rs['RESCD'] = "200";
        rs['MSG'] = rs_msg; 
        return rs;
            
if __name__ == '__main__':
    pass
