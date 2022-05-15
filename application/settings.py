from pathlib import Path
import os, sys

BASE_DIR = Path(__file__).resolve().parent.parent   # 当前目录地址
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))  # apps加入环境

SECRET_KEY = 'django-insecure-nomdt7&@f=trl6)d)ti&i-5q+*4#)uob^09huy01g3#1d2t)%!'

DEBUG = True

AUTH_USER_MODEL = 'smpd.UserProfile'

ALLOWED_HOSTS = ['*' ]

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.smpd',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'application.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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


# 国际化
LANGUAGE_CODE = 'zh-hans' # 语言
TIME_ZONE = 'Asia/Shanghai'# 时间
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')# 设置文件上传的目录和外部访问的路径
MEDIA_URL = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',     #   设置访问权限为只读
        # 'rest_framework.permissions.IsAuthenticated',             #   设置访问权限为必须是用户
        # 'rest_framework.permissions.IsAuthenticated',             #    IsAuthenticated 仅通过认证的用户
        'rest_framework.permissions.AllowAny',                    #   AllowAny 允许所有用户
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',#生成api文档
}

"""
日志配置
"""
SERVER_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'server.log')
ERROR_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'error.log')
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))

STANDARD_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'
CONSOLE_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': STANDARD_LOG_FORMAT
        },
        'console': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'file': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file':{
            'level':'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':SERVER_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 5,  # 最多备份5个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 3,  # 最多备份3个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            # 'class':'ColorStreamHandler.ColorStreamHandler',
        },
  },
  'loggers': {
    # default
    '':{
        'handlers': ['console','error','file'],
        'level': 'INFO',
    },
    # 数据库相关日志
    'django.db.backends': {
        'handlers': ['console'],
        'propagate': True,
        'level':'DEBUG',
    },
  }
}