from os.path import join, dirname, pardir, abspath

PROJECT_ROOT = abspath(join(dirname(__file__), pardir))
DEV_TMP_DIR = join(PROJECT_ROOT, pardir, '.devtmp')

DEBUG = False

ADMINS = ()
MANAGERS = ADMINS

# new Django security settings
ALLOWED_HOSTS = ['*']

# NOTE: development settings, overwrite it in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(DEV_TMP_DIR, 'devel.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# NOTE: development settings, overwrite it in production
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Media and static settings, development
MEDIA_ROOT = join(DEV_TMP_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = join(DEV_TMP_DIR, 'static')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'project_static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# NOTE: development settings, use real secret key in your production
SECRET_KEY = 'xx5%sl1pr3vz7$mv-zej*8!(=lw=&if5%i=!5%zy(*fjuc))5b'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.core.context_processors.request',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'ndbattle.context_processors.settings_variables',
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
    # 'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
)

ROOT_URLCONF = 'ndbattle.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.humanize',

    'raven.contrib.django.raven_compat',

    'ndbattle',
    'ndstats',

    'social_django',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SESSION_COOKIE_DOMAIN = ''

AUTHENTICATION_BACKENDS = (
    'social_core.backends.steam.SteamOpenId',
    'django.contrib.auth.backends.ModelBackend',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    # 'planner.pipeline.user_update_handler',
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'

QUEUE_NAME = 'ndstats'
QUEUE_LOCK = 'ndslock'
