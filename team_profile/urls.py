from django.contrib.auth import views
from .views import team_profile_views,join_team,manage_requests,create_team,create_team_with_code,join_team_with_code,register_for_event,payment_view
from django.urls import path
from .views import TeamCreationForm


urlpatterns = [
    path('',team_profile_views,name="teamprofile"),
    path('create-team/',create_team,name="create_team"),
    path('create-team/code/', create_team_with_code, name="create_team_with_code"),
    path('join/',join_team, name='join_team'),
    path('join-team/code/', join_team_with_code, name="join_team_with_code"),
    path('manage/',manage_requests, name='manage_requests'),
    path('register/',register_for_event,name='register_pay'),
    path('payment/',payment_view, name='payment_page'),

]