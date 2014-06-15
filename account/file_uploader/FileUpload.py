from django.views.generic.base import View

from custom_mixins.LoginCheckMixin import LoginCheckMixin
from custom_mixins.sendajaxresponsemixin import sendResponse


class SnapUpload(LoginCheckMixin, View):
    '''
       This will upload the file in the system.
       This will support only ajax call.
    '''
    def post(self, request):
        '''
           This will upload the snap onto the system.
           This will decided which type of file based on the post attribute file  
        '''
        # TODO: Build the necessary step for the snap upload
        dic = {}
        dic['STATUS_CODE'] = 200;
        dic['MSG'] = 'success';
        return sendResponse(request, dic);