import os

AUTH_USER_MODEL = 'irekua_database.User'


IREKUA_DATABASE_APPS = (
    [
        'irekua_database',
        'django.contrib.postgres',
        'django.contrib.gis',
    ]
)


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.environ.get('IREKUA_DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('IREKUA_DATABASE_PORT', '5432'),
        'NAME': os.environ.get('IREKUA_DATABASE_NAME', 'irekua'),
        'USER': os.environ.get('IREKUA_DATABASE_USER', 'irekua'),
        'PASSWORD': os.environ.get('IREKUA_DATABASE_PASSWORD', ''),
    }
}
