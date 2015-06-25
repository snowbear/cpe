import os
import sys

sys.path.append(os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_site.settings_prod'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()