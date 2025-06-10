from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect

def organiser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role=getattr(request.user,'userrole',None)
        if not user_role or not user_role.is_organiser:
            return HttpResponseForbidden("Access Denied: Organiser only.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def participant_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role = getattr(request.user, 'userrole', None)
        if not user_role:
            return HttpResponseForbidden("Access Denied: Participants only.")
        if user_role.is_organiser:
            return redirect('staff_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view