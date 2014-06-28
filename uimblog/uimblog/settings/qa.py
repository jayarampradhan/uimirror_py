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

# Logging
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
            'filename':  "%s/logs/uim_challenge.log" %SITE_ROOT,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'uimblog': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'filters': []
        },
        'ui_utilities': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'filters': []
        },
        'django.request': {
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
