'''
   This is responsible for the background job to get all the user related details from either WEB Call
   or get the object to store into the cache 
'''
from __future__ import absolute_import
from celery.app import shared_task


@shared_task
def findOrUpdateBasciProfileCache(profile_id):
    '''
       This will check the cache if user basic information exists or not
       if not it will get from the WEB call and update the cache
    '''
    from django.core.cache import cache
    user_basic = cache.get(profile_id+'.prf.basic');
    if user_basic:
        return user_basic;
    else:
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
        # TODO: get the details from the WEB and set into the cache
        cache.set(profile_id+'.prf.basic', dic, None)
        return dic;