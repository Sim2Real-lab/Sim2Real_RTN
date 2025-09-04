# simreal/middleware/maintenance_middleware.py

from django.http import HttpResponse
from django.conf import settings

class MaintenanceModeMiddleware:
    """
    Middleware to block all users when MAINTENANCE_MODE = True in settings.
    Staff users (is_staff) can bypass it.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if maintenance mode is ON
        if getattr(settings, 'MAINTENANCE_MODE', False):
            # Allow staff users to bypass
            if not request.user.is_authenticated or not request.user.is_staff:
                return HttpResponse(
                    "<h1>Site Under Maintenance</h1><p>We'll be back soon.</p>",
                    content_type="text/html",
                    status=503
                )

        response = self.get_response(request)
        return response
