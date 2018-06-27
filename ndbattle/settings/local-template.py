from os import path

DEBUG = True

DEVTMP = path.join(path.dirname(path.dirname(path.dirname(__file__))), '_devtmp')

MEDIA_ROOT = path.join(DEVTMP, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path.join(DEVTMP, 'db.sqlite3'),
    }
}
