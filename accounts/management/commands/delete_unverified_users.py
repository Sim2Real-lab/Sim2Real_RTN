from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete users who have not verified their email within 1 minute'

    def handle(self, *args, **kwargs):
        expiry_duration = timedelta(minutes=1)
        now = timezone.now()

        unverified_users = User.objects.filter(is_active=False, date_joined__lt=now - expiry_duration)

        count = unverified_users.count()
        unverified_users.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} unverified users.'))
