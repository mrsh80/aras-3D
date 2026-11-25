import os
from pathlib import Path


# مسیر اصلی پروژه
BASE_DIR = Path(__file__).resolve().parent.parent


# تنظیمات امنیتی
# در محیط عملیاتی، این مقادیر باید از متغیرهای محیطی دریافت شوند.
# تنظیمات امنیتی
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-development-only-change-before-deployment",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

# تنظیمات امنیتی مخصوص محیط عملیاتی
if not DEBUG:
    if SECRET_KEY.startswith("django-insecure-"):
        raise ValueError(
            "در محیط عملیاتی باید DJANGO_SECRET_KEY را تنظیم کنید."
        )

    if not ALLOWED_HOSTS:
        raise ValueError(
            "در محیط عملیاتی باید DJANGO_ALLOWED_HOSTS را تنظیم کنید."
        )

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # فقط پس از اطمینان از پیکربندی صحیح HTTPS فعال شود.
    SECURE_HSTS_SECONDS = 0


# برنامه‌های فعال Django
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # برنامه اصلی سایت Aras 3D
    "catalog.apps.CatalogConfig",
]


# میان‌افزارها
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# آدرس‌دهی اصلی پروژه
ROOT_URLCONF = "config.urls"


# تنظیمات قالب‌های HTML
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# تنظیمات سرور
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# پایگاه داده
# در محیط توسعه از SQLite استفاده می‌کنیم.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# اعتبارسنجی گذرواژه‌های پنل مدیریت
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


# زبان و منطقه زمانی
LANGUAGE_CODE = "fa-ir"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True


# فایل‌های استاتیک: CSS، JavaScript و تصاویر ثابت
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "catalog" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# تصاویر و فایل‌های رسانه‌ای محصولات
MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# تنظیمات ایمیل
# فعلاً ایمیل‌ها در محیط توسعه داخل ترمینال نمایش داده می‌شوند.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# نوع کلید اصلی مدل‌ها
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"