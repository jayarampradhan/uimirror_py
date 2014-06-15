#!/usr/bin/env python

from pyhostipdata import IP2Location
from ui_utilities.dsutilities import DSUtility
from ui_utilities.http_api import HttpApiGet


class HostIpClinetApi(object):
    
    HOSTIP_URL = 'http://api.hostip.info/get_json.php'
    POSITION = '&position=true'
    httpapiget = HttpApiGet()
    
    def getLocationByIP(self, ip):
        '''return Location information 
           for example http://api.hostip.info/get_json.php?ip=122.22.1.1&position=true
        '''    
        if not ip:
            return None
        
        querypart = '?ip=%s' % ip
            
        queryurl = self.HOSTIP_URL + querypart + self.POSITION
        short_summery = self.httpapiget.openurldecodesimplejson(queryurl)
        return self.getLocationSummery(short_summery);
        
    
    def getLocationSummery(self, dictionary):
        '''Returns the Location short summery'''
        country_name = DSUtility().getlistitem(dictionary, 'country_name')
        country_code = DSUtility().getlistitem(dictionary, 'country_code')
        city = DSUtility().getlistitem(dictionary, 'city')
        ip = DSUtility().getlistitem(dictionary, 'ip')
        return IP2Location(country_name, country_code, city, ip)
    
if __name__ == '__main__':
    pass