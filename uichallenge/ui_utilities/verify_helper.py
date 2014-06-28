'''
   Utility Methods for the Register Token Verification Screen
'''
def buildVerifyPageContext(tempProfileId, email, source, app, destination, _data = {}):
    '''
        tempProfileId, email, source, app, destination, _errors
       This will build the context parameter for the verify screen.
       @param tempProfileId: Temporary Profile ID created for this user.
       @param token: A Token which has been mailed to the user.
       @param email: Email Id of the user.
       @param source: Source Attribute suggests like email/form
       @param app: Application Code
       @param _data: A pre populated data. 
       @return: A dictionary which has the desired parameters to send to the verify screen.
    '''
    _data['prfid'] = tempProfileId;
    if app:
        _data['app_code'] = app;
    if destination:
        _data['des'] = destination;
    _data['email'] = email;
    _data['src'] = source;
    return _data;
        
def buildRegisterTokenVerifyGetArguments(email, destination, source, app):
    '''
       This will build the Register Token Verify arguments to be redirected to the Verify Token screen
        -email: Recently Registered Email.
        -destination: Destination where it will be redirected.
        -source: Source from where verification screen is rendering.
       @param email: Recently Registered Email.
       @param destination: Destination where it will be redirected.
       @param source: from where verification screen is rendering.
       @param app: Application code getting Used
       @return: A String with all the get arguments
    '''
    _GET_PARAM, _GET_SEPRATOR, apply_sep, _rs_uri = '', '&', False, ''
    _DES_ARG = 'des=%s';
    _EMAIL_ARG = 'em=%s'
    _SOURCE_ARG = 'src=%s'
    _APP_CODE_ARG = 'app=%s'
    
    if source:
        _rs_uri += (_SOURCE_ARG %source);
        apply_sep = True;
    if email:
        if apply_sep:
            _rs_uri += (_GET_SEPRATOR + _EMAIL_ARG %email);
        else:
            _rs_uri += (_EMAIL_ARG %email);
            apply_sep = True;
    if app:
        if apply_sep:
            _rs_uri += (_GET_SEPRATOR + _APP_CODE_ARG %app);
        else:
            _rs_uri += (_APP_CODE_ARG %app);
            apply_sep = True;
    if destination:
        if apply_sep:
            _rs_uri += (_GET_SEPRATOR + _DES_ARG %destination);
        else:
            _rs_uri += (_DES_ARG %destination);
            apply_sep = True;
    return _rs_uri;    