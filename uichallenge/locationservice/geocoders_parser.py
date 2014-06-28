import logging

from geopy import geocoders

from ui_utilities.dsutilities import DSUtility


log = logging.getLogger(__name__)

class GeoCodeParser(object):
    '''
       Utility class for parsing geocders by name of the location
       It uses internal API of Geocoders. 
    '''
    def getGecodesFromGoogle(self, location_query):
        '''
           This is used for getting the locations with longitude and latitude 
           for a query string using Google V3
           @param location_query: Location Name user entered.
           @return: Location array with longitude and latitude.
        '''
        log.debug('Getting the Location Details by location Name %s',location_query);
        
        if not location_query:
            return None;
        try:
            g = geocoders.GoogleV3();
            geocodes = g.geocode(location_query, exactly_one=False)
        except Exception as e:
            log.error('Exception during getting details about the location %s', str(e));
            return None;
        
        log.info(geocodes);
        ds = DSUtility();
        cityList = []
        for geocode in geocodes:
            location, (lat, lon) = geocode;
            log.debug("Location %s Lat %s Long %s", location, lat, lon);
            #TODO Implement the logic of seprating Country City ETC 
            cityList.append(ds.buildDictNary(location = location, lon = lon, lat = lat));
        
        return cityList;
    