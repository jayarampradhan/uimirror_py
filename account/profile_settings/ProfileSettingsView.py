import logging
from django.views.generic.base import View
from custom_mixins.LoginCheckMixin import LoginCheckMixin

log = logging.getLogger(__name__)
class ProfileSettingsView(LoginCheckMixin, View):
    
    def get(self, request):
        pass
        # TODO: Complete This Functionality with UI 