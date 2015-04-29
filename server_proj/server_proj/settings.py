# Django settings for server_proj project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

OAUTH_AUTHORIZE_VIEW = 'spotseeker_server.views.oauth.authorize'
OAUTH_CALLBACK_VIEW = 'spotseeker_server.views.oauth.callback'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'illinispaces@ics.illinois.edu'
SPACESCOUT_SUGGEST_FROM = 'illinispaces-support@lists.illinois.edu'
SPACESCOUT_REVIEW_MANAGERS = 'illinispaces-support@lists.illinois.edu'

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

# Our locations copied from web_proj.settings. Needed to support the
# uiuc_admin model with its map.
SS_LOCATIONS = {
    'uiuc': {
        'NAME': 'Urbana-Champaign',
        'CENTER_LATITUDE': '40.10527180599617',
        'CENTER_LONGITUDE': '-88.22699516931152',
        'ZOOM_LEVEL': '15',
        'DISTANCE': '1400',
    }
}
SS_DEFAULT_LOCATION = 'uiuc'

# Values can be one of 'all_ok' or 'oauth'. If using 'oauth', client applications will need an oauth key/secret pair.
SPOTSEEKER_AUTH_MODULE = 'spotseeker_server.auth.oauth'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
USE_TZ = False
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

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
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'spotseeker_server.middleware.shibboleth_sso.ShibbolethRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'server_proj.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'server_proj.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'spotseeker-server'
    }
}


CACHE_MIDDLEWARE_SECONDS = 60*60  # Cache what we can for an hour

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'shibboleth',
    'south',
    'spotseeker_server',
    'oauth_provider',
    'uiuc_admin',
    'uiuc_shib',
    'geoposition',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(name)s %(lineno)d "%(message)s"'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
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
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

JSON_PRETTY_PRINT = DEBUG

# Custom validation can be added by adding SpotForm and ExtendedInfoForm to org_forms and setting them here.
SPOTSEEKER_SPOT_FORM = 'spotseeker_server.org_forms.uiuc_spot.UIUCSpotForm'
SPOTSEEKER_SPOTEXTENDEDINFO_FORM = 'spotseeker_server.org_forms.uiuc_spot.UIUCSpotExtendedInfoForm'

SPOTSEEKER_SEARCH_FILTERS = (
    'spotseeker_server.org_filters.uiuc_search.Filter',
    'spotseeker_server.org_filters.uw_search.Filter',
)

# Some Shibboleth configuration. This maps attributes from Shibboleth into
# the attributes on the user in Django.
SHIBBOLETH_ATTRIBUTE_MAP = {
    'HTTP_UID':          (True, 'username'),
    'HTTP_MAIL':        (True, 'email'),
}

LOGIN_URL = '/shib/login'
SHIBBOLETH_LOGIN_URL = '/Shibboleth.sso/Login?target=%s'
SHIBBOLETH_LOGOUT_URL = '/Shibboleth.sso/Logout?target=%s'

try:
    from local_settings import *
except ImportError:
    pass
