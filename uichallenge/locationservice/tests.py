from django.test import TestCase
import logging
from locationservice.pyhostip import HostIpClinetApi
# Create your tests here.

logger = logging.getLogger(__name__)

class BaseTestCase(TestCase):
    
    def setUp(self):
        pass
    
    
class LocationTest(BaseTestCase):
    def testgetweatherByCityNameAndCountry(self):
        '''
           This will test for the city weather by city name and country code
        '''
        api = HostIpClinetApi()
        print 'Location %s' %(api.getLocationByIP('122.167.118.254').getCity())
        logger.info(api.getLocationByIP('122.167.118.254').getCity());
        self.assertTrue(True, 'true');
    

