import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ynx2%@$creosl*hn5)7kr)srxqyf+8&#(wv8npifkc+92zwz9='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
AUTHENTICATION_BACKENDS = (
    'apps.users.views.CustomBackend',
)

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.conf',
    'import_export',
    'apps.users',
    'apps.courses',
    'apps.organization',
    'apps.operation',
    'apps.utils',
    'captcha',
    'pure_pagination',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mooc_example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mooc_example.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# 空白处填写数据库信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': ''
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "users.UserProfile"
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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
IMPORT_EXPORT_USE_TRANSACTIONS = True

# admin theme
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_DEFAULT_THEME = 'light.css'

# mail setting
# 空白处填写邮件服务器信息
EMAIL_HOST = ""
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False

MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')

# pure_pagination
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}
