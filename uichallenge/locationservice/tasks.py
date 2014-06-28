'''
   This is the shared task definition for the Location cache update and back sync to the mongo instance
   This stores the common task definition
'''

from __future__ import absolute_import

from celery.app import shared_task

from account.constant import Constants


@shared_task
def updateLocationCache(query, result):
    '''
       This will store the location temporary in the cache.
    '''
    from django.core.cache import cache
    cache.set(Constants.LOCATION_KEY+query, result, 12*60*60);