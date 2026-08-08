from .base import *
import dj_database_url

# =====================
# Core
# =====================
SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# =====================
# Database
# =====================
DATABASES = {
    "default": dj_database_url.parse(
        env("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
# =====================
# Security
# =====================
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# =====================
# Static files
# =====================
MIDDLEWARE.insert(
    1,
    "whitenoise.middleware.WhiteNoiseMiddleware",
)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
