from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages
from user_profile.models import UserProfile

def user_view(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role = getattr(request.user, 'userrole', None)
        if not user_role:
            return HttpResponseForbidden("Access Denied")
        if user_role.is_organiser:
            return redirect("staff_dashboard")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def organiser_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user_role = getattr(request.user, 'userrole', None)
        if not user_role:
            return HttpResponseForbidden("Access Denied")
        if not user_role.is_organiser:
            return redirect("home") 
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def profile_updated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not profile or not profile.is_complete():
            messages.warning(request,"Update your profile to Continue.")
            return redirect('profile')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def profile_updated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.warning(request, "Please update your profile to continue.")
            return redirect('profile')  # Or 'profile_update' depending on your URL name
        
        if not profile.is_complete():
            messages.warning(request, "Please update your profile to continue.")
            return redirect('profile')

        return view_func(request, *args, **kwargs)
    return _wrapped_view