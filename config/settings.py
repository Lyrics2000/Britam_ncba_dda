
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


import json
file_path = BASE_DIR / 'config.json'

with open(file_path, 'r') as file:
    data = json.load(file)
# SECURITY WARNING: don't run with debug turned on in production!



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "home"
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



INDEV = True
if INDEV:
    DEBUG = data['BRITAM_NCBA_DDA']['UAT']['SECURITY']['DEBUG']
    ALLOWED_HOSTS = data['BRITAM_NCBA_DDA']['UAT']['SECURITY']['ALLOWED_HOSTS']
    SECRET_KEY = data['BRITAM_NCBA_DDA']['UAT']['SECURITY']['SECRET_KEY']
    APIS = data['BRITAM_NCBA_DDA']['UAT']['APIS']
    ROLES = data['BRITAM_NCBA_DDA']['UAT']['ROLES']
else:
    DEBUG = data['BRITAM_NCBA_DDA']['PROD']['SECURITY']['DEBUG']
    ALLOWED_HOSTS = data['BRITAM_NCBA_DDA']['PROD']['SECURITY']['ALLOWED_HOSTS']
    SECRET_KEY = data['BRITAM_NCBA_DDA']['PROD']['SECURITY']['SECRET_KEY']
    APIS = data['BRITAM_NCBA_DDA']['PROD']['APIS']
    ROLES = data['BRITAM_NCBA_DDA']['PROD']['ROLES']
# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = '/static_file/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_file'),
]

STATIC_ROOT = os.path.join('static_cdn')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join('media_cdn')


USERNAME = "info@britam.com"
PASSWORD = "V7@xZ!9tQ#2wL$8rJ%6nP&4m"

import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = os.getenv("LOG_DIR", BASE_DIR / "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Toggle chatty SQL logs per env (DEBUG level)
SQL_LOG_ENABLED = os.getenv("SQL_LOG", "false").lower() in ("1", "true", "yes")


from pathlib import Path

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "with_request_id": {
            "()": "home.logging_extras.RequestIDFilter",
        },
    },
    "formatters": {
        "standard": {
            "()": "home.logging_extras.SafeFormatter",  # <— safe
            "format": "%(levelname)s %(asctime)s %(name)s %(request_id)s %(message)s",
        },
        "concise": {
            "()": "home.logging_extras.SafeFormatter",  # <— safe here too
            "format": "%(levelname)s %(asctime)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "concise",
            "filters": ["with_request_id"],
        },
        "requests_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(Path(LOG_DIR) / "requests.log"),
            "maxBytes": 10_000_000,
            "backupCount": 5,
            "formatter": "standard",
            "filters": ["with_request_id"],
        },
        "responses_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(Path(LOG_DIR) / "responses.log"),
            "maxBytes": 10_000_000,
            "backupCount": 5,
            "formatter": "standard",
            "filters": ["with_request_id"],
        },
        "sql_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(Path(LOG_DIR) / "sql.log"),
            "maxBytes": 20_000_000,
            "backupCount": 5,
            "formatter": "standard",
            "filters": ["with_request_id"],
        },
        "app_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(Path(LOG_DIR) / "app.log"),
            "maxBytes": 20_000_000,
            "backupCount": 5,
            "formatter": "standard",
            "filters": ["with_request_id"],
        },
        "gunicorn_error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(Path(LOG_DIR) / "gunicorn.error.log"),
            "maxBytes": 20_000_000,
            "backupCount": 5,
            "formatter": "standard",
            "filters": ["with_request_id"],
        },
        "gunicorn_access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(Path(LOG_DIR) / "gunicorn.access.log"),
            "maxBytes": 20_000_000,
            "backupCount": 5,
            "formatter": "concise",
            "filters": ["with_request_id"],
        },
    },
    "loggers": {
        "": {  # root
            "handlers": ["console", "app_file"],
            "level": "INFO",
        },
        "reqres.request": {
            "handlers": ["console", "requests_file"],
            "level": "INFO",
            "propagate": False,
        },
        "reqres.response": {
            "handlers": ["console", "responses_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "app_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console", "sql_file"],
            "level": "DEBUG" if SQL_LOG_ENABLED else "WARNING",
            "propagate": False,
        },
        "gunicorn.error": {
            "handlers": ["console", "gunicorn_error_file"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn.access": {
            "handlers": ["console", "gunicorn_access_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
