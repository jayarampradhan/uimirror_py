import logging

logger = logging.getLogger(__name__)

def buildRegisterViewGetArguments(destination = None, issues = None):
        '''
           This will build the Register Token Verify arguments to be redirected to the Verify Token screen
            -email: Recently Registered Email.
            -destination: Destination where it will be redirected.
            -source: Source from where verification screen is rendering.
           @param app: Application Code.
           @param destination: Destination where it will be redirected.
           @param issues: If it needs to redirect because some issue happened.
           @return: A String with all the get arguments
        '''
        _GET_PARAM, _GET_SEPRATOR, apply_sep, _rs_uri = '', '&', False, ''
        _DES_ARG = 'des=%s';
        _ISSUES_ARG = 'itest=%s'
        if issues:
            _rs_uri += (_ISSUES_ARG %issues);
            apply_sep = True;
            
        if destination:
            if apply_sep:
                _rs_uri += (_GET_SEPRATOR + _ISSUES_ARG %destination);
            else:
                _rs_uri += (_ISSUES_ARG %destination);
                apply_sep = True;
        return _rs_uri;    

def prepareRegisterPageContext(app_code, destination, dic = {}):
    '''
       This prepares the register page parameters to be sent for the template processing
       -Required attributes are app_code and destination
    '''
    if app_code:
        dic['app_code'] = app_code;
    if destination:
        dic['des'] = destination;
    return dic;
       
class RegHelper(object):
    '''
       Common Utility class for the register process.
    '''        
    def buildRedirectToLoginDic(self, app_code, destination_ep):
        '''
           Build to register page context variable.
           @param app_code: appCode 
           @param destination_ep: Destination URl
           @return: HttpResponse
        '''
        dic = {}
        dic['appcode'] = app_code
        if destination_ep:
            dic['des'] = destination_ep

        return dic
    
    def buildValidationDic(self, field_key, err_msg, suggestion):
        '''
           This will build register form validation error message to be shown to the user.
           @param field_key: Key needs to highlighted
           @param err_msg: Error Message that will be shown up
           @param suggestion: Suggestion that user needs to take care
        '''
        dic = {}
        if field_key:
            dic['INVLDKEY'] = field_key;
        if err_msg:
            dic['INVLDMSG'] = err_msg;
        if suggestion:
            dic['INVLDSUG'] = suggestion;
        return dic;
    
if __name__ == '__main__':
    pass
