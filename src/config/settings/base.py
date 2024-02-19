import importlib.util
import logging
import os
from distutils.util import strtobool

try:
    import environ
except ModuleNotFoundError:
    logging.error("environ module not found")


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return strtobool(value) == 1
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e

    return default_value


def get_list_from_env(text):
    return [item.strip() for item in text.split(",")]


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

APP_NAME = os.getenv("APP_NAME", "bpm_tasks")

is_present_environ = importlib.util.find_spec("environ")
if is_present_environ:
    environ.Env.read_env(os.path.join(BASE_DIR, "../.env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY") or exit(f"SECRET_KEY environment variable is not set.")

# Application definition

BEFORE_DJANGO_APPS = []
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "django_object_actions",
    "rest_framework",
    "corsheaders",
    "debug_toolbar",
]
LOCAL_APPS = [
    "apps.common.apps.CommonConfig",
    "apps.users.apps.UsersConfig",
    "apps.api.apps.ApiConfig",
    "apps.web.apps.WebConfig",
    "apps.tasks.apps.TasksConfig",
]

INSTALLED_APPS = BEFORE_DJANGO_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.servers.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "bpm_db"),
        "USER": os.getenv("DB_USER", "bpm_db"),
        "PASSWORD": os.getenv("DB_PASSWORD", "bpm_db"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": int(os.getenv("DB_PORT", 5432)),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Asia/Almaty"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = os.getenv("STATIC_URL", "/files/static/")
STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join("/files", "static"))
STATICFILES_DIRS = (os.path.join(BASE_DIR, "staticfiles"),)

MEDIA_URL = os.getenv("MEDIA_URL", "/files/media/")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join("/files", "media"))

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
}

CSRF_TRUSTED_ORIGINS = get_list_from_env(
    os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000")
)

ALLOWED_HOSTS = get_list_from_env(os.getenv("ALLOWED_HOSTS", "*"))

AUTH_USER_MODEL = "users.User"


# BPM settings
BPM_HOST = os.getenv("BPM_HOST", "10.61.40.95:9443")
BPM_USERNAME = os.getenv("BPM_USERNAME", "nzh_muratbekov")
BPM_PASSWORD = os.getenv("BPM_PASSWORD", "%\RHhM<4Skru")
BPM_POST_TOKEN_EXPIRE_SECONDS = int(os.getenv("BPM_POST_TOKEN_EXPIRE_SECONDS", 30))
AUTH_TOKEN_EXPIRE_SECONDS = int(os.getenv("AUTH_TOKEN_EXPIRE_SECONDS", 60))


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s"},
        "verbose": {"format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s [%(filename)s:%(lineno)s]"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.getenv("LOGGING_FILE_PATH", os.path.join(BASE_DIR, "logs", "debug.log")),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": os.getenv("LOG_LEVEL", "INFO"),
        },
    },
}


CORS_ALLOWED_ORIGINS = [
    "https://10.61.40.95:9443",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
