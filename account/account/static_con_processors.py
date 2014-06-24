def global_settings(request):
    # return any necessary values
    return {
        'IMAGE_PATH': 'test',
        'GOOGLE_API_KEY': 'test',
        'apps':getAvailableApplication(),
        'SOCIAL_CHAT_VISIBILITIES' : getSocialChatVisibility(),
        'SOCIAL_SNAP_DOWNLOADABLES' : getSocialSnapDownLoadOptions(),
        'SOCIAL_SNAP_CONTRIBUTORS' : getSocialSnapContributorsOptions(),
        'SOCIAL_VISIBILITY_RECHABLES' : getSocialVisibilityReachMeOptions(),
        'SOCIAL_UPDATE_SPREAD_OPTNS' : getSocialUpdateSpreadOptions(),
        'SOCIAL_ACCOUNT_DISPLAYNAME_OPTNS' : getSocialAccountDisplayNameOptions(),
        'SOCIAL_ACCOUNT_DISPLAYDATE_FORMAT_OPTNS' : getSocialAccountDisplayDateFormatOptions(),
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

def getSocialChatVisibility():
    '''
       This will set the visibility of the chat setting of the user profile 
    '''
    visibilities = []
    visibilities.append({'id':0, 'name':'Visible To all'});
    visibilities.append({'id':1, 'name':'Invisible'});
    visibilities.append({'id':2, 'name':'Custom'});
    return visibilities;

def getSocialSnapDownLoadOptions():
    '''
       This will be the maximum options available for the options to down load image in social page. 
    '''
    downloadable = []
    downloadable.append({'id':0, 'name':'Everybody'});
    downloadable.append({'id':1, 'name':'Reachable users only'});
    downloadable.append({'id':2, 'name':'Snap/Album Specific'});
    downloadable.append({'id':3, 'name':'Custom'});
    downloadable.append({'id':4, 'name':'No One'});
    return downloadable;

def getSocialSnapContributorsOptions():
    '''
       This will be the maximum options available for the options to contributor list in social page. 
    '''
    contributors = []
    contributors.append({'id':0, 'name':'Everybody'});
    contributors.append({'id':1, 'name':'Reachable users only'});
    contributors.append({'id':2, 'name':'Snap/Album Specific'});
    contributors.append({'id':3, 'name':'Custom'});
    contributors.append({'id':4, 'name':'No One'});
    return contributors;

def getSocialVisibilityReachMeOptions():
    '''
       This will be the maximum options available for the options to who can reach me list in social page. 
    '''
    rechable_options = []
    rechable_options.append({'id':0, 'name':'Everybody'});
    rechable_options.append({'id':1, 'name':'Who Know my email'});
    rechable_options.append({'id':2, 'name':'Who has common reachable'});
    rechable_options.append({'id':3, 'name':'Who has common School'});
    rechable_options.append({'id':4, 'name':'Who has common College'});
    rechable_options.append({'id':5, 'name':'Who is currently working with me'});
    rechable_options.append({'id':6, 'name':'With whom I have worked'});
    rechable_options.append({'id':7, 'name':'No One'});
    return rechable_options;

def getSocialUpdateSpreadOptions():
    '''
       This will be the maximum options available for the options to who can spread my updates list in social page. 
    '''
    spread_options = []
    spread_options.append({'id':0, 'name':'Everybody'});
    spread_options.append({'id':1, 'name':'Reachable and followers'});
    spread_options.append({'id':2, 'name':'Reachable users only'});
    spread_options.append({'id':3, 'name':'Followers only'});
    spread_options.append({'id':4, 'name':'Update Specific'});
    spread_options.append({'id':5, 'name':'Custom'});
    spread_options.append({'id':6, 'name':'No One'});
    return spread_options;

def getSocialAccountDisplayNameOptions():
    '''
       This will be the maximum options available for the options to display Name list in social page. 
    '''
    displayname_options = []
    displayname_options.append({'id':0, 'name':'First Name'});
    displayname_options.append({'id':1, 'name':'Last Name'});
    return displayname_options;

def getSocialAccountDisplayDateFormatOptions():
    '''
       This will be the maximum options available for the options to display Date Format list in social page. 
    '''
    dateformat_options = []
    dateformat_options.append({'id':0, 'name':'YYYY-MM-DD HH:MM:SS'});
    dateformat_options.append({'id':1, 'name':'DD-MM-YYYY HH:MM:SS'});
    dateformat_options.append({'id':2, 'name':'MM-DD-YYYY HH:MM:SS'});
    dateformat_options.append({'id':3, 'name':'DD-Month-YYYY HH:MM:SS'});
    dateformat_options.append({'id':4, 'name':'Month-DD-YYYY HH:MM:SS'});
    return dateformat_options;