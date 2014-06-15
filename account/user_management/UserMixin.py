'''
   This class will be whole responsible to get and set the cache in a Synchronous way.
'''
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