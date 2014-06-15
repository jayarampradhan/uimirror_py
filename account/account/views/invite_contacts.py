'''
   This will invite the imported contact from the provider.
'''
import logging

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import View

from account.constant import Constants
from account.tasks import updateImportedContactCache, sendInvite
from contact_importer.lib.outh_helper import OuathHelper
from custom_mixins.LoginCheckMixin import LoginCheckMixin
from custom_mixins.sendajaxresponsemixin import sendResponse


log = logging.getLogger(__name__)
class InviteEmailContact(LoginCheckMixin, View):
    '''
       Generic Contact invite helper.
       Once service provider respond with the contact list process them and return back to user UI.
       Store the contacts in cache for some time and make a web-service call to save all the contact imported 
       for the profile id.  
    '''
    def get(self, request):
        log.info('[START]- Contact Response has been received from the provider.');
        provider = request.GET.get(Constants.PROVIDER);
        code = request.GET.get('code')
        oauth_token = request.GET.get('oauth_token')
        oauth_verifier = request.GET.get('oauth_verifier')
        redirect_url = OuathHelper()._get_redirect_url(request)
        

        provider_instance = OuathHelper()._get_provider_instance(provider, redirect_url)
        if provider == Constants.YAHOO:
            provider_instance.oauth_token = oauth_token
            provider_instance.oauth_verifier = oauth_verifier
            provider_instance.oauth_token_secret = request.session["oauth_token_secret"]
            provider_instance.get_token()
            contacts = provider_instance.import_contacts()
            del request.session["oauth_token_secret"]
        else:
            access_token = provider_instance.request_access_token(code)
            contacts = provider_instance.import_contacts(access_token)
            
        profile_id = request.session.get(Constants.PRF_ID);
        updateImportedContactCache.delay(contacts, provider, profile_id);
        from django.core.cache import cache
        _next_des = cache.get(profile_id+Constants.CH_NEXT_KEY);
        log.info('[END]- Contact Response saved to cache and redirecting user to the destination url.')
        if not _next_des:
            return redirect(reverse('account.uiwelcome'));
        else:
            return redirect(_next_des);
        
    def post(self, request):
        '''
           This will help us to send the invitation to the user based on the contact selected.
           this will be in ajax way to send the invitation.
           email id's will be in array so save that into the cache as well for that provider and user profile id.
        '''
        log.info('[START]- Request Received for the sending invitation.');
        provider = request.GET.get(Constants.PROVIDER);
        ids = request.POST.getlist("ids");
        profile_id = request.session.get(Constants.PRF_ID);
        sendInvite.delay(ids, provider, profile_id);
        log.info('[END]- Request completed for the sending invitation.');
        dic = {}
        dic['STATUS_CODE'] = 200;
        dic['MSG'] = 'success';
        return sendResponse(request, dic)