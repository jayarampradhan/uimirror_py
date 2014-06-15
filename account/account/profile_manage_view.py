import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View


log = logging.getLogger(__name__)
class ProfileManageView(View):
    def get(self, request):
        dic = {}
        context = RequestContext(request,dic)
        response = render_to_response('profile/manage/manage.html', context)
        return response