from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings

# OTP implementation  
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.models import User
from django_otp.admin import OTPAdminSite
from django.conf.urls.static import static

# class OTPAdmin(OTPAdminSite):
#     pass

# admin_site = OTPAdmin(name='OTPAdmin')
# admin_site.register(User)
# admin_site.register(TOTPDevice)

# from django_otp.admin import OTPAdminSite
# admin.site.__class__ = OTPAdminSite

# URL paths
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('congress.urls')),
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('aprivatesocialmeet/', admin.site.urls),
]