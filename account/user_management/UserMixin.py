'''
   This class will be whole responsible to get and set the cache in a Synchronous way.
'''
from account.constant import Constants


def findOrUpdateBasicProfileCache(profile_id):
    '''
       This will update the user profile basic details such as 
           -First Name
           -Last Name
           -Sex
           -Date Of Birth In date, month and year
           -Time Zone
           -Locale
           -current status
    '''
    # TODO: get profile from the web service call
    dic = {};
    dic['fname'] = "Jayaram";
    dic['lname'] = 'Pradhan';
    dic['displayname'] = 'Jayaram';
    dic['sex'] = 'M';
    dic['tz'] = 'Asia/Kolkota';
    dic['locale'] = 'en';
    status = {}
    status['type'] = 'job'
    status['id'] = '1234'
    status['status'] = 'Software engineer'
    status['name'] = 'EMC'
    
    dic['status'] = status
    dob = {}
    dob['date'] = '18'
    dob['month'] = 'March'
    dob['year'] = '1988'
    
    dic['dob'] = status
    from django.core.cache import cache
    cache.set(profile_id+'.prf.basic', dic, None);
    return dic;

def findOrUpdateProfileAttribute(profile_id):
    '''
       This will find or update the attributes about a profile
       it can be age: suggests the new or old
    '''
    dic = {}
    dic['age'] = 'new'
    from django.core.cache import cache
    attr = cache.get(profile_id+'.prf.attr', dic, None);
    if attr:
        return attr;
    else:
        cache.set(profile_id+'.prf.attr', dic, None);
        return attr;
        return attr;
    
def findOrUpdateProfileSettingsCache(profile_id, appName, tab):
    '''
       This will store the User Profile Setting information based on application and tab.
    '''
    cache_key = Constants.PROFILE_KEY+profile_id+'.'+appName+'.'+tab
    from django.core.cache import cache
    result = cache.get(cache_key);
    if not result:
        # TODO: Change this dummy once done
        result = getSocialDummySettings(tab);
        cache.set(cache_key, result, 15*60);
    return result; 

def getSocialDummySettings(tab):
    # TODO: Delete This once done with WS call
    if tab == 'chat':
        return buildDummyChatSetting();
    elif tab == 'snap':
        return buildDummySnapSettings();
    elif tab == 'visibility':
        return buildDummyVisibilitySettings();
    elif tab == 'updates':
        return buildDummyUpdatesSettings();
    elif tab == 'account':
        return buildDummyAccountSettings();
    else:
        return 'test';
    
def buildDummyChatSetting():
    # TODO : Delete This as This was for only dummy data
    return {'showlocation': 'Y', 'minimizewindow' : 'y', 'visible': {'id':0}}
    
def buildDummySnapSettings():
    # TODO : Delete This as This was for only dummy data
    return {'downdloadable' : {'id':0}, 'contributor':{'id':0}};
def buildDummyVisibilitySettings():
    # TODO : Delete This as This was for only dummy data
    return {'observer' : 'y', 'showmetorechable' : 'y', 'showemtofollowers': 'y', 'whocanreachme':{'id':0}};
def buildDummyUpdatesSettings():
    # TODO : Delete This as This was for only dummy data
    return {'showlocation' : 'y', 'showdevice' : 'y', 'noupdatesfrom': {'enable':'Y'}, 'noupdatesto': {'enable':'Y'}, 'spreader':{'id':0}};
def buildDummyAccountSettings():
    # TODO : Delete This as This was for only dummy data
    return {'displaynameas' : 0, 'dateformat' : 1};