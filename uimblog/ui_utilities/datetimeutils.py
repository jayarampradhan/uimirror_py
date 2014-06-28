#!/usr/bin/env python
from time import gmtime, strftime
from datetime import datetime

class DateTimeUtil(object):
    '''
       This is date time utill class which will be reponsible for 
       all type of date utils
    '''
    DATETIMEFORMAT = '%Y-%m-%d %H:%M:%S'
    DATEFORMAT = '%Y:%m:%d'
    def checkDateLiesWithindaysFromNow(self, o_date, date_range):
        '''
           This will check if date time lies between days specified or not
        '''
        if not date_range and not o_date:
            time_diff_min = self.getTimeDiffInMin(self.getCurrentUTCTime(), o_date)
            if time_diff_min <= date_range:
                return True
        return False

    def getCurrentGmtTime(self):
        '''
           This will get the current gmt time in yyyy-mm-dd hh:mm:s
        '''
        return strftime(self.DATETIMEFORMAT, gmtime())
    
    def convertDateInString(self, strDate):
        '''
           This will convert the date into string format,
           this will get the converted date in yyyy-mm-dd.
        '''
        return datetime.strptime(strDate, self.DATEFORMAT)
    
    def convertDateTimeInString(self, strDate):
        '''
          This will convert date time in string.
        '''
        return datetime.strptime(strDate, self.DATETIMEFORMAT)
    
    def getTimeDiffInMin(self, strDate1, strDate2):
        '''
           This will first convert the string date into datetime,
           then substarct date2 from date1 and get the differance in minute.
        '''
        if type(strDate1) is not datetime.date:
            d1 = datetime.strptime(strDate1, self.DATETIMEFORMAT)
        else:
            d1 = strDate1
            
        if type(strDate1) is not datetime.date:
            d2 = datetime.strptime(strDate2, self.DATETIMEFORMAT)
        else:
            d2 = strDate2
        
        result = d1 - d2
        return result.total_seconds()/60
    
    def getCurrentUTCTime(self):
        '''
           This will generate current UTC time.
        '''
        return datetime.utcnow()

    def getCurrentUTCTimeInString(self):
        '''
           This will get the current UTC time in yyyy-mm-dd hh:mm:s
           in string format.
        '''
        dtime= self.getCurrentUTCTime()
        return strftime(self.DATETIMEFORMAT,dtime.timetuple())
    
    def validateDateInDMY(self, date_str):
        '''
           This will validate if date is in DD-MM-YYYY format or not
           @param date_str: A Date in string format.
        '''
        try:
            datetime.strptime(date_str, '%d-%m-%Y');
            return True;
        except ValueError:
            return False;
