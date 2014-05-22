# Django settings for web_proj project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

FEEDBACK_EMAIL_RECIPIENT = (
    'illinispaces+feedback@ics.illinois.edu',
)
DEFAULT_FROM_EMAIL = 'illinispaces@ics.illinois.edu'

AUTHENTICATION_BACKENDS = (
    'shibboleth.backends.ShibbolethRemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_SSL', 'on')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SS_LOCATIONS = {
    'uiuc': {
            'NAME': 'Urbana-Champaign',
            'CENTER_LATITUDE': '40.107471',
            'CENTER_LONGITUDE': '-88.227081',
            'ZOOM_LEVEL': '16',
            }
}
SS_DEFAULT_LOCATION = 'uiuc'

SHOW_IOS_SMART_BANNER = False

# This is the list of zoom levels for which the spaces are clustered by building on the map.  An empty list means no building clustering
SS_BUILDING_CLUSTERING_ZOOM_LEVELS = []

# The ratio (distance between spaces / diagonal distance visible on map) below which spaces will cluster
# together on the map when not clustering by building
SS_DISTANCE_CLUSTERING_RATIO = .1

SHIBBOLETH_ATTRIBUTE_MAP = {
    'HTTP_UID':         (True, 'username'),
    'HTTP_MAIL':        (True, 'email'),
    'HTTP_ISMEMBEROF':  (True, 'groups[]'),
}
LOGIN_URL = '/Shibboleth.sso/Login'
SHIBBOLETH_LOGOUT_URL = '/Shibboleth.sso/Logout?target=%s'

SPACESCOUT_SEARCH_FILTERS = (
    'spacescout_web.org_filters.uiuc_search.Filter',
)

GMAPS_API_KEY = 'AIzaSyB6eqWhhGQWvtZt_Hm9lfe9jJHKzpmOQXo'
GA_TRACKING_ID = 'UA-51282505-1'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
USE_TZ = False
TIME_ZONE = 'America/Chicago'

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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'spacescout_web.context_processors.show_ios_smart_banner',
    'spacescout_web.context_processors.less_not_compiled',
    'spacescout_web.context_processors.is_mobile',
    'spacescout_web.context_processors.ga_tracking_id',
    'spacescout_web.context_processors.gmaps_api_key',
    'shibboleth.context_processors.login_link',
    'shibboleth.context_processors.logout_link',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'spacescout_web.middleware.unpatch_vary.UnpatchVaryMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'spacescout_web.middleware.shibboleth_sso.ShibbolethRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'mobility.middleware.DetectMobileMiddleware',
    'mobility.middleware.XMobileMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'web_proj.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'web_proj.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'shibboleth',
    'spacescout_web',
    'compressor',
    'templatetag_handlebars',
)

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

#Django Compressor - LessCSS Compiler
COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (('text/less', 'lessc {infile} {outfile}'),)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'spacescout-web'
    }
}

try:
    from local_settings import *
except ImportError:
    pass
