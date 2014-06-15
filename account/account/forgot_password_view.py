import logging
import sys

from django.http import HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View

from useragent import user_agent_parser
from useragent.determine_user_agent import UserAgent


USER_AGENT = UserAgent()

log = logging.getLogger(__name__)

class ForgotPasswordView(View):
    
    def get(self, request):
        '''
           This will be used for Forgot password request landing for this page.
        '''
        log.info('user agent %s' %(USER_AGENT.get_client_ip(request)))
        print 'User agent %s' %(USER_AGENT.get_browser_agent(request))
        print 'User agent %s'%(user_agent_parser.Parse(USER_AGENT.get_browser_agent(request)))
        dic = {}
        dic['a'] = 'a'
        context = RequestContext(request,dic)
        response = render_to_response('forgot/forgot_password.html', context)
        return response
        #return HttpResponse('sucess');
        

    
if __name__ == '__main__':
    pass