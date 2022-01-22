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

# OTP implementation
# class OTPAdmin(OTPAdminSite):
#     pass

# admin_site = OTPAdmin(name='OTPAdmin')
# admin_site.register(User)
# admin_site.register(TOTPDevice)

# from django_otp.admin import OTPAdminSite
# admin.site.__class__ = OTPAdminSite

# URL paths
urlpatterns = [
    # Security feature - Honeypot Admin: fake login page which records the ip and attempeted username and password 
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # Real admin page 
    path('aprivatesocialmeet/', admin.site.urls),
    # Imports the urls from the app congress/urls.py
    path('', include('congress.urls')),
]