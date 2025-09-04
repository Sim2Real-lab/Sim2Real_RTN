from django.shortcuts import render
from django.conf import settings

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip maintenance for superusers/admins
        if getattr(settings, "MAINTENANCE_MODE", False) and not request.user.is_organiser:
            return render(request, "maintenance.html")
        return self.get_response(request)
