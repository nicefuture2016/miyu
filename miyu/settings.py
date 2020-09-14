import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'm39*5bysb%sye+_t$3veuqy001g9ftl#4p&1%_h8#k_f7@bole'
APP_KEY = 'xxxxx'
APP_SECRET = 'xxxxxxx'

# COS 地址
COS = 'https://img-1256517108.cos.ap-chengdu.myqcloud.com/'
BANNER = 'banner.jpg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'administrator.apps.AdministratorConfig',
    'rest_framework',
    'django_filters',
    #'rest_framework.authtoken',
    'corsheaders',
    'django_summernote'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'miyu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'miyu.wsgi.application'

SEARCH_RANK = 'SEARCH_RANK'
#
# MySQL 配置

REDIS_SERVER = os.environ['DBHOST']
REDIS_PORT = 6379
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DBNAME'],
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASSWORD'],
        'HOST': os.environ['DBHOST'],
        'PORT': 3306,
        'DEFAULT_CHARSET': 'utf-8',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
'''
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:6379/0"%os.environ['DBHOST'],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    },
}
'''
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

# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
LOG_DIR = os.environ['LOGDIR']

# 短信配置
APPID = 'xxxxx'
APPKEY = 'xxxxx'
TEMPLATEID = xxxxxx
SIGN = '秋子互娱'
SMS_TIME = 2

# 定义后台登录的地址
LOGIN_URL = '/administrator/sys_login/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'handlers': {
        # 终端调试日志
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        # 自定义错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR,'error.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 1,
            'formatter': 'verbose'
        },
        'default': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR,'all.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 1,
            'formatter': 'verbose',
        },
        # 系统错误日志
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR,'request.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'miyu.api.views': {
            'handlers': ['error'],
            'level': 'INFO',
            'propagate': False
        },
        'miyu.api.common.func': {
            'handlers': ['error'],
            'level': 'INFO',
            'propagate': False
        },
        'miyu.api.utils.authentication': {
            'handlers': ['error'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
SUMMERNOTE_CONFIG = {
    'width': '100%',
    'height': '480',
    'disable_upload': False,
    'lang': 'zh-CN',
}

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES':{
        'default': '200/d', # 一天200次
        'data': '10/m',     # 每分钟10次
    }
}
