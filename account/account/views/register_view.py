from account.reg_helper import prepareRegisterPageContext
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from ui_utilities.destination_builder import getDestinationByAppCode
import logging

log = logging.getLogger(__name__)
class RegisterView(View):
    '''
       This will be responsible to Register User activity.
       It has get method to show the screen and post call responsible for registering user.
       PATH VARIABLES:
           -request: A HttpRequest object which has originated the request.
           -app_code: Application code from which application request has been comes from.
        GET VARIABLES:
            -des: A destination to which it will be redirected back in case request completed successfully.
            -itest: If any URL faced any issue and want to report then this will be take care by this parameter,
                    It has severity level such as 
                        0- Small Minor, user will see some internal issues, apologizes we are working on it
                        1- Minor, user will see we are working on it to get it fixed for you.
                        2- Sever, User will see, we are working fine thanks for the testing.
       LOGIC:
           GET:
               It first checks the required GET parameters if it is not valid create a destination URL on the basics of the 
               application code and return back to the register screen.
           POST:
               Once User has key in his all the required details, it will be validated and make a web service call to save the details and return
               to the verify page.
               User also must have got an email to verify the account.
    '''
    #@cache_page(60 * 15, cache="uim.register")
    def get(self, request, app_code = '1'):
        '''
           This will be used for any Register request landing for this page.
           This expect for a get parameter i.e a destination where user will be navigate, if it is absent a destination URL 
           is formed on the basics of the application code.These are the below two possible get values it will look at
               -des
               -next
           @param request: HttpRequest made by the user.
           @param app_code: Application Code, from where request came from
        '''
        log.info('[START]-Request Received for Register Page.');
        destination, _issues = request.GET.get('des', request.GET.get('next')), request.GET.get('itest');
        destination = destination if destination else getDestinationByAppCode(app_code); 
        context = RequestContext(request, self.buildRegisterViewArgs(app_code, destination, _issues));
        log.info('[END]- Request Served for the register page.')
        return render_to_response('register/register.html', context)
    
    def buildRegisterViewArgs(self, app_code, destination, issues):
        '''
           This will build the register parameter for the register page landing.
           @param app_code: Application From which request coming.
           @param destination: Destination where to navigate
           @param _issues: In case of any issues it will show a issue list.
        '''
        dic, err_msg = {}, ''
        if issues:
            if issues == '0' or issues == 0:
                err_msg = 'Sorry for the inconvenience, we are working on priority to fix this for you.'
            elif issues == '1' or issues == 1:
                err_msg = 'OOPS!!! Something went wrong, we are working on priority to fix this for you.'
            elif issues == '2' or issues == 2:
                err_msg = 'We are working fine Thanks for your time to Test.'
            else:
                err_msg = 'OOPS!!! Something went wrong, we are working on priority to fix this for you.'
        if err_msg:
            dic['INVLDMSG'] = err_msg;
        return prepareRegisterPageContext(app_code, destination, dic);
    
    def post(self, request, app_code = '1'):
        '''
           This will handle register submit form.
           if form validation fails, it will return back to the UI holding form data and validation key and message.
           On successful registration user will be moved to verify form.
           @param request: HttpRequest made by the user.
           @param app_code: Application code, for which user want to register.
        '''
        log.info('[START]- User has Requested to create an account.');
        #populate User submitted form in a map
        form = self.getRegisterForm(request, app_code);
        #Next Validate the form
        errors = self.validateForm(form);
        if errors:
            #add Context and return to the page
            errors['fldval'] = form
            context = RequestContext(request,prepareRegisterPageContext(app_code, errors.get('destination'), errors));
            response = render_to_response('register/register.html', context);
            return response;
        
        #Process Registration
        sr_response = self.register(request, form);
        log.info('[END]- User creation request completed successfully');
        dev_mode = getattr(settings, "SKIP_WEB_CALL", 'n');
        if dev_mode == 'y':
            # TODO: Webmock Method Delete on production ready
            sr_response = self.buildWebMockData();
        return self.processResponse(request, sr_response, form)
    
    def getRegisterForm(self, request, app_code):
        '''
           This will build a dictionary of the submitted registered map.
           @param request: HttpRequest Submitted by the user.  
           @param app_code: Application Code
        '''    
        form = {};
        
        form["fname"] = request.POST.get('fname');
        form["lname"] = request.POST.get('lname');
        form["email"] = request.POST.get('email');
        form["pwd"] = request.POST.get('password');
        form["conf_pwd"] = request.POST.get('confirmPassword');
        form["birth_date"] = request.POST.get('birth_date');
        form["birth_month"] = request.POST.get('birth_month');
        form["birth_year"] = request.POST.get('birth_year');
        form["dob"] = form["birth_date"]+"-"+form["birth_month"]+"-"+form["birth_year"];
        form["sex"] = request.POST.get('gender');
        form["tz"] = request.POST.get('timeZone', 'UTC');
        from django.utils import translation
        form["lang"] = request.POST.get('langCode', translation.get_language());
        # Get user Agent and IP
        from useragent.determine_user_agent import UserAgent
        USER_AGENT = UserAgent();
        form["ip"] = USER_AGENT.get_client_ip(request);
        form["agent"] = USER_AGENT.get_browser_agent(request);
        form["destination"] = request.GET.get('des', getDestinationByAppCode(app_code));
        form["app"] = app_code;
        return form;
    
    def validateForm(self, form):
        '''
           This will validate the user submitted form for email, password etc.
           @param form: User Submitted form
        '''
        key, msg, sug = '','','';
        #First Check Form
        if not form:
            log.error('User Entered data is not populated in Request');
            msg += 'OOPS!!!Something Went wrong, we are working on it.\n';
            
        #second Check first name
        if not form["fname"]:
            log.error('An Invalid Name.');
            key += 'fname, lname, ';
            msg += 'An Invalid Name.\n';
            sug += 'Please enter your real name.\n'
        
        #3 check for email
        from django.core.exceptions import ValidationError
        from django.core.validators import validate_email
        try:
            validate_email(form["email"]);
        except ValidationError:
            log.error('An Invalid Email.');
            key += 'email, ';
            msg += 'An Invalid Email Id.\n';
            sug += 'Please enter your email id.\n'
        
        #4 check for password
        if not form["pwd"] or (form["pwd"] != form['conf_pwd']):
            log.error('An Invalid Password.');
            key += 'pwd, ';
            msg += 'An Invalid Password.\n';
            sug += 'Please choose a password and confirm it.\n'
        
        #5 Check for DOB
        from ui_utilities.datetimeutils import DateTimeUtil
        if not DateTimeUtil().validateDateInDMY(form["dob"]):
            log.error('An Invalid date of birth.');
            key += 'dob, ';
            msg += 'An Invalid Date Of Birth.\n';
            sug += 'Please enter your Date of birth.\n'
            
        #6 Check for Sex
        if form["sex"] not in ("M","F", "O", "T"):
            log.error('An Invalid Gender.');
            msg += 'An Invalid Gender.\n';
            sug += 'Please enter your Gender.\n'
        
        key = key.rstrip(', ') if key else None
        msg = key.rstrip('\n') if msg else None
        sug = key.rstrip('\n') if sug else None
        from account.dic_builder import buildValidationErrorDic
        return buildValidationErrorDic(key, msg, sug);
        
    def register(self, request, form):
        '''
           This will register user by calling the service.
           @param request: HttpRequest object submitted by user.
           @param form: Register form submitted by user.
        '''
        import urllib
        WEB_BASE_URL = getattr(settings, "REST_BASE_URL", None);
        WEB_BASE_URL += 'register';
        data = urllib.urlencode(form, doseq=True);
        #make instance of rest client
        from ui_utilities.http_api import RestClient
        client = RestClient();
        return client.postWithAuthHeader(WEB_BASE_URL, data);
    
    def processResponse(self, request, sr_response, form):
        '''
          Builds the response object for the next step of action.
          @param request: HttpRequest object 
          @param sr_response: Response Received from WEB-Service call
        '''
        from ui_utilities.dsutilities import DSUtility
        res_code = DSUtility().getlistitem(sr_response, 'RESCD');
        res_msg = DSUtility().getlistitem(sr_response, 'MSG');
        errors = {};
        if res_code == "200" or res_code == 200:
            log.info('[END]- Registration process completed, redirecting to verify screen.');
            return self.nextView(DSUtility().getlistitem(res_msg, 'tmpprfid'), form.get('email'), form.get('destination'), form.get('app'))
        else:
            from account.dic_builder import buildValidationErrorDic
            if res_code == "406" or res_code == 406:
                #Invalid Field
                errors = buildValidationErrorDic(DSUtility().getlistitem(res_msg, 'INVLDKEY'), DSUtility().getlistitem(res_msg, 'INVLDMSG'), DSUtility().getlistitem(res_msg, 'INVLDSUG'));
                
            elif res_code == "400" or res_code == 400:
                #Web service didn't receive any input
                errors = buildValidationErrorDic(None, 'OOps provided data is not sufficient.', 'Please check with the entered data and try again.');
            else:
                #in case of internal server error.
                errors = buildValidationErrorDic(None, 'OOps, Something went wrong, we are working on it.', 'Please check with us again after sometime, apologies for the inconvenience.');
                
            errors['fldval'] = form;
            context = RequestContext(request,prepareRegisterPageContext(form.get('app'), form.get('destination'), errors));
            response = render_to_response('register/register.html', context);
            return response;
    
    def nextView(self, tempProfileId, email, destination, app):
        '''
           This will navigate to the verify screen once register request has been completed.
           @param tempProfileId: Created profile ID
           @param email: Email Id that has been registered now.
           @param destination: Destination Where It will be Navigated.
           @param app: Application Code 
        '''    
        from account.verify_helper import buildRegisterTokenVerifyGetArguments;
        from django.shortcuts import redirect
        from django.core.urlresolvers import reverse
        return redirect('%s?%s' % (reverse('uim.register.token.verify', kwargs={'tpid':tempProfileId}), buildRegisterTokenVerifyGetArguments(email, destination, 'form', app)));
    
    def buildWebMockData(self):
        '''
           This builds the sample test data to work in eb flow with out web service.
        '''
        rs_msg = {};
        rs_msg['tmpprfid'] = '1234';
        rs = {}
        rs['RESCD'] = "200";
        rs['MSG'] = rs_msg; 
        return rs;
if __name__ == '__main__':
    pass
