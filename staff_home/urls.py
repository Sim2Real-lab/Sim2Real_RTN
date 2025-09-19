from django.urls import path
from .views import staff_dashboard,checkregistration,all_users_view,upload_questions,upload_brochure,queries,manage_resources,create_announcement,resolve_query,announcement_list,announcement_edit,verify_payments,view_payment_screenshot,add_section,manage_problem_statement,delete_section,edit_section

urlpatterns = [
    path('', staff_dashboard, name='staff_dashboard'),
    path('check/registration/', checkregistration, name='check_registration'),
    path('upload/question/', upload_questions, name='upload_questions'),
    path('check/queries/', queries, name='respond_queries'),
    path('respond/queries/<uuid:ticket>/', resolve_query, name='resolve_query'),
    path('make/registration/',create_announcement, name='make_announcments'),
    path('modify/',announcement_list, name='announcement_list'),
    path('modify/edit/<int:pk>/',announcement_edit, name='announcement_edit'),
    path("verify-payments/", verify_payments, name="verify_payments"),  # list view
    path("verify-payments/<int:team_id>/", verify_payments, name="verify_payments"),  # verify single team
    path("payment-screenshot/<int:team_id>/", view_payment_screenshot, name="view_payment_screenshot"),
    path("problem-statement/",manage_problem_statement, name="manage_problem_statement"),
    path("problem-statement/add/", add_section, name="add_section"),
    path("problem-statement/<int:pk>/edit/", edit_section, name="edit_section"),
    path("problem-statement/<int:pk>/delete/", delete_section, name="delete_section"),
    path("resources/", manage_resources, name="manage_resources"),
    path("brochure/",upload_brochure,name='upload_brochure'),
    path("users/",all_users_view,name="user_data"),
]
