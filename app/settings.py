import os
from unipath import Path
from decouple import config
import dj_database_url



BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEBUG=True

ALLOWED_HOSTS=['*']


SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'carne_db5',
        'HOST':'localhost',
        'PORT':'5432',
        'USER': 'florm2496',
        'PASSWORD':'pan1994245',
    }
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'applications.bases',
    'applications.productos',
    'applications.compras',
    'applications.ventas',
    'rest_framework',
    'applications.apis',
    'applications.reses',
    'applications.caja',
    #'applications.carne',
    'django_userforeignkey'
   
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_userforeignkey.middleware.UserForeignKeyMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'




# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE='America/Argentina/Buenos_Aires'


STATIC_ROOT=os.path.join(BASE_DIR ,'staticfiles')
STATIC_URL = '/static/'
#estas configuraciones se hicieron para el deploy en heroku
STATIICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = (os.path.join(BASE_DIR ,'static'),)


#STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'




db_from_env=dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)