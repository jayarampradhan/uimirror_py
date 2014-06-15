from django.conf import settings
from django.shortcuts import redirect

from account.constant import Constants


class LoginCheckMixin(object):
    user_check_failure_path = ''  # can be path, url name or reverse_lazy

    def check_user(self, user):
        return True

    def user_check_failed(self, request, *args, **kwargs):
        return redirect(self.user_check_failure_path)

    def dispatch(self, request, *args, **kwargs):
        dev_mode = getattr(settings, "SKIP_WEB_CALL", 'n');
        if dev_mode == 'y':
            request.session[Constants.PRF_ID] = '123';
        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)
        return super(LoginCheckMixin, self).dispatch(request, *args, **kwargs)