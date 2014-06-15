#!/usr/bin/env python

class IP2Location(object):
    '''This class represent the location details from ip'''
    
    def __init__(self, country_name, country_code, city, ip):
        self.country_name = country_name
        self.country_code = country_code
        self.city = city
        self.ip = ip;

    def getCountryName(self):
        return self.country_name
    def getCountryCode(self):
        return self.country_code
    def getCity(self):
        return self.city
    def getIP(self):
        return self.ip
    
    def __unicode__(self):
        return u"%s %s %s" %(self.city, self.country_name, self.ip)

if __name__ == '__main__':
    pass