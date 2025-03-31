

from pathlib import Path
from datetime import timedelta
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)bf=mdu_&@xb!px+%g)z4u21#7w3q42&tb9hsseoui@c577w$b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['montessori.website','localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'common',
    "hero",
    'facilities',
    "about",
    "career",
    'activities',
    'contact',
    "rest_framework",
    "rest_framework_simplejwt",
    "phonenumber_field",
    "user",
    "corsheaders",
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

ROOT_URLCONF = "montelearning.urls"

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

WSGI_APPLICATION = "montelearning.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'pratice', 
#         'USER': 'test', 
#         'PASSWORD': 'Sagar@1234',
#         'HOST': 'localhost',   
#         'PORT': '3306',  
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR / 'media'

import pymysql

try:
    pymysql.install_as_MySQLdb()
except Exception as e:
    print(f"An error occurred while installing pymysql as MySQLdb: {e}")



REST_FRAMEWORK = {  
    'DEFAULT_AUTHENTICATION_CLASSES': (  
        'rest_framework_simplejwt.authentication.JWTAuthentication',  
    ),
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES' :(
        'rest_framework.renderers.JSONRenderer',
    ),
    # "DEFAULT_THROTTLE_CLASSES":(
    #     'rest_framework.throttling.UserRateThrottle',
    #     'rest_framework.throttling.AnonRateThrottle',
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '10/minute',   # Unauthenticated users can make 10 requests per minute
    #     'user': '500/day',     # Authenticated users can make 100 requests per day
    # }
}  


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # "ROTATE_REFRESH_TOKENS": True,
    # "BLACKLIST_AFTER_ROTATION": True,
    # "AUTH_COOKIE": "access_token",  # Name of the access token cookie
    # "AUTH_COOKIE_SECURE": True,  # Set to True for HTTPS
    # "AUTH_COOKIE_HTTP_ONLY": True,  # Prevent JS access
    # "AUTH_COOKIE_PATH": "/",
    # "AUTH_COO KIE_SAMESITE": "Lax",
}
PHONENUMBER_DEFAULT_REGION = 'NP'

# CORS_ALLOWS_CREDENTIALS=True
CORS_ALLOWED_ORIGINS = [
    "http://montessori.website",  # Allow requests from your domain
         # Allow requests from localhost for development
    "http://localhost:5173",      # Allow requests from React app running on port 5173
]
# CSRF_TRUSTED_ORIGINS = [
#     "https://montessori.website"  # Trust frontend for CSRF protection
# ]

# # Alternatively, if you want to allow all origins (not recommended for production)
# # CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_HEADERS = [
#     "authorization",
#     "content-type",
# ]
# # cookies for the jwt
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SIMPLE_JWT['AUTH_COOKIE_SECURE'] = True  # Custom setting (if you rely on it)
# SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS

# # When behind a proxy (Nginx), tell Django to respect the forwarded protocol:
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]
