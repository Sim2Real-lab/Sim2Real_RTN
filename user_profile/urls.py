from django.contrib.auth import views
from django.urls import path, include
from .views import userprofile_view
urlpatterns = [
    path('user/',userprofile_view,name="profile"),
    path('team/', include('team_profile.urls'),name='manage_requests'),
]