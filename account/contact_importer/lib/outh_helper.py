import logging

from django.conf import settings
from django.core.urlresolvers import reverse

from account.constant import Constants
from contact_importer.providers.google import GoogleContactImporter
from contact_importer.providers.live import LiveContactImporter
from contact_importer.providers.yahoo import YahooContactImporter


log = logging.getLogger(__name__)
class OuathHelper(object):
    '''
       Helper class which will help us to identify if it needs a redirect or not.
       providers says which are the current providers we are supporting.
    '''
    providers = {
                 "google": GoogleContactImporter,
                 "live": LiveContactImporter,
                 "yahoo": YahooContactImporter
                 }
    
    def _get_redirect_url(self, request):
        '''
           This will get the next redirect URL, before making the auth request to the provider.
           @param request: HttpRequest Object
           @return: A URL, which will be redirect to the providers.
        '''
        provider = request.GET.get(Constants.PROVIDER);
        invite_url = "%s?provider=%s" % (reverse("account.uiwelcome.contacts.invite"), provider)
        
        request_scheme = Constants.RQ_SCH_SECURE if request.is_secure() else Constants.RQ_SCH_HTTP
        redirect_url = "%s://%s%s" % (request_scheme, request.META["HTTP_HOST"], invite_url);
        return redirect_url

    def _get_provider_instance(self, provider, redirect_url):    
        '''
           Help to get the instance of the service providers.
           @param provider: A string which specifies which provider like google, yahoo etc.
           @param redirect_url: URL, which will be redirected for outh token
        '''
        if provider not in self.providers:
            raise Exception("The provider %s is not supported." % provider)
        client_id = getattr(settings, "%s_CLIENT_ID" % provider.upper(), None);
        client_secret = getattr(settings, "%s_CLIENT_SECRET" % provider.upper(), None)
        
        if not client_id:
            raise Exception("The provider %s is not supported." % provider)
        
        provider_class = self.providers[provider]
        return provider_class(client_id, client_secret, redirect_url)        