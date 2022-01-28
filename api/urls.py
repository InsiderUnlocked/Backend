# @Author Farhan Rehman
# Imports
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings

# OTP Libraries  
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.models import User
from django_otp.admin import OTPAdminSite
from django.conf.urls.static import static

# Auto Documentation Imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# OTP implementation
# You need to create an admin user, login on the /aprivatesocialmeet page, and register your device under the TOTP Devices page
# class OTPAdmin(OTPAdminSite):
#    pass

# admin_site = OTPAdmin(name='OTPAdmin')
# admin_site.register(User)
# admin_site.register(TOTPDevice)

# admin.site.__class__ = OTPAdminSite

# Creating Documentation for the API
schema_view = get_schema_view(
   openapi.Info(
      title="Insider Unlocked",
      default_version='v1',
      description="Insider Unlocked API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="rehmafar@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# URL paths
urlpatterns = [
    # Security feature - Honeypot Admin: fake login page which records the ip and attempeted username and password 
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # Real admin page 
    path('aprivatesocialmeet/', admin.site.urls),
    # Imports the urls from the app congress/urls.py
    path('', include('congress.urls')),

    # Auto Documentation url
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
