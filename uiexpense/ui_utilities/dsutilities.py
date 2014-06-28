#!/usr/bin/env python

class DSUtility(object):
    '''
       This will be genric api for different datastructre.
    '''
    def getlistitem(self, listitems, item):
        ''' returns the desired item of a list if available otherwise return None'''
        if item in listitems:
            return listitems[item]
        else:
            return None
    
    def buildDictNary(self, **kwargs):
        '''
           This will create a dictonairy.
        '''
        d = {}
        for name, value in kwargs.items():
            d[name] = value
            
        return d;

    def addUniqueElementToArray(self, arr, elm):
        addFlag = False
        for em in arr:
            if elm == em:
                addFlag = False
                break;
            else:
                addFlag = True
                if addFlag:
                    arr.append(elm)
        return arr
