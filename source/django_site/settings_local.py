from .settings_common import *

SECRET_KEY = 'ca%x0zuw_$!&pm-$(9(15zce7z(7b2*ikre3+l9ru_b)0$fcy%'

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'cpe',
    'USER': 'cpe',
    'PASSWORD': 'cpe',
    'HOST': 'localhost',
    'PORT': '',
}

DEBUG = TEMPLATE_DEBUG = True
