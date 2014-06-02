from django.conf import settings
from django.conf.urls import patterns, url, include

from forgot_password_view import ForGotPassword
from login.change_pwd_view import ChangePassword
from login_view import LoginView
from pre_login_view import PreLogin
from resend_reset_mail_view import ResendResetMail


#from django.contrib import admin
#admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'login.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', PreLogin.as_view(), name='uim.prelogin'),
    url(r'^(?P<app_code>\d{1})/$', LoginView.as_view(), name='uim.login'),
    #ForgotPassword
    url(r'^forgotpassword/(?P<app_code>\d{1})/$', ForGotPassword.as_view(), name='uim.forgot.password'),
    #Resend Mail
    url(r'^forgotpassword/resend/(?P<app_code>\d{1})/(?P<mode>\d{1})/(?P<pid>\d+)/(?P<rid>\d+)/$', ResendResetMail.as_view(), name='uim.forgot.password.resend.mail'),
    #ForgotPassword Reset Password
    url(r'^change/(?P<app_code>\d{1})/(?P<mode>\d{1})/(?P<pid>\d+)/(?P<rid>\d+)/$', ChangePassword.as_view(), name='uim.change.password'),
    
)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
