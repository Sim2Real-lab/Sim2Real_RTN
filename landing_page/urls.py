# landing_page/urls.py

from django.urls import path
from . import views

app_name = 'landing_page' # This defines the namespace for your app

urlpatterns = [
    # Main Landing Page
    path('', views.main_landing_page_view, name='main_landing_page'),
    path('queries/submit/', views.general_query_submit_view, name='general_query_submit'),

    # Dedicated Sponsor Page
    path('sponsor/', views.landing_page_sponsor_view, name='sponsor_page'),
    path('sponsor/contact-submit/', views.sponsor_contact_submit_view, name='sponsor_contact_submit'),
    path("brochure/download/", views.download_brochure, name="download_brochure_home"),
]

