from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Query(models.Model):
    USER = 'user'
    SPONSOR = 'sponsor'
    QUERY_TYPE_CHOICES = [
        (USER, 'User'),
        (SPONSOR, 'Sponsor'),
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional for sponsors
    name = models.CharField(max_length=100)  # For sponsor queries without login
    email = models.EmailField()
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    contact = models.CharField(max_length=15, blank=True, null=True)  # optional for users
    organisation = models.CharField(max_length=100, blank=True, null=True)  # only for sponsors
    query_type = models.CharField(max_length=10, choices=QUERY_TYPE_CHOICES)
    resolved = models.BooleanField(default=False)
    ticket=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responded_queries')

   
    def __str__(self):
        return f"{self.query_type.upper()} - {self.name} ({self.email})"
