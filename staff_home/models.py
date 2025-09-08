from django.db import models
from django.contrib.auth.models import User
import datetime
from team_profile.models import Team
from django.utils import timezone
# Create your models here.

class Announcments(models.Model):
    message=models.TextField()
    created_at=models.DateField(auto_now=True)
    valid_till=models.DateField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    schedule_for_later=models.DateField(help_text="Schedule time")
     # Manual override flags
    manual_visibility = models.BooleanField(null=True, blank=True, help_text="Set visibility manually")
    manual_validity = models.BooleanField(null=True, blank=True, help_text="Set validity manually")
    CATEGORY_CHOICES = [
        ('GENERAL', 'General'),
        ('REGISTERED', 'Registered'),
        ('NOT_REGISTERED', 'Not Registered'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def is_visible(self):
        today = datetime.date.today()
        if self.manual_visibility is not None:
            return self.manual_visibility
        return self.schedule_for_later <= today

    def is_valid(self):
        today = datetime.date.today()
        if self.manual_validity is not None:
            return self.manual_validity
        return today <= self.valid_till

    def save(self, *args, **kwargs):
        # Auto-manage the validity and visibility if not overridden
        if self.manual_validity is None:
            self.validity = self.is_valid()
        else:
            self.validity = self.manual_validity

        if self.manual_visibility is None:
            self.visibility = self.is_visible()
        else:
            self.visibility = self.manual_visibility

        super().save(*args, **kwargs)

    # These are just to store the final evaluated values
    visibility = models.BooleanField(default=False)
    validity = models.BooleanField(default=False)

    # staff_home/models.py


class ProblemStatementConfig(models.Model):
    enabled = models.BooleanField(default=False)  # Control visibility
    file = models.FileField(upload_to="problem_statements/", null=True, blank=True)

    def __str__(self):
        return "Problem Statement Config"
