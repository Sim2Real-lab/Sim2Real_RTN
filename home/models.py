from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Team(models.Model):
    # ...
    leader = models.ForeignKey(User, related_name='led_home_team', on_delete=models.CASCADE)
    # ...
