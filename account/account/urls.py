from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from account.views.ThirdPartyContactImport import ContactImporter
from account.views.invite_contacts import InviteEmailContact
from account.views.register_view import RegisterView
from account.views.resend_register_verify_token_view import ResendVrfyEmailView
from account.views.verify_change_email_view import ChangeEmailView
from account.views.verify_register_token_view import VerifyView
from account.views.welcome_view import WelcomeView
from create_page_view import CreatePage
from forgot_password_view import ForgotPasswordView
from profile_manage_view import ProfileManageView
from reset_password_view import ResetPasswordView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #Creating profile should have which app code made the request so that it will redirect to that view
    url(r'^$', RegisterView.as_view(), name='uim.register.create.home'),
    url(r'^(?P<app_code>\d{1})/$', RegisterView.as_view(), name='uim.register.create.with.app'),
    url(r'^create/(?P<app_code>\d{1})/$', RegisterView.as_view(), name='uim.register.create.with.path.app'),
    
    #Registeration Email Verifications from web form.
    url(r'^verify/(?P<tpid>\d+)/$', VerifyView.as_view(), name='uim.register.token.verify'),
    #Re-send email verify token
    url(r'^verify/resend/(?P<tpid>\d+)/$', ResendVrfyEmailView.as_view(), name='uim.register.token.verify.resend.mail'),
    #Change Email
    url(r'^verify/change/(?P<tpid>\d+)/$', ChangeEmailView.as_view(), name='uim.register.token.verify.change.mail'),
    
    #First time edit profile
    url(r'^uiwelcome/$', WelcomeView.as_view(), name='account.uiwelcome'),
    #Contact Import Third Party
    url(r'^contacts/$', ContactImporter.as_view(), name='uim.contact.third.party.import'),
    
    #Once Contact Avaialable by provider process them
    url(r'^contacts/invite/$', InviteEmailContact.as_view(), name='account.uiwelcome.contacts.invite'),
    #Reset password request will be landed here
    url(r'^forgotPassword/$', ForgotPasswordView.as_view(), name='account.forgot.password'),
    #Reset Pass word
    url(r'^resetPassword/$', ResetPasswordView.as_view(), name='account.reset.password'),
    #Create Page
    url(r'^createPage/$', CreatePage.as_view(), name='account.create.page'),
    #Manage Profile
    url(r'^manageProfile/$', ProfileManageView.as_view(), name='account.manage.profile'),
    (r'^facebook/', include('facebook_sdk.urls')),
    #Upload file
    (r'^upload/', include('file_uploader.urls')),
    #location
    (r'^location/', include('locationservice.urls')),
    #Settings
    (r'^setting/', include('profile_settings.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
