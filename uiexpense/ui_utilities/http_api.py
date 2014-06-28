#!/usr/bin/env python

from django.conf import settings
from json import load
from urllib2 import urlopen, URLError
import json
import logging
import urllib2
from commonutilities import CommonUtils 

log = logging.getLogger(__name__)

class HttpApiGet(object):
    '''
       Utility class for all the crul specific work
    '''
    def openurldecodejson(self, url):
        ''' open a given url and returns the python object representation of a json string'''
        query_data = urlopen(url)
        return load(query_data)
    
    def openurldecodesimplejson(self, url):
        ''' open a given url and returns the python object representation of a json string'''
        query_data = urlopen(url).read()
        return json.loads(query_data)
        
        
class RestClient(object):
    '''
      Class for the rest utility methods to make any 
      post or get call to web service with custom authentication key
    '''
    
    def postWithAuthHeader(self, url, data):
        
        try:
            req = urllib2.Request(url)
            req.add_header('apiKey', getattr(settings, "REST_API_KEY", None))
            response = urllib2.urlopen(req, data=data)
            return json.load(response);
        except URLError as e:
            log.error('Exception happened Making Web-service call %s', str(e))
            return CommonUtils().getInavlidResponse();
        except TypeError as e:
            log.error('Exception happened Making Web-service call %s', str(e))
            return CommonUtils().getInavlidResponse();
        
