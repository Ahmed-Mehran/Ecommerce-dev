

## Django environ setup

import environ

env = environ.Env()

environ.Env.read_env()



from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

#CSRF_TRUSTED_ORIGINS = ['']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'store',   # StoreDjango app

    'cart',     # Cart django app

    'account',   # Account Django app

    'payment',   # Payment Django app


    'crispy_forms', ## both for crispy forms
    "crispy_bootstrap5",

    'storages',  ## S3
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'store.views.categories',

                'cart.context_processors.cart',   ## first cart is name of our so go in cart app, look for context_processors file and in that file look
                                                 ## for cart function
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'   ## here with static url we are letting django know about the static folder

## now we will let django know where to connect to it
STATICFILES_DIRS = [BASE_DIR/ 'static']


MEDIA_URL = '/media/'  ## url for media folder under static folder

MEDIA_ROOT = BASE_DIR/ 'static/media'  # location for media folder





# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

## SMTP CONFIGURATION

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  

EMAIL_HOST = 'smtp.gmail.com' 

EMAIL_PORT = '587'  

EMAIL_USE_TLS = 'True'  



EMAIL_HOST_USER = env('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')




###    AMAZON CREDENTIALS


AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID') # - Enter your AWS Access Key ID HERE
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY') # - Enter your AWS Secret Access Key ID HERE


# AWS S3 CONFIGURATION

# Django 4.2 > Storage configuration for Amazon S3



AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')   


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_FILE_OVERWRITE = False




##  Allow PayPal Popups

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'