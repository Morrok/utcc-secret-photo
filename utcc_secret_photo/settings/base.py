from pathlib import Path
import environ
import os

env_schema = dict(
    DEBUG=(bool, False),
    LANGUAGE_CODE=(str, 'en-us'),
    TIME_ZONE=(str, 'UTC'),
    USE_I18N=(bool, True),
    USE_L10N=(bool, True),
    USE_TZ=(bool, True),
    # STATIC_URL=(str, 'static/'),
    LOGIN_URL=(str, 'login/'),
    # DEFAULT_AUTO_FIELD=(str, 'django.db.models.BigAutoField'),
    LOG_LEVEL=(str, 'INFO'),
    # MONGO_URI=(str, 'mongodb://localhost:27017/sao-local'),
    DB_NAME=(str, 'postgres'),
    DB_USER=(str, 'postgres'),
    DB_PASSWORD=(str, '1234'),
    DB_HOST=(str, 'localhost'),
    DB_PORT=(str, '5432'),
    # GDCC_HOST=(str, 'localhost'),
    # PROMETHEUS_HOST=(str, 'localhost'),
    # HTTP Retry
    # HTTP_RETRIES_MAX_REQUESTS=(int, 15),
    # HTTP_RETRIES_MAX_REQUESTS_BPMN_SLOWNESS=(int, 5),
    # HTTP_RETRIES_BACKOFF_FACTOR=(float, 0.2),
    # HTTP_RETRIES_STATUS_CODE=(list, [502, 503, 504]),
    # HTTP_RETRIES_METHODES=(list, ['get', 'post', 'put', 'delete']),
    # GDCC_API_UPDATE_PROMETHEUS_HOST=(str, 'localhost'),
    # ALLOW_MORE_THAN_ONE=(bool, False),
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
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
    'rest_framework',
    'django_extensions',
    'django.contrib.humanize',
    'django_bootstrap5',
    'secret_photo'
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

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
