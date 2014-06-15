import logging

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import View

from account.constant import Constants
from account.tasks import updateContactImportStateCache
from contact_importer.lib.outh_helper import OuathHelper
from custom_mixins.LoginCheckMixin import LoginCheckMixin


log = logging.getLogger(__name__)
class ContactImporter(LoginCheckMixin, View):
    '''
       Generic Contact Importer, which will make request to the service provider.
       Once Contact Information is available request will be back to the welcome page -> get
    '''
    
    def get(self, request):
        '''
           GET request that user will be making to import the contact with provider as get parameters.
           If providers is empty or null then throw exception/ error message.
           @param request: HttpRequest Made by the user
        '''
        provider = request.GET.get(Constants.PROVIDER);
        profile_id = request.session.get(Constants.PRF_ID);
        log.info('[START]-Request Received for importing contact from %s',provider);
        if cache.get(profile_id+Constants.CH_IMPORTED_KEY+provider):
            log.info('Contact Already Imported from the service provider, no need for another call.');
            return redirect(reverse('account.uiwelcome'));
        # TODO: Make Provider Validation
        provider_instance = OuathHelper()._get_provider_instance(provider, OuathHelper()._get_redirect_url(request))
        if provider == Constants.YAHOO:
            provider_instance.get_request_token()
            request.session["oauth_token_secret"] = provider_instance.oauth_token_secret
        
        state = cache.get(request.session.get(Constants.PRF_ID) +Constants.STATE_POST_FIX);
        
        updateContactImportStateCache.delay(state, provider, profile_id)    
        log.info('[END]-Request Redirecting to the Provider site.');
        return redirect(provider_instance.request_authorization());