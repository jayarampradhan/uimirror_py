'''
   This is the shared task definition for the Location cache update and back sync to the mongo instance
   This stores the common task definition
'''

from __future__ import absolute_import

from celery.app import shared_task

from account.constant import Constants


@shared_task
def findOrUpdateProfileSettingsCache(profile_id, appName, tab):
    '''
       This will store the User Setting information based on application and tab.
    '''
    cache_key = Constants.PROFILE_KEY+profile_id+'.'+appName+'.'+tab
    from django.core.cache import cache
    result = cache.get(cache_key);
    if not result:
        # TODO: Change this dummy once done
        result = buildDummyChatSetting();
        cache.set(cache_key, result, 15*60);
    return result; 

def buildDummyChatSetting():
    return {'showlocation': 'Y', 'minimizewindow' : 'y', 'visible': '0'}
    
    
    