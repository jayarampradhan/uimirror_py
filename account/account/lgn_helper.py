import logging

logger = logging.getLogger(__name__)

def buildAuthenticateParam(self, res_msg):
        '''
           This will build the authentication get message to be sent to the called page,
           all data needs to be encrypted
           this will encrypt the token and auth details and form as string and returns
           @param res_msg: Auth Dictionary
           @return: A string containing the authentication details as Get Parameter
        '''
        from django.conf import settings
        PRV_ENC_KEY = getattr(settings, "PRV_ENC_KEY", 'n');
        from ui_utilities.dsutilities import DSUtility
        # First AUth ID
        auth_id = DSUtility().getlistitem(res_msg, 'authid');
        from encryption.uiencrypt import EncryptionUtil
        authIdApi = EncryptionUtil(PRV_ENC_KEY);
        auth_id = authIdApi.encryptText(auth_id);
        # Second Prev AUth ID
        prv_auth_id = DSUtility().getlistitem(res_msg, 'prvauthid');
        prv_auth_id = authIdApi.encryptText(prv_auth_id);
        
        # 3 Token
        token = DSUtility().getlistitem(res_msg, 'token');
        token = authIdApi.encryptText(token);
        # 4 Prev Token
        prv_token = DSUtility().getlistitem(res_msg, 'prvtoken');
        prv_token = authIdApi.encryptText(prv_token);
        # 5 Profile ID
        prf_id = DSUtility().getlistitem(res_msg, 'prfid');
        prf_id = authIdApi.encryptText(prf_id);
        
        return 'au=%s&pau=%s&tn=%s&ptn=%s&pi=' %(auth_id, prv_auth_id, token, prv_token, prf_id);   

def buildLoginGetArguments(destination = None, itest = None):
        '''
           This will build the login arguments to be redirected to the login view
           -des: A destination where request will be forwarded.
           -itest: If any URL faced any issue and want to report then this will be take care by this parameter,
                    It has severity level such as 
                        0- Small Minor, user will see some internal issues, apologizes we are working on it
                        1- Minor, user will see we are working on it to get it fixed for you.
                        2- Sever, User will see, we are working fine thanks for the testing.
           @param destination: Destination after which it will be redirected.
           @param _issues: Issues if have any to show in the login page.
           @return: A String with all the get arguments
        '''
        _GET_PARAM, _GET_SEPRATOR, apply_sep, _rs_uri = '', '&', False, ''
        _DES_ARG = 'des=%s';
        _ISSUE_ARG = 'itest=%s'
        
        if itest:
            _rs_uri += (_ISSUE_ARG %itest);
            apply_sep = True;
                
        if destination:
            if apply_sep:
                _rs_uri += (_GET_SEPRATOR + _DES_ARG %destination);
            else:
                _rs_uri += (_DES_ARG %destination);
                apply_sep = True;
        return _rs_uri;    
class LoginHelper(object):
    '''
       Common Utility class for the login process.
    '''        
    
    def buildValidationDic(self, field_key, err_msg, suggestion):
        '''
           This will build login form validation error message to be shown to the user.
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
