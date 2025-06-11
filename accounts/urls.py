from django.contrib.auth import admin,views
from django.urls import path, include
from .views import login_view, signup_view, activate,resend_verification_view,request_otp_view,verify_otp_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('resend-verification/', resend_verification_view, name='resend_verification'),
    path('request-otp/',request_otp_view, name='request_otp'),
    path('verify-otp/',verify_otp_view, name='verify_otp'),
]

