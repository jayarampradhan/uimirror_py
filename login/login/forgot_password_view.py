import logging
import urllib

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from forgot_password_helper import buildChangePasswordGetArguments
from lgn_helper import buildLoginGetArguments
from login.forgot_password_helper import ForGotPasswordHelper
from ui_utilities.dsutilities import DSUtility

log = logging.getLogger(__name__)

class ForGotPassword(View):
    '''
       This class will help to request for the creating a request for password change by the different options selected 
       by the user like, user can reset password by the registered email or by alternative email and most recent password.
       PATH VARIABLES:
           -request: A HttpRequest object which has originated the request.
           -app_code: Application code from which application request has been comes from.
        GET VARIABLES:
            -des: A destination to which it will be redirected back in case request completed successfully.
       LOGIC:
           GET:
               It always redirect to login page forgot password tab, to request for initiating reset password page.
               
           POST:
               Once User has been selected and key the required information, it will create a request for password change 
               and navigate to the change password screen, else user will be stay at the same page.
               If any suspicious activity detected, then user will be navigated to the login page.
    '''
    def get(self, request, app_code):
        '''
           A get request to this will always redirect to login page with the error code and details.
           @param app_code: Application code from where request has been generated.
           @return: A login page with the forgot password page opened.
        '''
        log.info('[START]-Request Received for Forgot Password.');
        destination = request.GET.get('des');
        log.info('[END]-Served the the login page with forgot password tab enabled.');
        return redirect('%s?%s' % (reverse('uim.login', kwargs={'app_code':app_code}), buildLoginGetArguments(destination, 'y')))
    
    def post(self, request, app_code):
        '''
           In case user has forgot the password or his account has been hacked including email account,
           he will key in the email/email he has access or most recent password in case account has been hacked.
           @param request: HttpRequest for this web flow.
           @param app_code: Appcode From which user is tying to access.
           @return: if all the details input by the user is correct then he will be navigate to the change password
                    screen, else he will be stay back at the same page with the error details.
        '''
        log.info('[START]-Requesting for the forgot password process to be started to navigate to the change password page.');
        destination, _reset_option = request.GET.get('des'), request.POST.get('preoption');
        _recent_pwd, _alt_email = '', '';
        if _reset_option == '1' or _reset_option == 1:
            _email = request.POST.get('uimSignedUpEmail');
        elif _reset_option == '2' or _reset_option == 2:
            _email, _alt_email, _recent_pwd = request.POST.get('uimEmail'), request.POST.get('uimResetEmailAccessTo'), request.POST.get('uimRecentPwd');
        
        # Get user Agent and IP
        from useragent.determine_user_agent import UserAgent
        USER_AGENT = UserAgent()
        user_ip, user_agent = USER_AGENT.get_client_ip(request), USER_AGENT.get_browser_agent(request);

        # validate the user submitted form
        errors = self.validateForm(_email, _alt_email, _recent_pwd, _reset_option);
        if errors:
            # add Context and return to the page
            log.info('[END]-As the inputs are not valid asking user to re input the details.');
            return self.stayAtSamePage(request , self.buildErrorMap(app_code, destination, _reset_option, errors))
        
        # process for the service call and return back with the response
        dev_mode = getattr(settings, "SKIP_WEB_CALL", 'n');
        if dev_mode == 'y':
            # TODO: Webmock Method Delete on production ready
            sr_response = self.buildWebMockData();
        else:
            sr_response = self.forgotPassword(user_agent, user_ip, _email, _alt_email, _recent_pwd, _reset_option, destination);
        
        log.info('[END]-Forgot Password request Completed, processing the response received from web call.');
        return self.processResponse(request, sr_response, destination, app_code, _reset_option, _email, _alt_email);
    
    def validateForm(self, _email, _alt_email, _recent_pwd, mode):
        '''
           This will validate the submitted form for a initial check before calling web service,
           so initially if any error found, it will stop the process.
           @param email: Email Id, which has been used for signup /id he has access to get the verification mail.
           @param _alt_email: If user trying to reset through other's email, then its goes to this field.
           @param _recent_pwd: Most Recent Password he has been used in case he has lost access.
           @param mode: mode might be 1 or 2, 1 means reseting by his own mail, 2 means reseting by other email.
           @return: errors if found else none
        '''
        key, msg, sug = '','','';
        
        # Step 1- Validate EMail
        try:
            validate_email(_email);
        except ValidationError:
            msg += 'Email Is Not Valid. \n';
            sug += 'Key In the correct email. \n';
            if mode == '1' or mode == 1:
                key += 'signedUpEmail, ';
            else:
                key += 'uimEmail, ';
        
        # Step 2- Check for the mode and if mode 2 then password should present
        if (mode == '2' or mode == 2) and not _recent_pwd:
            key += 'recentPwd, ';
            msg += 'Invalid Password. \n';
            sug += 'Key In Recent Password. \n';
        
        # Step 3- Check for the mode if mode 2 and uimirror email not present then return with error
        if mode == '2' or mode == 2:
            try:
                validate_email(_alt_email);
            except ValidationError:
                key += 'alterNativeEmail, ';
                msg += 'AlterNative Email Is Not Valid. \n';
                sug += 'Key In the correct AlterNative email. \n';
                
        key = key.rstrip(', ') if key else None
        msg = key.rstrip('\n') if msg else None
        sug = key.rstrip('\n') if sug else None
        return ForGotPasswordHelper().buildValidationDic(key, msg, sug);
    
    def forgotPassword(self, user_agent, ip, _email, _alt_email, _recent_pwd, _reset_option, destination):
        '''
          This will call the web-service to get the Password Reseted.
          @param usr_agent: User Agent of the Browser
          @param ip: IP address of the user
          @param email: Email Id, which has been used for signup /id he has access to get the verification mail.
          @param _alt_email: Email Id, he has access to get the verification mail.
          @param _recent_pwd: Most Recent Password he has been used in case he has lost access.
          @param _reset_option: mode might be 1 or 2, 1 means reseting by his own mail, 2 means reseting by other email.
          @param destination: A destination where user will be navigated back once validated.
          @return: Return the response received from Web-service
        '''
        # for the Data Form to be sent over network
        forms = {"mode": _reset_option, "client_meta": user_agent, "ip": ip, "email": _email, "alt_email":_alt_email, "pwd": _recent_pwd, 'des': destination}
        data = urllib.urlencode(forms, doseq=True);
        
        # form the URL
        WEB_BASE_URL = getattr(settings, "REST_BASE_URL", None);
        WEB_BASE_URL += 'forgotPassword'
        # make instance of rest client
        from ui_utilities.http_api import RestClient
        client = RestClient();
        return client.postWithAuthHeader(WEB_BASE_URL, data);
    
    def processResponse(self, request, sr_response, destination, app_code, _reset_option, _email, _alt_email):
        '''
           This will parse the response received from the web service call.
           This will show the new password page if user entered details are valid else return back to the same screen with error message.
           @param request: A HttpRequest object.
           @param sr_response: Response Received from the web service call.
           @param destination: Destination User will be redirect after successful password reset.
           @param app_code: Appcode user is trying to access.
           @param _reset_option: Reseting the password by which way like by own email, alternative email etc.
           @param _email: Registered Email Id.
           @param _alt_email: Alternative Email Id.
           @return: success response to key in the new password or return to the same screen. 
        '''
        log.debug('Response Received for the forgot password request {}',sr_response);
        res_code, res_msg = DSUtility().getlistitem(sr_response, 'RESCD'), DSUtility().getlistitem(sr_response, 'MSG');
        
        if res_code == "200":
            log.info('[END]- Forgot password request is accepted and redirecting to the change password page');
            return self.redirectToNextView(res_msg, app_code, destination, _reset_option, _email, _alt_email);
        else:
            if res_code == "406":
                # Invalid Field
                errors = ForGotPasswordHelper().buildValidationDic(DSUtility().getlistitem(res_msg, 'INVLDKEY'), DSUtility().getlistitem(res_msg, 'INVLDMSG'), DSUtility().getlistitem(res_msg, 'INVLDSUG'));
            elif res_code == "400":
                # Web service didn't receive any input
                errors = ForGotPasswordHelper().buildValidationDic(None, 'OOps provided data is not sufficient.', 'Please check with the entered data and try again.');
            else:
                # in case of internal server error.
                errors = ForGotPasswordHelper().buildValidationDic(None, 'OOps, Something went wrong, we are working on it.', 'Please check with us again after sometime, apologies for the inconvenience.');

            return self.stayAtSamePage(request , self.buildErrorMap(app_code, destination, _reset_option, errors))
        
    def redirectToNextView(self, res_msg, app_code, destination, _reset_option, _email, _alt_email):
        '''
           This will build the data for the next view and redirect to the new password page.
           @param res_msg: Response Received from the webservice call
           @param app_code: Application from which request is originated.
           @param destination: Destination User will be redirect after successful password reset.
           @param _reset_option: Reseting the password by which way like by own email, alternative email etc.
           @param _email: Regsitered Email Id.
           @param _alt_email: Alternative Email Id.
           @return: Redirect to the password reset page.
        '''
        dic = {};
        dic['app_code'] = app_code;
        dic['pid'] = DSUtility().getlistitem(res_msg, 'pid');
        dic['rid'] = DSUtility().getlistitem(res_msg, 'rid');
        dic['mode'] = _reset_option;

        return redirect('%s?%s' % (reverse('uim.change.password', kwargs=dic)
                                       , buildChangePasswordGetArguments(email = _email, des = destination, src = 'form', alt_email = _alt_email)))
    
    def buildErrorMap(self, app_code, destination, _reset_option='1', errors={}):
        '''
           A common Helper which will add the necessary details to the exiting dictionary for same page stop navigation.
           @param app_code: Application from which request is originated.
           @param destination: Destination User will be redirect after successful password reset.
           @param _reset_option: Reseting the password by which way like by own email, alternative email etc.
           @param errors: A pre-populated dictionary or a empty dictionary.
           @return: Updated dictionary that will be send back to the UI.
        '''
        errors['app_code'] = app_code;
        errors['des'] = destination;
        errors['FORGOTPWD'] = 'Y';
        errors['mode'] = _reset_option;
        return errors;
    
    def stayAtSamePage(self, request, dic={}):
        '''
           This will be redirecting to the same page, where error has been generated, with the error details,
           so that user can rectify the error and re submit the form.
           @param request: HttpRequest which has initiated this call.
           @param dic: A attribute List which will be followed 
        '''
        context = RequestContext(request,dic)
        return render_to_response('login/login.html', context)
    
    
    def buildWebMockData(self):
        '''
           This builds the sample test data to work in eb flow with out web service.
        '''
        rs_msg = {};
        rs_msg['pid'] = '1234';
        rs_msg['rid'] = '1';
        rs = {}
        rs['RESCD'] = "200";
        rs['MSG'] = rs_msg; 
        return rs;
        
