from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View

class UpdatesView(View):
    def get(self, request):
        context = RequestContext(request, {});
        return render_to_response('individual/feed/home.html',context);