"""Django settings for the Open Asset Platform (OAP) backend.

All configuration is read from environment variables (12-factor). Secret values
are read from files referenced by *_FILE variables so that Docker secrets can be
mounted without exposing credentials in the environment or in logs.
"""

from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _read_secret(name: str, file_var: str, default: str = "") -> str:
    """Return the secret value from the env var or its referenced file."""
    path = os.environ.get(file_var, "")
    if path and os.path.exists(path):
        return Path(path).read_text(encoding="utf-8").strip()
    return os.environ.get(name, default)


def _csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _bool(value: str, default: bool = False) -> bool:
    if not value:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


SECRET_KEY = _read_secret("DJANGO_SECRET_KEY", "DJANGO_SECRET_KEY_FILE", "")
if not SECRET_KEY:
    # Development fallback only; production must provide a secret via file.
    SECRET_KEY = "dev-insecure-do-not-use-in-production"

DEBUG = _bool(os.environ.get("DJANGO_DEBUG", "false"))

ALLOWED_HOSTS = _csv(os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1"))

CSRF_TRUSTED_ORIGINS = _csv(os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "http://localhost:8080"))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    # OAP bounded contexts (dependency order: core -> platforms -> events -> assets ->
    # telemetry -> plugins -> connectivity -> dashboards -> spatial)
    "core",
    "platforms",
    "events",
    "assets",
    "telemetry",
    "plugins",
    "connectivity",
    "dashboards",
    "spatial",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

AUTH_USER_MODEL = "core.User"

# --- Database -----------------------------------------------------------
DB_ENGINE = os.environ.get("DB_ENGINE", "postgresql")
if DB_ENGINE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("SQLITE_PATH", str(BASE_DIR / "oap.sqlite3")),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "oap"),
            "USER": os.environ.get("DB_APP_USER", "oap_app"),
            "PASSWORD": _read_secret("DB_APP_PASSWORD", "DB_APP_PASSWORD_FILE"),
            "HOST": os.environ.get("DB_HOST", "db"),
            "PORT": os.environ.get("DB_PORT", "5432"),
            "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),
            "OPTIONS": {"sslmode": os.environ.get("DB_SSLMODE", "prefer")},
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Auth / DRF ---------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "core.pagination.StandardPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "core.errors.api_exception_handler",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

from datetime import timedelta  # noqa: E402

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.environ.get("AUTH_ACCESS_MINUTES", "30"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.environ.get("AUTH_REFRESH_DAYS", "7"))),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Open Asset Platform API",
    "DESCRIPTION": (
        "Contratos REST versionados de OAP. Generado con drf-spectacular; "
        "regenerar con `manage.py spectacular --file docs/contracts/openapi.yaml --validate`."
    ),
    "VERSION": "1.0.0",
}

# --- CORS ---------------------------------------------------------------
CORS_ALLOWED_ORIGINS = _csv(os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:8080"))
CORS_ALLOW_CREDENTIALS = True

# --- i18n / tz ----------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Security (production hardening; off by default in dev) -----------------
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
SECURE_SSL_REDIRECT = _bool(os.environ.get("SECURE_SSL_REDIRECT", "false"))
SESSION_COOKIE_SECURE = _bool(os.environ.get("SESSION_COOKIE_SECURE", "false"))
CSRF_COOKIE_SECURE = _bool(os.environ.get("CSRF_COOKIE_SECURE", "false"))
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
if _bool(os.environ.get("TRUST_X_FORWARDED_PROTO", "false")):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --- OAP application settings ------------------------------------------
OAP_ENV = os.environ.get("OAP_ENV", "development")
OAP_PUBLIC_URL = os.environ.get("OAP_PUBLIC_URL", "http://localhost:8080")
OAP_DEFAULT_TIMEZONE = os.environ.get("OAP_DEFAULT_TIMEZONE", "UTC")
OAP_MULTI_TENANT = _bool(os.environ.get("OAP_MULTI_TENANT", "true"))

# Telemetry defaults (seed-once; per-agent and per-attribute overrides persist in DB).
TELEMETRY_DEFAULT_STORAGE_MODE = os.environ.get("TELEMETRY_DEFAULT_STORAGE_MODE", "on_change")
TELEMETRY_DEFAULT_ABSOLUTE_EPSILON = float(os.environ.get("TELEMETRY_DEFAULT_ABSOLUTE_EPSILON", "0"))
TELEMETRY_DEFAULT_MAX_SAMPLES = int(os.environ.get("TELEMETRY_DEFAULT_MAX_SAMPLES", "60"))
TELEMETRY_DEFAULT_WINDOW = os.environ.get("TELEMETRY_DEFAULT_WINDOW", "PT1H")
TELEMETRY_DEFAULT_WINDOW_STRATEGY = os.environ.get("TELEMETRY_DEFAULT_WINDOW_STRATEGY", "first")
TELEMETRY_MAX_CLOCK_SKEW_SECONDS = int(os.environ.get("TELEMETRY_MAX_CLOCK_SKEW_SECONDS", "300"))
TELEMETRY_LATE_EVENT_POLICY = os.environ.get("TELEMETRY_LATE_EVENT_POLICY", "reject")

# Plugin bootstrap (seed-once).
PLUGINS_BOOTSTRAP_MODE = os.environ.get("PLUGINS_BOOTSTRAP_MODE", "once")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "plain"},
    },
    "root": {"handlers": ["console"], "level": os.environ.get("OAP_LOG_LEVEL", "INFO")},
}
