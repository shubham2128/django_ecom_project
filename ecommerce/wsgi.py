import os
from django.core.wsgi import get_wsgi_application

settings_module = 'azure_project.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'ecommerce.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
application = get_wsgi_application()
