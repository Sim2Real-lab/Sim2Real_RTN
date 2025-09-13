from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

class Team(models.Model):
    name=models.CharField(max_length=100)
    join_code=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    leader=models.OneToOneField(User,related_name="led_team",on_delete=models.CASCADE)
    members=models.ManyToManyField(User,related_name="team")
    is_paid = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    payment_screenshot = models.ImageField(upload_to="payments/", blank=True, null=True)
    payment_ref = models.CharField(max_length=50, blank=True, null=True)

    def is_registered(self):
        return self.is_paid and self.is_verified
    def is_outsider(self):
        return any(member.profile.college != "National Institute of Technology Karnataka" for member in self.members.all())

    def is_full(self):
        return self.members.count()>=3
    
    def __str__(self):
        return self.name
    
class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')

    class Meta():
        unique_together=('user','team')