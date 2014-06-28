'''
This is a common service interface to retrieve all the user details when requested for
It will first query the local cache if not found, it will query the Webservice to get the details
# TODO: currently the implementation is a dummy return but this needs to be finalize soon.
'''
import logging


log = logging.getLogger(__name__)
def getUserShortSummery(request, profile_id = None):
    '''
       It will retrieve user short summary like name, sex, locale
       # TODO: give the complete definition latter with doc update
    '''
    dic = {};
    dic['fname'] = "Jayaram";
    dic['lname'] = 'Pradhan';
    dic['sex'] = 'M';
    dic['type'] = 'new';
    loc = {};
    loc['id'] = "12345";
    loc['name'] = "Bhubaneswar";
    plcaes = {};
    plcaes['current'] = loc;
    dic['loc'] = plcaes;
    from django.core.cache import get_cache
    redis_cache = get_cache('default')  # Use the name you have defined for Redis in settings.CACHES
    redis = redis_cache.raw_client
    connection_pool = redis.connection_pool
    log.info('Created connections so far: %d' % connection_pool._created_connections)
    
    #json.dumps(dic) 
    return dic;