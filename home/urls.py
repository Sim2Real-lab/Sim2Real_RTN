from django.contrib.auth import views
from django.urls import path, include
from .views import home_view,schedule_view,registration_view,download_brochure,resources_view,announce_view,faq_view,problem_statement_view,user_submission_windows,submit_to_window
urlpatterns = [
    path('',home_view,name='home'),
    path('logout/',views.LogoutView.as_view(next_page='login'),name='logout'),
    path('user_profile/',include('user_profile.urls'),name="profile"),
    path('events_schedule/',schedule_view,name='schedule'),
    path('register/',registration_view,name='register'),
    path('resources/',resources_view,name='resources'),
    path('announcements/',announce_view,name='announcements'),
    path('faqs/',faq_view,name='faq_1'),    
    path('team/', include('team_profile.urls'),name='manage_requests'),
    path('problem_statement/',problem_statement_view,name='problem_statement'),
    path("brochure/download/", download_brochure, name="download_brochure"),
    path("submissions/", user_submission_windows, name="user_submission_windows"),
    path("submissions/<int:window_id>/submit/", submit_to_window, name="submit_to_window"),
]