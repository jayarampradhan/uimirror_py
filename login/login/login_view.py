import logging
import urllib
import urlparse

from django.conf import settings
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View

from login.lgn_helper import LoginHelper
from ui_utilities.destination_builder import getDestinationByAppCode


log = logging.getLogger(__name__)
class LoginView(View):
    '''
       This class will help to Serve the Login/forgot password tab based on the reference.
       This will help to authenticate as well from the post call.
       PATH VARIABLES:
           -request: A HttpRequest object which has originated the request.
           -app_code: Application code from which application request has been comes from.
        GET VARIABLES:
            -des: A destination where request will be forwarded.
            -fgp: If user want to see the forgot password tab, then this value should be populated.
            -itest: If any URL faced any issue and want to report then this will be take care by this parameter,
                    It has severity level such as 
                        0- Small Minor, user will see some internal issues, apologizes we are working on it
                        1- Minor, user will see we are working on it to get it fixed for you.
                        2- Sever, User will see, we are working fine thanks for the testing.
       LOGIC:
           GET:
              This validate the get parameter and based on the details it will show the tab.
              default tab is login
           POST:
               If user has all the valid details Then he will be requested for the authentication by the authentication system.
    '''
    
    def get(self, request, app_code):
        '''
           This will be used for any login request landing for this page.
           @param request: A HttpRequest which generate the call.
           @param app_code: Application Code where request coming from.
        '''
        log.info('[START]- Request Received for the login page.');
        destination, forgotPasswordTab, _issues , forgotPasswordSubTab = request.GET.get('des', getDestinationByAppCode(app_code)), request.GET.get('fgp'), request.GET.get('itest'), request.GET.get('fgpm');
        #Ternary operator
        #destination = destination if destination else getDestinationByAppCode(app_code);
        log.info('[END]- Request Completed for the login page.')
        return self.loginResponseMixIn(request, self.buildLoginArgs(app_code, destination, forgotPasswordTab, forgotPasswordSubTab, _issues));
    
    def buildLoginArgs(self, app_code, destination, tab, subtab, _issues):
        '''
           This will build the login parameter for the login page landing.
           @param app_code: Application From which request coming.
           @param destination: Destination where to navigate
           @param tab: Forgot Password Tab to navigate direct.
           @param subtab: Forgot Password Sub Tab
           @param _issues: In case of any issues it will show a issue list.
        '''
        dic, err_msg = {}, ''
        dic['app_code'] = app_code;
        dic['des'] = destination;
        if _issues:
            if _issues == '0' or _issues == 0:
                err_msg = 'Sorry for the inconvenience, we are working on priority to fix this for you.'
            elif _issues == '1' or _issues == 1:
                err_msg = 'OOPS!!! Something went wrong, we are working on priority to fix this for you.'
            elif _issues == '2' or _issues == 2:
                err_msg = 'We are working fine Thanks for your time to Test.'
            else:
                err_msg = 'OOPS!!! Something went wrong, we are working on priority to fix this for you.'
        
        if tab:
            dic['FORGOTPWD'] = 'Y'
            if subtab:
                dic['mode'] = subtab
            if err_msg:
                dic['FP_INVLDMSG'] = err_msg;
                
        if err_msg and not tab:
            dic['INVLDMSG'] = err_msg;
        return dic;
    
    def post(self, request, app_code):
        '''
          This will be used when login form will be submitted.
          @param request: HttpRequest for this operation
          @param app_code: Which app made this login request
        '''
        log.info('[START]- Request Received for the Authentication.');
        # First Decide Destination
        destination = request.GET.get('des', getDestinationByAppCode(app_code));
        keepmelogin = 'Y' if request.POST.get('loggedinFlag') else 'N'
        
        # Get user Agent and IP
        from useragent.determine_user_agent import UserAgent
        USER_AGENT = UserAgent()
        user_ip, user_agent = USER_AGENT.get_client_ip(request), USER_AGENT.get_browser_agent(request);
        password, user_id = request.POST.get('password', None), request.POST.get('user_id', None);
        # pwdEncApi = EncryptionUtil(self.PASSWORD_KEY);
        # password = pwdEncApi.encryptText(password)
        errors = self.validateForm(user_id, password, user_ip, destination);

        if errors:
            # add Context and return to the page
            errors['app_code'] = app_code;
            errors['des'] = destination;
            log.info('[END]- Aborting Authentication request as user has given invalid data.');
            return self.loginResponseMixIn(request, errors);
             
        # log.info('--->asasa->%s',validate_email(email))
        # forms = {"type": "cookie","client_meta": "assmjhasjhaskashkashk","ip": '127.0.0.1', "prfid": "1234", "authid": "1", "prvauthid": "1", "token": "abcde", "prvtoken": "abcde","lgnid":"1"}
        sr_response = self.authenticate(user_agent, user_ip, user_id, password, keepmelogin);
        log.info('[END]- Authentication Request Completed, taking action based on the response.');
        dev_mode = getattr(settings, "SKIP_WEB_CALL", 'n');
        if dev_mode == 'y':
            return HttpResponse('SucessFully Logged in.');
        
        return self.processResponse(request, sr_response, destination, app_code);
    
    def validateForm(self, user_id, pwd, ip, destination):
        '''
           This will validate the submitted form for a initial check before calling web service,
           so initially if any error found, it will stop the process.
           @param user_id: User Id of the user it may be email/ mobile number.
           @param pwd: Password entered by the user.
           @param ip: IP address of the user.
           @param destination: Destination URL, which might be wrong while calling
        '''
        # step 1- URL validator
        key, msg, sug = '','','';
        from django.core.exceptions import ValidationError
        from django.core.validators import URLValidator, \
        validate_ipv46_address
        try:
            url_validate = URLValidator();
            url_validate(destination);
        except ValidationError:
            log.error('Destination URL %s , user trying to access is not valid', destination);
            msg += 'You have modified original End point URL.\n';
            sug += 'We are working fine, Thanks for your Time to test.\n'
            
        # Step 2- Validate password
        if not pwd:
            log.info('User Entered Password is not correct');
            key += 'pwd, ';
            msg += 'Password is not valid. \n';
            sug += 'Please Enter a valid password. \n'
        
        # Step 3- Validate User_id
        if not self.isValideUserId(user_id):
            log.info('User Entered User Id is not correct');
            key += 'user_id, ';
            msg += 'User Id is not valid. \n';
            sug += 'Please Enter a valid User Id. \n'
        
        # Step 4- Validate IP
        try:
            validate_ipv46_address(ip);
        except ValidationError:
            log.error('IP Address %s of the user is not valid', ip);
            msg += 'OOps Something went wrong. \n';
            sug += 'Currently we are not able to determine your system details, please try after some time. \n'
            
        key = key.rstrip(', ') if key else None
        msg = key.rstrip('\n') if msg else None
        sug = key.rstrip('\n') if sug else None
        return LoginHelper().buildValidationDic(key, msg, sug);
    
    def isValideUserId(self, user_id):
        '''
           This will validate the user_id field, it might be an email id or an mobile number.
           @param user_id: User Entered User_id
           @return: true if the details are valid else false
        '''
        # First check if user id is email
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(user_id);
        except ValidationError:
            log.info('Might be User trying to authenticate using mobile number')
            try:
                if long(user_id) and not user_id.isalpha():
                    # Phone Number is not valid
                    min_length = 10
                    max_length = 13
                    ph_length = str(user_id)
                    # Finding Exact Error
                    if (len(ph_length) < min_length) or (len(ph_length) > max_length):
                        raise ValidationError('Phone number length not valid')
            except (ValueError, TypeError, ValidationError):
                log.info('Mobile Number entered by user %s, is not valid', user_id)
                return False;
        return True
    
    def authenticate(self, usr_agent, ip, usr_id, pwd, keepmelogin):
        '''
          This will call the web-service to get the user authenticated.
          @param usr_agent: User Agent of the Browser
          @param ip: IP address of the user
          @param usr_id: User ID entered by the user.
          @param pwd: Password Entered by the user.
          @param keepmelogin: Keep me login flag, checked by the user
          @return: Return the response received from Web-service
        '''
        # for the Data Form to be sent over network
        forms = {"type": "form", "client_meta": usr_agent, "ip": ip, "user_id": usr_id, "pwd": pwd, "keepmelogin": keepmelogin, "id_type":self.getTypeOfUserId(usr_id)}
        data = urllib.urlencode(forms, doseq=True);
        
        # form the URL
        WEB_BASE_URL = getattr(settings, "REST_BASE_URL", None);
        WEB_BASE_URL += 'auth'
        # make instance of rest client
        from ui_utilities.http_api import RestClient
        client = RestClient();
        return client.postWithAuthHeader(WEB_BASE_URL, data);
    
    def getTypeOfUserId(self, user_id):   
        '''
           This will get type of the user login id, it might be email or mobile number
           @param user_id: User ID entered by the user.
        '''         
        try:
            long(user_id)
            return 'M';
        except ValueError:
            return 'E';
    
    
    
    def processResponse(self, request, sr_response, destination, app_code):
        '''
          Builds the response object for the next step of action.
          @param request: HttpRequest object 
          @param sr_response: Response Received from WEB-Service call
          @param destination: Destination End point where Request will be navigated.
          @param app_code: Application Code Trying To access
        '''
        from ui_utilities.dsutilities import DSUtility
        res_code, res_msg = DSUtility().getlistitem(sr_response, 'RESCD'), DSUtility().getlistitem(sr_response, 'MSG');
        errors = {};
        if res_code == "200":
            url = urlparse.urlparse(destination);
            query = urlparse.parse_qs(url.query)
            from lgn_helper import buildAuthenticateParam
            if query:
                destination += ("&%s" %(buildAuthenticateParam(res_msg)));
            else:
                destination += ("?%s" %(buildAuthenticateParam(res_msg)));
            log.debug('final destination end point %s', destination);
            return HttpResponseRedirect(destination);
        else:
            if res_code == "406":
                # Invalid Field
                errors = LoginHelper().buildValidationDic(DSUtility().getlistitem(res_msg, 'INVLDKEY'), DSUtility().getlistitem(res_msg, 'INVLDMSG'), DSUtility().getlistitem(res_msg, 'INVLDSUG'));
            elif res_code == "400":
                # Web service didn't receive any input
                errors = LoginHelper().buildValidationDic(None, 'OOps provided data is not sufficient.', 'Please check with the entered data and try again.');
            else:
                # in case of internal server error.
                errors = LoginHelper().buildValidationDic(None, 'OOps, Something went wrong, we are working on it.', 'Please check with us again after sometime, apologies for the inconvenience.');
            errors['app_code'] = app_code;
            errors['des'] = destination;
            return self.loginResponseMixIn(request, errors);
        
        
    def loginResponseMixIn(self, request, dic={}):
        '''
           Common Redirect point for the login page
        '''
        context = RequestContext(request, dic)
        return render_to_response('login/login.html', context)
    
if __name__ == '__main__':
    pass
