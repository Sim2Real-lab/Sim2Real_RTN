from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserRole(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='userrole')
    is_organiser=models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}"


import random
from django.utils import timezone
from datetime import timedelta

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f'OTP for {self.user.email} - {self.otp}'
