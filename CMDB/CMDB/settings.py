"""
Django settings for CMDB project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+7+&!50b$n+!do0__1q(l@ge$7a0m!jjpqj)yv*y!)0yd11i#6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
    'rest_framework',
    'crond',
    'django_celery_beat',
    'django_celery_results',
    'asset',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'web.access_times_limit_middleware.AccessTimesLimitMiddleware',
]

ROOT_URLCONF = 'CMDB.urls'

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

WSGI_APPLICATION = 'CMDB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cmdb',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '10.0.0.61',
        'PORT': "3306",
    }
}
# http://yshblog.com/blog/156
# 也可以把{}等使用json序列化为字符串，存入缓存中
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.0.0.61:6379/1",
        "OPTIONS": {
           "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True
# celery
# 由于celery-4.1.0存在时区bug，必须启用USE_TZ
# raise ValueError("MySQL backend does not support timezone-aware datetimes when USE_TZ is False.")
# ValueError: MySQL backend does not support timezone-aware datetimes when USE_TZ is False.
USE_TZ = True

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://10.0.0.61:6379'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# 这是使用了django-celery默认的数据库调度模型,任务执行周期都被存在你指定的orm数据库中
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# 设置STATIC_URL对应的路径，后面访问127.0.0.1:8000/static/就会访问到STATICFILES_DIRS下的内容
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
# 对应login_required装饰器跳转的登录页面
LOGIN_URL = "/login/"
# 由于自己重写了user表，所以需要在这里添加一条配置
AUTH_USER_MODEL = 'web.MyUser'
# 与用户上传图片相关的配置
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# 中间件中访问频率的限制
ACCESS_TIME = 60
ACCESS_LIMIT = 5
# rest_framework认证配置
# 我们的版本在前面~然后是认证，然后是权限~ 最后是频率~~所以大家要清楚~~
REST_FRAMEWORK = {
    # 配置全局认证
    'DEFAULT_AUTHENTICATION_CLASSES': ["web.rest_auth.MyApiAuth", ],
    # 配置全局权限
    "DEFAULT_PERMISSION_CLASSES": ["web.rest_permission.MyApiPermission"],
    "DEFAULT_THROTTLE_CLASSES": ["web.rest_throttle.MyThrottle"],
        "DEFAULT_THROTTLE_RATES":{
            'WD':'5/m',         #速率配置每分钟不能超过5次访问，WD是scope定义的值，

        }
}
# 需要事先在role表中添加该角色
REST_OWN_PERMISSION_USER_ROLE_CODE = "API_user"
# 下面就是logging的配置
LOGGING = {
    'version': 1,  # 指明dictConnfig的版本，目前就只有一个版本，哈哈
    'disable_existing_loggers': False,  # 表示是否禁用所有的已经存在的日志配置
    'formatters': {  # 格式器
        'verbose': {  # 详细
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {  # 标准
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        },
    },
    # handlers：用来定义具体处理日志的方式，可以定义多种，"default"就是默认方式，
    # "console"就是打印到控制台方式。file是写入到文件的方式，注意使用的class不同
    'handlers': {  # 处理器，在这里定义了两个个处理器
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # 文件重定向的配置，将打印到控制台的信息都重定向出去
            #                                python manage.py runserver >> /home/aea/log/test.log
            # 'stream': open('/home/aea/log/test.log','a'),
            # #虽然成功了，但是并没有将所有内容全部写入文件，目前还不清楚为什么
            'formatter': 'standard'   # 制定输出的格式，注意 在上面的formatters配置里面选择一个，否则会报错
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/project/file.log',  # 这是将普通日志写入到日志文件中的方法，
            'formatter': 'standard'
        },
        'file_rotate': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/project/file_rotate.log',  # 日志输出文件
            'maxBytes': 1024*1024*5,                  # 文件大小
            'backupCount': 5,                         # 备份份数
            'formatter': 'standard',                   # 使用哪种formatters日志格式
        },
        # 上面两种写入日志的方法是有区别的，前者是将控制台下输出的内容全部写入到文件中，这样做的好处就是我们在views代码中的所有print也会写在对应的位置
        # 第二种方法就是将系统内定的内容写入到文件，具体就是请求的地址、错误信息等，小伙伴也可以都使用一下然后查看两个文件的异同。
    },
    'loggers': {  # log记录器，配置之后就会对应的输出日志
        # django 表示就是django本身默认的控制台输出，就是原本在控制台里面输出的内容，在这里的handlers里的file表示写入到上面配置的file-/home/aea/log/jwt_test.log文件里面
        # 在这里的handlers里的console表示写入到上面配置的console-/home/aea/log/test.log文件里面
        'django': {
            'handlers': ['console', 'file_rotate'],
            # 这里直接输出到控制台只是请求的路由等系统console，当使用重定向之后会把所有内容输出到log日志
            'level': 'INFO',
            'propagate': True,
        },
        'django.request ': {
            'handlers': ['console', 'file_rotate'],
            'level': 'INFO',  # 配合上面的将警告log写入到另外一个文件
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console', 'file_rotate'],  # 指定file handler处理器，表示只写入到文件
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
