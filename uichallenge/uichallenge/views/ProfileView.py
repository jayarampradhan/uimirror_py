from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View

class ProfileView(View):
    def get(self, request, pid, name):
        context = RequestContext(request, {});
        return render_to_response('profile/home.html',context);