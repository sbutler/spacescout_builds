# Local settings for server_proj project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Values can be one of 'all_ok' or 'oauth'. If using 'oauth', client applications will need an oauth key/secret pair.
SPOTSEEKER_AUTH_MODULE = 'spotseeker_server.auth.all_ok'

# Custom validation can be added by adding SpotForm and ExtendedInfoForm to org_forms and setting them here.
SPOTSEEKER_SPOT_FORM = 'spotseeker_server.org_forms.uiuc_spot.UIUCSpotForm'
SPOTSEEKER_SPOTEXTENDEDINFO_FORM = 'spotseeker_server.org_forms.uiuc_spot.SpotExtendedInfoForm'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'server.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

LDAP_INFO = {
    # Campus LDAP Server
    'url':'ldap.uiuc.edu',
    # Search Root for finding people.
    'person_ou':'ou=people,DC=UIUC,DC=EDU',
# Campus LDAP Username and Password
    'user':'CN=...,DC=ad,DC=uillinois,DC=edu',
    'password':'',
}

SPOTSEEKER_SEARCH_FILTERS = (
#    'spotseeker_server.org_filters.uiuc_search.Filter',
    'spotseeker_server.org_filters.uw_search.Filter',
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
#TIME_ZONE = 'America/Chicago'
USE_TZ = False
TIME_ZONE = 'America/Chicago'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

