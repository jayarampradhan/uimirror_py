'''
   This is the shared task definition for the user activity or welcome page activity
   This stores the common task definition
'''
from __future__ import absolute_import
from celery.app import shared_task
from account.constant import Constants

@shared_task
def updateImportedContactCache(contacts, provider, profile_id):
    '''
       This will store the contacts temporary in the cache.
       and make the web service call to store all the contacts imported by the user according to the provider.
    '''
    from django.core.cache import cache
    cache.set(profile_id+Constants.CH_IMPORTED_KEY+provider, contacts, 5*60);
    # TODO: make web-service call to save the Contact Cache

@shared_task    
def updateContactImportStateCache(state, provider, profile_id):
    '''
       This will update the state of the contact importer state into the cache.
    '''
    state[Constants.IMPORT_SERVICE_PRVOVIDER] = provider;
    state[Constants.STEP] = '3';
    from django.core.cache import cache
    cache.set(profile_id+Constants.STATE_POST_FIX, state)

@shared_task    
def sendInvite(contacts, provider, profile_id):
    '''
       This will make the web service call to send the invitation.
    '''
    # TODO: Implement this latter
    pass

@shared_task
def updateStateCache(state, profile_id):
    '''
       This will store the state of the user flow into session async
    '''
    if state and profile_id:
        from django.core.cache import cache
        cache.set(profile_id+Constants.STATE_POST_FIX, state, None);