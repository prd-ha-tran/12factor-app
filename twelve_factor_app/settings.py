"""
Django settings for twelve_factor_app project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import configparser
import logging.config
import os
from pathlib import Path

app_config = configparser.ConfigParser()

app_config.read(os.environ["12FACTOR_APP_CONFIG"])

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@5gq8-(arl!ejdi1t(-t=ifj3!x!5b9sc#82dk7i+&j7vt4ltl"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("12FACTOR_APP_DEBUG") == "TRUE"

DISABLE_WHITENOSE = app_config["default"].get("disable_whitenose") == "1"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

_whitenose_middleware = [] if DISABLE_WHITENOSE else ["whitenoise.middleware.WhiteNoiseMiddleware"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    *_whitenose_middleware,
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "twelve_factor_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "twelve_factor_app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "assets/"
if not DISABLE_WHITENOSE:
    STATIC_ROOT = BASE_DIR / "assets"
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING_CONFIG = None


def config_logging(app_config):
    if "keys" in app_config["loggers"]:
        loggers_keys = app_config["loggers"]["keys"]
    else:
        loggers_keys = ""
    if "root" not in loggers_keys:
        app_config.set(
            "loggers", "keys", loggers_keys + ",root" if loggers_keys != "" else "root"
        )
        app_config.add_section("logger_root")
        app_config["logger_root"]["handlers"] = ""
        app_config["logger_root"]["level"] = "WARNING"
    if "formatters" not in app_config:
        app_config.add_section("formatters")
        app_config["formatters"]["keys"] = ""
    if "handlers" not in app_config:
        app_config.add_section("handlers")
        app_config["handlers"]["keys"] = ""


try:
    config_logging(app_config)
except KeyError:
    app_config.add_section("loggers")
    config_logging(app_config)

logging.config.fileConfig(app_config)


GUNICORN_CONFIGS = {
    **dict(app_config["gunicorn"]),
    "logger_class": "twelve_factor_app.gunicorn.logger.GLogger",
    "accesslog": "-",
}

WAIT_SECS = float(app_config["default"]["wait_secs"])

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS.extend(
    [host.strip() for host in app_config["default"].get("allowed_hosts", "").split(",") if host.strip()]
)
