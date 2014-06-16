'''
   This will handle the location update request in ajax way.
'''

import logging
from django.views.generic.base import View
from account.constant import Constants
from custom_mixins.LoginCheckMixin import LoginCheckMixin
from custom_mixins.sendajaxresponsemixin import sendResponse

log = logging.getLogger(__name__)
class HandleLocation(LoginCheckMixin, View):
    
    def get(self, request):
        '''
           This will be used for any get request to get location by Location name with cordinates.
           @param request: HttpRequest made by the user.
        '''
        query = request.GET['q'];
        
        if query:
            from django.core.cache import cache
            cache_res = cache.get(Constants.LOCATION_KEY+query);
            if cache_res:
                return sendResponse(request, cache_res);
            else:
                from locationservice.geocoders_parser import GeoCodeParser
                geo_parser = GeoCodeParser();
                result = geo_parser.getGecodesFromGoogle(query);
                if result:
                    from locationservice.tasks import updateLocationCache
                    updateLocationCache.delay(query, result);
                    return sendResponse(request, result);
                else:
                    dic = {}
                    dic['STATUS_CODE'] = 404;
                    dic['MSG'] = 'Not Found';
                    return sendResponse(request, dic);
        else:
            dic = {}
            dic['STATUS_CODE'] = 400;
            dic['MSG'] = 'Invalid Request';
            return sendResponse(request, dic);
    
    def post(self, request):
        '''
           This will handle the location add/update request.
           this will handle in ajax calls. 
        '''
        log.info('[START]- Request Received to update the location details of the user.')
        # TODO: Checks for the parameter which location user wants to update.
        locations_to_update = request.POST.dict();
        # TODO: Handle Current and and home town separate
        log.debug('Current City Lat %s', locations_to_update.get('current.current.location'));
        dic = {}
        dic['STATUS_CODE'] = 200;
        dic['MSG'] = 'success';
        log.info('[END]- Request for location update completed.')
        return sendResponse(request, dic)
        
    def delete(self, request):
        '''
           This will handle the location delete request.
           this will handle in ajax calls. 
        '''
        # TODO: Checks for the parameter which location user wants to update.
        dic = {}
        dic['STATUS_CODE'] = 200;
        dic['MSG'] = 'success';
        return sendResponse(request, dic)
        
    
