# -*- coding: utf-8 -*-
# from os import getenv
import urlparse

from env_utils import get_env

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'side_effects',
    'test_app'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

SECRET_KEY = "side-effects"

ROOT_URLCONF = 'urls'

APPEND_SLASH = True

STATIC_URL = '/static/'

TIME_ZONE = 'UTC'

USE_TZ = True

SITE_ID = 1

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 'null': {
        #     'level': 'DEBUG',
        #     'class': 'django.utils.log.NullHandler',
        # },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'side_effects': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        # 'django': {
        #     'handlers': ['console'],
        #     'level': getenv('LOGGING_LEVEL_DJANGO', 'WARNING'),
        #     'propagate': False,
        # },
        # 'django.db.backends': {
        #     'level': 'ERROR',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        'onfido': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# And we're using redis for queued tasks, either locally or via redistogo on Heroku
redis_url = urlparse.urlparse(get_env('REDIS_URL'))

RQ_QUEUES = {
    'side_effects': {
        'HOST': redis_url.hostname,
        'PORT': redis_url.port,
        'DB': 0,
        'PASSWORD': redis_url.password,
    },
}

assert DEBUG is True, "This project is only intended to be used for testing."
