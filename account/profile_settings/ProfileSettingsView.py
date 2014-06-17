import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from custom_mixins.LoginCheckMixin import LoginCheckMixin

log = logging.getLogger(__name__)
class ProfileSettingsView(LoginCheckMixin, View):
    
    def get(self, request):
        context = RequestContext(request, {});
        log.info('[END]- Welcome View rendered.');
        return render_to_response('profile/settings/home.html',context);
        pass
        # TODO: Complete This Functionality with UI 