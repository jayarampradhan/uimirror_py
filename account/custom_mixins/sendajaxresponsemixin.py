def sendResponse(request, response):
    '''
        This will handle the response to be sent over network
        @param request: httpRequest 
        @param response: Response that will be sent over network.
    '''
    if(request.is_ajax()):
        from ui_utilities.JSONResponseMixin import JSONResponseMixin
        return JSONResponseMixin().render_to_response(response);
    else:
        from django.http.response import HttpResponse
        return HttpResponse(response);