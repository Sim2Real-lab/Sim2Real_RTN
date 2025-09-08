from django.contrib.auth import views
from django.urls import path, include
from .views import home_view,schedule_view,registration_view,prize_view,brochure_view,resources_view,announce_view,faq_view,problem_statement_view
urlpatterns = [
    path('',home_view,name='home'),
    path('logout/',views.LogoutView.as_view(next_page='login'),name='logout'),
    path('user_profile/',include('user_profile.urls'),name="profile"),
    path('events_schedule/',schedule_view,name='schedule'),
    path('register/',registration_view,name='register'),
    path('prize/',prize_view,name='prizes'),
    path('brochure/',brochure_view,name='brochure'),
    path('resources/',resources_view,name='resources'),
    path('announcements/',announce_view,name='announcements'),
    path('faqs/',faq_view,name='faq_1'),
    path('team/', include('team_profile.urls'),name='manage_requests'),
    path('problem_statement/',problem_statement_view,name='problem_statement'),
]