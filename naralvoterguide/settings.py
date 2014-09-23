from unipath import Path
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Kevin Grinberg', 'kevin@activefrequency.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['voterguide.herokuapp.com', '.prochoicemassvotes.org']

# For Heroku
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://foo:bar@localhost:5432/db')}

# Turn on PostGIS
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Get project base directory (project-level - where settings, project templates, etc. are; manage.py and friends are one level up)
PROJECT_DIR = Path(__file__).ancestor(1)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'staticroot'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v*xir3k@d=cy7)2-05&s(vv%ae0kf05ml1spktrd(be#28ce+1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'naralvoterguide.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'naralvoterguide.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'south',
    'django_extensions',
    'debug_toolbar',
    'compressor',
    'front',
    'voterguide',
)

# Add context processors, rather than overriding defaults
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_TCP
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TCP + (
    'django.core.context_processors.request',
    'voterguide.context_processors.google_analytics',
)

# needed for django-front to work
SOUTH_MIGRATION_MODULES = {
    'front': 'front.south_migrations',
}

# Disable Django Debug Toolbar by default - override in settings_local if you want to turn it on
INTERNAL_IPS = ( )

# to make the classes match up with Bootstrap
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# compress offline
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} > {outfile}'),
)

LOGIN_URL = '/tools/login/'

EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('MANDRILL_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('MANDRILL_APIKEY')
EMAIL_USE_TLS = True
SERVER_EMAIL = 'kevin+naralvoterguide@activefrequency.com'
DEFAULT_FROM_EMAIL = 'kevin+naralvoterguide@activefrequency.com'

SUNLIGHT_API_KEY = os.environ.get('SUNLIGHT_API_KEY', '')

VOTERGUIDE_SETTINGS = {
    'DEFAULT_STATE': os.environ.get('VOTERGUIDE_DEFAULT_STATE', 'MA'),
    'DEFAULT_YEAR': os.environ.get('VOTERGUIDE_DEFAULT_YEAR', '2014'),
}

GOOGLE_ANALYTICS_PROPERTY_ID = os.environ.get('GOOGLE_ANALYTICS_PROPERTY_ID', '')

# turn on "Placeholder mode" - hijacks to placeholder page
SHOW_PLACEHOLDER = os.environ.get('SHOW_PLACEHOLDER', False)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# No file uploads by default

# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
# AWS_PRELOAD_METADATA = True
# AWS_QUERYSTRING_AUTH = False

# DEFAULT_FILE_STORAGE = 'naralvoterguide.s3utils.MediaRootS3BotoStorage'
# MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/media/'

try:
    from settings_local import *
except NameError:
    pass
except ImportError:
    pass

