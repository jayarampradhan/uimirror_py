from django.test import TestCase
from ui_utilities.datetimeutils import DateTimeUtil
# Create your tests here.
class BaseTestCase(TestCase):
    
    def setUp(self):
        pass
    
class DateTimeTest(BaseTestCase):
    '''
       This will check the time api methods.
    '''
    dateApi = DateTimeUtil()
    
    def getCurrentTimeUTCTest(self):
        print 'Current UTC Time %s' %(self.dateApi.getCurrentUTCTime())
    
    def getCurrentTimeInUTCString(self):
        print 'Current UTC time in String %s' %(self.dateApi.getCurrentUTCTimeInString())
    
    def convertDateTimeInString(self):
        print 'Converted Date Time is %s' %(self.dateApi.convertDateInString('2014-01-12 12:12:12'))
        
    def testDateLiesBetweenRange(self):
        print self.dateApi.checkDateLiesWithindaysFromNow(self.dateApi.getCurrentUTCTime(), 14*24*60)
