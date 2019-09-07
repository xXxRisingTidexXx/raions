from os.path import dirname, abspath, join
from os import environ
from YamJam import yamjam
from datetime import timedelta

BASE_DIR = dirname(dirname(abspath(__file__)))

config = yamjam(join(BASE_DIR, '.yamjam/config.yaml'))

DEBUG = environ.get('AGONY_DEBUG') is not None

SECRET_KEY = config['secret-key']

ADMINS = list(map(tuple, config['admins']))

ALLOWED_HOSTS = config['allowed-hosts']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'core.apps.CoreConfig',
    'rest_framework',
    'rest_framework_gis'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'agony.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR, 'core/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ]
        }
    }
]

WSGI_APPLICATION = 'agony.wsgi.application'


DATABASES = config['databases']


AUTH_USER_MODEL = 'core.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    }
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [join(BASE_DIR, 'core/static')]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}


JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(hours=12)
}


EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_HOST_USER = config['email']['host-user']

EMAIL_HOST_PASSWORD = config['email']['host-password']

EMAIL_PORT = 587

EMAIL_USE_TLS = True

DEFAULT_FROM_MAIL = EMAIL_HOST_USER

SENDGRID_API_KEY = config['sendgrid']['api-key']

SENDGRID_SANDBOX_MODE_IN_DEBUG = False


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} '
                      '{process:d} {thread:d} {message}',
            'style': '{'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(BASE_DIR, 'logs/access.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
