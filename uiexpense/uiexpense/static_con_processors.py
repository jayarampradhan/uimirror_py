def global_settings(request):
    # return any necessary values
    return {
        'IMAGE_PATH': 'test',
        'GOOGLE_API_KEY': 'test',
        'apps':getAvailableApplication(),
    }
    
def getAvailableApplication():
    '''
       This will return the available applications and there respective URL
    '''
    apps = []
    social = {}
    social['name'] = 'Social'
    social['url'] = '//uimirror.com'
    apps.append(social);
    return apps;
