import logging
import urllib
import urlparse

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator, validate_email
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.views.generic.base import View

from dic_builder import buildValidationErrorDic
from encryption.uiencrypt import EncryptionUtil
from lgn_helper import buildLoginGetArguments
from ui_utilities.dsutilities import DSUtility
from ui_utilities.http_api import RestClient
from useragent.determine_user_agent import UserAgent


log = logging.getLogger(__name__)
class ChangePassword(View):
    '''
       This will be responsible to Change The password screen and handling all the call to the path changepassword/.
       It has get method to show the screen and post call responsible for the changing the password.
       PATH VARIABLES:
           -request: A HttpRequest object which has originated the request.
           -app_code: Application code from which application request has been comes from.
           -mode: In which way user trying to reset the password, it might be 1 for using signed off mail or 2 if 
                   His email account hacked and trying to reset from alternative mail ID.
           -pid: Profile Id of the user, when request lands to the page, it assumes that forgot password process has been initiated.
           -rid: Request ID of the forgot password process for the token validation.
        GET VARIABLES:
            -em: Email id of the user
            -src: Source from which this request has been come from possible values are form or email
            -aem: Alternative Email ID, if in case user trying to reset the password via other email ID.
            -token: A pre-populated token, in case user is trying to access this page from the email link.
            -des: A destination to which it will be redirected back in case request completed successfully.
       LOGIC:
           GET:
               It first checks the required GET parameters if it is present then it will render the change password screen to the user.
               So that user can key in his new password details and click on reset password, which will invoke the POST call.
               In the process of serving the file, if it some how feels a suspicious activity then it will be redirect to the login page forgot password tab.
               
           POST:
               Once User has key in his new password, confirm password, then it will validated along with the token, source with request ID and process continues 
               to reset the password.
    '''
    
    def get(self, request, app_code, mode, pid, rid):
        '''
           This will handel the change password request made by the user in get url.
           it will be redirect to the login page as we will not be handleing get request for this.
           If all the required parameter are not available then it will redirect to login pgae of forget passowrd tab.
           minimum required attributes are:
               -email
               -Destination
        '''
        log.info('[START]-Request Received for Change password Page.');
     
        destination, source, _email, _alt_email, token  = request.GET.get('des'), request.GET.get('src'), request.GET.get('em'), request.GET.get('aem'), request.GET.get('token', None);
        if not _email or not destination or (mode == '2' and not _alt_email):
            #do navigation to login page
            log.info('[END]- As sufficient attributes are not provided navigating back to the login screen of the forgot password tab.')
            return self.redirectToLoginPage(app_code, destination); 
        
        dic = self.buildResetPageMap(app_code, destination, _email, _alt_email, mode, pid, rid, token, source)
        context = RequestContext(request, dic);
        log.info('[END]-Request completed for the rendering the change password screen.');
        return render_to_response('forgotpassword/reset.html', context)
    
    def post(self, request, app_code, mode, pid, rid):
        '''
           This will be a post request to re-send the email with link and token for password reset request.
           @param request: A HttpRequest object
           @param app_code: Application from which request intiated
           @param mode: Reset mode 1, for by own registered mail or 2 for by other alternative mail.
           @param pid: Profile Id of the user.
           @param rid: A Valid Request open ID.
           @return: A response message saying delivered link or not.
        '''
        log.info('[START]-Request Received for Change password.');
        destination, _email, _alt_email = request.GET.get('des'), request.GET.get('em'), request.GET.get('aem');
        # If request is not valid stop the request processing
        if not destination or not _email or (mode == '2' and not _alt_email):
            log.error("[END]-Invalid request received for password Change.");
            return self.redirectToLoginPage(app_code, destination);  
        # Get user Agent and IP
        USER_AGENT = UserAgent()
        user_ip, user_agent = USER_AGENT.get_client_ip(request), USER_AGENT.get_browser_agent(request);
        
        # get the form data
        newPassword, confirmPassword, token, source = request.POST.get('newPassword'), request.POST.get('confirmPassword'), request.POST.get('token'), request.POST.get('src');
        useAsNewUidFlag = ''
        if mode == '2':
            useAsNewUidFlag = request.POST.get('useAsNewUidFlag');

        # validate the user submitted form
        errors = self.validateForm(_alt_email, newPassword, confirmPassword, token, source, pid, rid, useAsNewUidFlag, mode, user_ip, destination, app_code);
        if errors:
            # add Context and return to the page
            log.info('[END]- As Validation Failed Returning to correct input in change password screen.')
            return self.restPasswordMixIn(request, self.buildResetPageMap(app_code, destination, _email, _alt_email, mode, pid, rid, token, source, errors));
        
        # process for the service call and return back with the response
        dev_mode = getattr(settings, "SKIP_WEB_CALL", 'n');
        if dev_mode == 'y':
            # Dummy take help latter
            return HttpResponse('Password Successfully changed.');
        else:
            sr_response = self.changePassword(user_agent, user_ip, _email, _alt_email, useAsNewUidFlag, pid, rid, source, app_code, newPassword, mode);
        log.info('[END]-Request completed for the Change Password.');
        return self.processResponse(request, sr_response, destination, app_code, mode, _email, _alt_email);
    
    def validateForm(self, _alt_email, newPassword, confirmPassword, token, source, pid, rid, useAsNewUidFlag, mode, user_ip, destination, app_code):
        '''
           This will validate the submitted form for a initial check before calling web service,
           so initially if any error found, it will stop the process.
           @param _alt_email: If user trying to reset through other's email, then its goes to this field.
           @param newPassword: User Typed New Password.
           @param confirmPassword: User Typed Confirmed Password.
           @param token: Token Issued To reset the password.
           @param source: Source From which Reset Password Invoking.
           @param pid: Profile Id Of the user.
           @param rid: Request Id That has been generated by the call of forgot password.
           @param useAsNewUidFlag: In case User Want to use the alternative mail as his User Id.
           @param mode: Channel of reseting the password, via registered Email or alternative mail.
           @param ip: IP address of the user.
           @param destination: Destination URL, which might be wrong while calling
           @param app_code: Application from which request comes from.
           @return: errors if found else none
        '''
        key, msg, sug = '','','';
        # step 1- URL validator
        try:
            url_validate = URLValidator();
            url_validate(destination);
        except ValidationError:
            log.error('Destination URL %s , user trying to access is not valid', destination);
            msg += 'You have modified original End point URL. \n';
            sug += 'We are working fine, Thanks for your time to test. \n'
            
        # Step 2- Validate AlterNative EMail if useAsNewUidFlag is marked
        if useAsNewUidFlag == 'y' and (mode == '2' or mode == 2):
            try:
                validate_email(_alt_email);
            except ValidationError:
                log.info('AlterNative Email ID is not valid.')
                msg += 'Don\'t modified Alternative Email. \n';
                sug += 'We are working fine, Thanks for your time to test. \n'
        
        # Step 3- Check the new password and match with confirm one
        if not newPassword or not confirmPassword:
            log.error('New/Confirm Password Enter by the user is invalid.')
            key += 'pwd, confirmPassword, ';
            msg += 'Invalid Password. \n';
            sug += 'Key In Correct Password and re type to match. \n'
        
        if newPassword != confirmPassword:
            log.error('New/Confirm Password Not Matching.')
            key += 'pwd, confirmPassword, ';
            msg += 'Invalid Password. \n';
            sug += 'Key In Correct Password and re type to match. \n'
        
        # Step 4- Check for token
        if not token and source == 'email':
            log.error('User Trying to change password from the email link, but details are missing like token.')
            return self.redirectToLoginPage(app_code, destination, mode);
        elif not token and source == 'form':
            log.error('New/Confirm Password Not Matching.')
            key += 'token, ';
            msg += 'Invalid Token. \n';
            sug += 'Key In Correct Token You got in your Mail In-box. \n'
        
        key = key.rstrip(', ') if key else None
        msg = key.rstrip('\n') if msg else None
        sug = key.rstrip('\n') if sug else None    
        return buildValidationErrorDic(key, msg, sug);
    
    def changePassword(self, user_agent, ip, _email, _alt_email, useAsNewUidFlag, pid, rid, source, app_code, password, mode):
        '''
          This will call the web-service to get the Password Reseted.
          @param usr_agent: User Agent of the Browser
          @param ip: IP address of the user
          @param _email: Email Id, which has been used for signup /id he has access to get the verification mail.
          @param _alt_email: Email Id, he has access to get the verification mail.
          @param useAsNewUidFlag: If User want to use alternative email as primary login id.
          @param pid: profile id Of the user.
          @param rid: request Id for this change password.
          @param source: Source through which change password approved.
          @param app_code: Application code from which its initiated.
          @param password: New Password.
          @param mode: Which mode user tried to reseting the password.
          @return: Return the response received from Web-service
        '''
        # for the Data Form to be sent over network
        forms = {"mode": mode, "client_meta": user_agent, "ip": ip, "email": _email, "alt_email":_alt_email, "pwd": password,
                 "change_new_uid_flag": useAsNewUidFlag, "pid":pid, "rid": rid, "source": source}
        data = urllib.urlencode(forms, doseq=True);
        
        # form the URL
        WEB_BASE_URL = getattr(settings, "REST_BASE_URL", None);
        WEB_BASE_URL += 'changepassword'
        # make instance of rest client
        client = RestClient();
        return client.postWithAuthHeader(WEB_BASE_URL, data);
    
    def processResponse(self, request, sr_response, destination, app_code, _email, _alt_email, mode, pid, rid, token, source):
        '''
           This will parse the response received from the web service call.
           This will show the new password page if user entered details are valid else return back to the same screen with error message.
           @param request: A HttpRequest Made for this web flow.
           @param sr_response: Response Received from the web service call.
           @param destination: Destination User will be redirect after successful password reset.
           @param app_code: Appcode user is trying to access.
           @param _email: Registered Email Id.
           @param _alt_email: Alternative Email Id.
           @param mode: Mode Of the password Reset.
           @param pid: profile Id Of the user.
           @param rid: Request Id Of the request for forgot password.
           @param token: Token Issued to the user.
           @param source: Source In which user try to use the token.
           @return: success response to key in the new password or return to the same screen. 
        '''
        res_code = DSUtility().getlistitem(sr_response, 'RESCD');
        res_msg = DSUtility().getlistitem(sr_response, 'MSG');
        errors = {};
        if res_code == "200":
            log.info('[END]Password has been successfully changed, redirecting to the next view requested for.');
            return self.redirectToNextView(res_msg, destination);
        else:
            if res_code == "406":
                # Invalid Field
                errors = buildValidationErrorDic(DSUtility().getlistitem(res_msg, 'INVLDKEY'), DSUtility().getlistitem(res_msg, 'INVLDMSG'), DSUtility().getlistitem(res_msg, 'INVLDSUG'));
            elif res_code == "400":
                # Web service didn't receive any input
                errors = buildValidationErrorDic(None, 'OOps provided data is not sufficient.', 'Please check with the entered data and try again.');
            else:
                # in case of internal server error.
                errors = buildValidationErrorDic(None, 'OOps, Something went wrong, we are working on it.', 'Please check with us again after sometime, apologies for the inconvenience.');
            
            return self.restPasswordMixIn(request, self.buildResetPageMap(app_code, destination, _email, _alt_email, mode, pid, rid, token, source, errors));
    
    # work pending    
    def redirectToNextView(self, res_msg, destination = None):
        '''
           This will build the data for the next view and redirect to the new password page.
           @param res_msg: Response Received from the webservice call
           @param destination: Destination User will be redirect after successful password reset.
           @return: Redirect to the Destination URL.
        '''
        destination = destination if destination else DSUtility().getlistitem(res_msg, 'DESTINATION');
        url = urlparse.urlparse(destination);
        query = urlparse.parse_qs(url.query)
        from lgn_helper import buildAuthenticateParam
        if query:
            destination += ("&%s" %(buildAuthenticateParam(res_msg)));
        else:
            destination += ("?%s" %(buildAuthenticateParam(res_msg)));
        log.debug('final destination end point %s', destination);
        return HttpResponseRedirect(destination);
        
    
    def buildResetPageMap(self, appCode, destination, _email, _alt_email, _reset_option, pid, rid, token, source, _rq = {}):
        '''
           Builds the map which will be send back to the Reset Page, in case of any error
           @param app_code: Application Code
           @param destination: Destination to be redirected back
           @param _email: Email Id of the user
           @param _alt_email: Alternative Email Id
           @param _reset_option: Mode of reseting password
           @param pid: Profile Id of the user.
           @param rid: Request Issued Token.
           @param token: Token transfered via Email.
           @param source: Source where change password is generated.  
        '''
        if appCode:
            _rq['app_code'] = appCode;
        if destination:
            _rq['des'] = destination;
        if _email:
            _rq['email'] = _email;
        if _alt_email:
            _rq['alt_email'] = _alt_email;
        if _reset_option:
            _rq['mode'] = _reset_option;
        if pid:
            _rq['pid'] = pid;
        if rid:
            _rq['rid'] = rid;
        if token:
            _rq['token'] = token;
        if source:
            _rq['src'] = source;
        return _rq; 
        
    
    def restPasswordMixIn(self, request, dic={}):
        '''
           Common Redirect point for the Reset page
        '''
        context = RequestContext(request, dic)
        return render_to_response('forgotpassword/reset.html', context)
    
    def redirectToLoginPage(self, app_code, destination = None, mode = '1'):
        '''
           This will redirect to login page, when ever it sees any issues or any suspicious activity happened.
           @param app_code: Application code from which the request has been landing here
           @param destination: Destination Endpoint to keep track of.
           @return: The login page with forgot password tab selected and error message on that. 
        '''
        mode = '1' if not mode else mode;
        return redirect('%s?%s' % (reverse('uim.login', kwargs={'app_code':app_code}), buildLoginGetArguments(destination, 'y', sub_tab= mode, _issues = '2')))
