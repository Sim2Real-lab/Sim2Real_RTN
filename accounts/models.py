from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserRole(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='userrole')
    is_organiser=models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}"