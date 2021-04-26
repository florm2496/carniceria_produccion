from .base import *

DEBUG=False

ALLOWED_HOSTS=['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'carniceria',
        'HOST':'localhost',
        'PORT':'5432',
        'USER': 'florm2496',
        'PASSWORD':'pan1994245',
    }
}



STATIC_ROOT=os.path.join(BASE_DIR ,'staticfiles')
STATIC_URL = '/static/'
#estas configuraciones se hicieron para el deploy en heroku

STATICFILES_DIRS = (os.path.join(BASE_DIR ,'static'),)


#STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'



