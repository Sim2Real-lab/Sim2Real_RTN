from django.urls import path
from .views import staff_dashboard,checkregistration,upload_questions,queries,create_announcement,resolve_query,announcement_list,announcement_edit,verify_payments

urlpatterns = [
    path('', staff_dashboard, name='staff_dashboard'),
    path('check/registration/', checkregistration, name='check_registration'),
    path('upload/question/', upload_questions, name='upload_questions'),
    path('check/queries/', queries, name='respond_queries'),
    path('respond/queries/<uuid:ticket>/', resolve_query, name='resolve_query'),
    path('make/registration/',create_announcement, name='make_announcments'),
    path('modify/',announcement_list, name='announcement_list'),
    path('modify/edit/<int:pk>/',announcement_edit, name='announcement_edit'),
    path("verify-payments/<int:team_id>/", verify_payments, name="verify_payments")
]
