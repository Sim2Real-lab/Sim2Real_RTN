from django.urls import path
from .views import staff_dashboard,checkregistration,upload_questions,queries,create_announcement,resolve_query

urlpatterns = [
    path('', staff_dashboard, name='staff_dashboard'),
    path('check/registration/', checkregistration, name='check_registration'),
    path('upload/question/', upload_questions, name='upload_questions'),
    path('check/queries/', queries, name='respond_queries'),
    path('respond/queries/<uuid:ticket>/', resolve_query, name='resolve_query'),
    path('make/registration/',create_announcement, name='make_announcments'),
]
