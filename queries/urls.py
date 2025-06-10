from .views import user_query_view,query_response,fetch_response
from django.urls import path, include

urlpatterns = [
    path('',user_query_view,name='user_query'),
    path('response/',query_response,name='query_response'),
    path('query/response/<uuid:ticket>/', fetch_response, name='fetch_response'),
]
