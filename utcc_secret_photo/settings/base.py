from pathlib import Path
import environ
import os
from datetime import timedelta

env_schema = dict(
    DEBUG=(bool, False),
    LANGUAGE_CODE=(str, 'en-us'),
    TIME_ZONE=(str, 'UTC'),
    USE_I18N=(bool, True),
    USE_L10N=(bool, True),
    USE_TZ=(bool, True),
    STATIC_URL=(str, 'static/'),
    LOGIN_URL=(str, 'login/'),
    LOG_LEVEL=(str, 'INFO'),
    DB_NAME=(str, 'postgres'),
    DB_USER=(str, 'postgres'),
    DB_PASSWORD=(str, '1234'),
    DB_HOST=(str, 'localhost'),
    DB_PORT=(str, '5432'),
    AUTHEN_SECRET_KEY=(str, 'RL72rg9bPzajnmwP9cB8vrKuJaIN6Iy6N99gncjD8QE='),
    EMAIL_HOST=(str, 'localhost'),
    EMAIL_PORT=(str, '1025'),
    EMAIL_USE_TLS=(bool, False),
    EMAIL_HOST_USER=(str, 'your-email@gmail.com'),
    EMAIL_HOST_PASSWORD=(str, 'your-gmail-password'),
    WEB_PROTOCAL=(str, 'http'),
    WEB_DOMAIN_NAME=(str, 'localhost:8000'),
    IMAGE_SECRET_KEY=(str, 'yqiLYf3TF44eJGUkF7adm0K8pWs9iKg62FI6Wkmj0to=')
    # HTTP Retry
    # HTTP_RETRIES_MAX_REQUESTS=(int, 15),
    # HTTP_RETRIES_MAX_REQUESTS_BPMN_SLOWNESS=(int, 5),
    # HTTP_RETRIES_BACKOFF_FACTOR=(float, 0.2),
    # HTTP_RETRIES_STATUS_CODE=(list, [502, 503, 504]),
    # HTTP_RETRIES_METHODES=(list, ['get', 'post', 'put', 'delete']),
    # CORS_ORIGIN_ALLOW_ALL=(bool, False),
    # CORS_ORIGIN_WHITELIST=(list, ['https://localhost:8081'])
)

root = environ.Path(__file__) - 3
env_src_file = root('.env')
if os.path.exists(env_src_file):
    environ.Env.read_env(env_file=env_src_file)
env = environ.Env(**env_schema)
for key in env_schema:
    exec("{} = env('{}')".format(key, key))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--o-5t-3&z*8qj0_2ck*a-2oj8aqhn6=h@0(4(urke-((8y#11='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'django.contrib.humanize',
    'django_bootstrap5',
    'secret_photo'
    # 'secret_photo.apps.SecretPhotoConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'utcc_secret_photo.urls'

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
                # 'secret_photo.views.base_html',
            ],
        },
    },
]

WSGI_APPLICATION = 'utcc_secret_photo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'psqlextra.backend',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  # or the URL of your frontend application
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

AUTH_USER_MODEL = 'secret_photo.CustomUser'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
PASSWORD_RESET_TIMEOUT = 60
