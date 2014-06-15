import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View


log = logging.getLogger(__name__)
class CreatePage(View):
    
    def get(self, request):
        dic = {}
        dic['a'] = 'a'
        context = RequestContext(request,dic)
        response = render_to_response('page/create_page.html', context)
        return response