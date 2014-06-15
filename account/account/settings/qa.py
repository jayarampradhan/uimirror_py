"""
    QA settings and globals.
"""

from common import *
from qa_property import *

########## DEBUG CONFIGURATION
DEBUG = True
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'uimirror',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '192.168.1.6',
        'PORT': '3306',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
########## END CACHE CONFIGURATION


########## DJANGO-DEBUG-TOOLBAR CONFIGURATION
# MIDDLEWARE_CLASSES += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )

# INSTALLED_APPS += (
#     # debug tool bar
#     'django.contrib.staticfiles',
#     'debug_toolbar',
# )

# IPs allowed to see django-debug-toolbar output.
INTERNAL_IPS = ('127.0.0.1',)

# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
# ]

# DEBUG_TOOLBAR_CONFIG = {
#     # If set to True (default), the debug toolbar will show an intermediate
#     # page upon redirect so you can view any debug information prior to
#     # redirecting. This page will provide a link to the redirect destination
#     # you can follow when ready. If set to False, redirects will proceed as
#     # normal.
#     'INTERCEPT_REDIRECTS': False,
# 
#     # If not set or set to None, the debug_toolbar middleware will use its
#     # built-in show_toolbar method for determining whether the toolbar should
#     # show or not. The default checks are that DEBUG must be set to True and
#     # the IP of the request must be in INTERNAL_IPS. You can provide your own
#     # method for displaying the toolbar which contains your custom logic. This
#     # method should return True or False.
# #    'SHOW_TOOLBAR_CALLBACK': None,
# 
#     # An array of custom signals that might be in your project, defined as the
#     # python path to the signal.
#     'EXTRA_SIGNALS': [],
# 
#     # If set to True (the default) then code in Django itself won't be shown in
#     # SQL stacktraces.
#     'ENABLE_STACKTRACES': True,
# 
#     # If set to True (the default) then a template's context will be included
#     # with it in the Template debug panel. Turning this off is useful when you
#     # have large template contexts, or you have template contexts with lazy
#     # datastructures that you don't want to be evaluated.
# #    'SHOW_TEMPLATE_CONTEXT': True,
# 
#     # If set, this will be the tag to which debug_toolbar will attach the debug
#     # toolbar. Defaults to 'body'.
#     # 'INSERT_BEFORE': 'body',
# }
########## END DJANGO-DEBUG-TOOLBAR CONFIGURATION


########## CELERY CONFIGURATION
# INSTALLED_APPS += (
#    'djkombu',
# )

# BROKER_BACKEND = 'djkombu.transport.DatabaseTransport'
# Celery settings
# BROKER_URL = 'redis://127.0.0.1:6379/0'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# BROKER_BACKEND = "redis"
# BROKER_HOST = "localhost"  # Maps to redis host.
# BROKER_PORT = 6379         # Maps to redis port.
# BROKER_VHOST = "0"         # Maps to database number.
# 
# CELERY_RESULT_BACKEND = "redis"
# REDIS_HOST = 6379
# REDIS_PORT = 6379
# REDIS_DB = 0
# 
# CELERY_ALWAYS_EAGER = True
# CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
########## END CELERY CONFIGURATION

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            #'format': '%(levelname)s %(asctime)s %(message)s'
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)-15s] [%(name)-5s] %(levelname)-8s %(message)s'
            
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename':  "%s/logs/uim_account.log" %SITE_ROOT,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'account': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'filters': []
        },
        'ui_utilities': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'filters': []
        },
        'contact_importer': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'filters': []
        },
        'profile_importer': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'filters': []
        },        
        'django.request': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },'facebook_sdk': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {
            'handlers': [],
            'level': 'WARNING',
            'filters': []
        },
    }
}
