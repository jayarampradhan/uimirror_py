import logging


logger = logging.getLogger(__name__)

def buildValidationErrorDic(field_key, err_msg, suggestion):
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
