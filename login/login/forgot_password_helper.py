import logging

logger = logging.getLogger(__name__)

def buildChangePasswordGetArguments(email = None, des = None, src = 'form', alt_email = None):
        '''
           This will build the Change Password arguments to be redirected to the Change Password view
           @param email: Registered Email Id of the user.
           @param des: Destination where to navigate back.
           @param src: Source default to form
           @param alt_email: Alternative Email of the user.
           @return: A String with all the get arguments
        '''
        _GET_PARAM, _GET_SEPRATOR, apply_sep, _rs_uri = '', '&', False, ''
        _EMAIL_ARG = 'em=%s';
        _ALT_EMAIL_ARG = 'aem=%s'
        _SRC_ARG = 'src=%s'
        _DES_ARG = 'des=%s'
        
        if src:
            _rs_uri += (_SRC_ARG %src);
            apply_sep = True;
        if email:
            if apply_sep:
                _rs_uri += (_GET_SEPRATOR + _EMAIL_ARG %email);
            else:
                _rs_uri += (_EMAIL_ARG %email);
                apply_sep = True;
        
        if alt_email:
            if apply_sep:
                _rs_uri += (_GET_SEPRATOR + _ALT_EMAIL_ARG %alt_email);
            else:
                _rs_uri += (_ALT_EMAIL_ARG %alt_email);
                apply_sep = True;
                
        if des:
            if apply_sep:
                _rs_uri += (_GET_SEPRATOR + _DES_ARG %des);
            else:
                _rs_uri += (_DES_ARG %des);
                apply_sep = True;
        return _rs_uri;    
       
class ForGotPasswordHelper(object):
    '''
       Common Utility class for the forgotPassword process.
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
            dic['FP_INVLDKEY'] = field_key;
        if err_msg:
            dic['FP_INVLDMSG'] = err_msg;
        if suggestion:
            dic['FP_INVLDSUG'] = suggestion;
        return dic;
    
if __name__ == '__main__':
    pass
