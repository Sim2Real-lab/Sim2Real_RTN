from django.urls import path
from .views import list_tests,create_test,edit_test,delete_test,manage_questions,add_question,edit_question,delete_question,view_submissions,view_analysis,staff_dashboard,checkregistration,manage_submissions,toggle_window_visibility,create_window,window_detail,all_users_view,grade_submission,upload_questions,upload_brochure,queries,manage_resources,create_announcement,resolve_query,announcement_list,announcement_edit,verify_payments,view_payment_screenshot,add_section,manage_problem_statement,delete_section,edit_section

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
    path("manage/",manage_submissions, name="manage_submissions"),
    path("create/", create_window, name="create_window"),
    path("window/<int:window_id>/", window_detail, name="window_detail"),
    path("grade/<int:submission_id>/", grade_submission, name="grade_submission"),
    path("windows/<int:window_id>/toggle_visibility/", toggle_window_visibility, name="toggle_window_visibility"),
    path('staff/tests/', list_tests, name='list_tests'),                 # List all tests
    path('staff/tests/create/', create_test, name='create_test'),       # Create new test
    path('staff/tests/<int:test_id>/edit/', edit_test, name='edit_test'),  # Edit test details
    path('staff/tests/<int:test_id>/delete/', delete_test, name='delete_test'),  # Delete test
    path('staff/tests/<int:test_id>/questions/', manage_questions, name='manage_questions'),  # List questions in a test
    path('staff/tests/<int:test_id>/questions/add/', add_question, name='add_question'),       # Add question
    path('staff/tests/<int:test_id>/questions/<int:question_id>/edit/', edit_question, name='edit_question'),  # Edit question
    path('staff/tests/<int:test_id>/questions/<int:question_id>/delete/', delete_question, name='delete_question'),  # Delete question
    path('staff/tests/<int:test_id>/submissions/', view_submissions, name='test_submissions'),  # View all submissions for a test
    path('staff/tests/submissions/<int:submission_id>/grade/', grade_submission, name='grade_submission'),  # Grade a submission
]
