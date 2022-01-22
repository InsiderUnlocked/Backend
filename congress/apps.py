# @Author: Farhan Rehman
# Purpose: Registering app (congress folder) with django

# Import Libraries
from django.apps import AppConfig
from django.conf import settings

# Standard App config (django)
class CongressConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'congress'

    
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from api import operator
            operator.start()

