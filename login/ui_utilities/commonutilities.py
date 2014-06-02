#!/usr/bin/env python

class CommonUtils(object):
    
    def getPostiveIntFromString(self,numstr):
        import string
        a=string.maketrans('','')
        ch=a.translate(a, string.digits)
        return int(numstr.translate(a, ch))
    
    def rreplace(self, s, old, new, occurrence):
        '''
           Find the string and replace the character specified to the number of occurrences from last.
           @param s: string where search operation will happen
           @param old: old value 
           @param new: new value to be replaced
           @param occurrence: number of time from right it will be replaced
        '''
        li = s.rsplit(old, occurrence)
        return new.join(li)
    
    def lreplace(self, s, old, new, occurrence):
        '''
           Find the string and replace the character specified to the number of occurrences from last.
           @param s: string where search operation will happen
           @param old: old value 
           @param new: new value to be replaced
           @param occurrence: number of time from right it will be replaced
        '''
        li = s.lsplit(old, occurrence)
        return new.join(li)
    
    def getInavlidResponse(self):
        '''
           This will return a dictionary containing response code and error message so that caller can translate it.
           @return: dict: containing response code and error message as internal error
        '''
        return {"RESCD":"500", "MSG":"OOps Something went wrong!!! We are working on to get that for you ASAP."}
        
