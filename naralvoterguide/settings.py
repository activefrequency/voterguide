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
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.herokuapp.com').split(':')

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
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR.child('templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'voterguide.context_processors.google_analytics',
                'voterguide.context_processors.branding',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
    'flat',
    'django.contrib.admin',
    'django.contrib.gis',
    'django_extensions',
    'debug_toolbar',
    'compressor',
    'front',
    'voterguide',
)

# Disable Django Debug Toolbar by default - override in settings_local if you want to turn it on
INTERNAL_IPS = ()

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
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = os.environ.get('SERVER_EMAIL')

# GeoDjango settings
# GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH', '')
# GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH', '')

GEOS_LIBRARY_PATH = "{}/libgeos_c.so".format(os.environ.get('GEOS_LIBRARY_PATH'))
GDAL_LIBRARY_PATH = "{}/libgdal.so".format(os.environ.get('GDAL_LIBRARY_PATH'))
PROJ4_LIBRARY_PATH = "{}/libproj.so".format(os.environ.get('PROJ4_LIBRARY_PATH'))

SUNLIGHT_API_KEY = os.environ.get('SUNLIGHT_API_KEY', '')

VOTERGUIDE_SETTINGS = {
    'DEFAULT_STATE': os.environ.get('VOTERGUIDE_DEFAULT_STATE', 'MA'),
    'DEFAULT_YEAR': os.environ.get('VOTERGUIDE_DEFAULT_YEAR', '2014'),
    'SHOW_ENDORSEMENTS': bool(os.environ.get('VOTERGUIDE_SHOW_ENDORSEMENTS', '1') == '1'),
    'BRANDING': {
        'ORG_NAME': os.environ.get('VOTERGUIDE_BRANDING_ORG_NAME', 'NARAL Pro-Choice Massachusetts'),
        'ORG_URL': os.environ.get('VOTERGUIDE_BRANDING_ORG_URL', 'http://www.prochoicemass.org'),
        'FACEBOOK_URL': os.environ.get('VOTERGUIDE_BRANDING_FACEBOOK_URL', 'https://www.facebook.com/prochoicemass'),
        'TWITTER_URL': os.environ.get('VOTERGUIDE_BRANDING_TWITTER_URL', 'https://www.twitter.com/prochoicemass'),
        'CONTACT_URL': os.environ.get('VOTERGUIDE_BRANDING_CONTACT_URL', 'http://www.prochoicemass.org/about-us/contact.shtml'),
        'REGISTER_VOTE_URL': os.environ.get('VOTERGUIDE_BRANDING_REGISTER_VOTE_URL', 'http://www.sec.state.ma.us/ele/eleifv/howreg.htm'),
        'DONATE_URL': os.environ.get('VOTERGUIDE_BRANDING_DONATE_URL', 'http://www.prochoicemass.org/donate/'),
        'VOLUNTEER_EMAIL': os.environ.get('VOTERGUIDE_BRANDING_VOLUNTEER_EMAIL', 'choice@prochoicemass.org'),
        'LOGO_IMG': os.environ.get('VOTERGUIDE_BRANDING_LOGO_IMG', 'logo-ma.png'),
        'SHOW_STATEWIDE_ENDORSEMENTS': bool(os.environ.get('VOTERGUIDE_SHOW_STATEWIDE_ENDORSEMENTS', '1') == '1'),
        'SHOW_STATEWIDE': bool(os.environ.get('VOTERGUIDE_SHOW_STATEWIDE', '1') == '1'),
    }
}

GOOGLE_ANALYTICS_PROPERTY_ID = os.environ.get('GOOGLE_ANALYTICS_PROPERTY_ID', '')

# turn on "Placeholder mode" - hijacks to placeholder page
SHOW_PLACEHOLDER = bool(os.environ.get('VOTERGUIDE_SHOW_PLACEHOLDER', '0') == '1')


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
