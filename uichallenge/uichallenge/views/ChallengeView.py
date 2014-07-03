from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View

class ChallengeView(View):
    def get(self, request, cid, cname):
        context = RequestContext(request, {});
        return render_to_response('challenge/view/home.html',context);