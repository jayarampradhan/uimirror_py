#!/usr/bin/env python

class UserAgent(object):
    '''
       Determine the client details from the inn-comming request.
    '''

    
    def get_client_ip(self,request):
        '''
           Determine the Ip address
        '''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'NA')
        return ip
    
    def get_browser_agent(self, request):
        '''Get the client user agent.'''
        return (request.META.get('HTTP_USER_AGENT', 'NA'));

