from django.views.generic.base import View
from django.http.response import HttpResponse
class UpdatesView(View):
    def get(self, request):
        return HttpResponse('Success');