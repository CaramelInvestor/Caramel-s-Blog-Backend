# This handles the urls for the auth app
# ---------------------------------------------

from django.urls import path
from .views import *

urlpatterns = [
    path('auth/routes/', routes, name='routes'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/register/', register_view, name='register'),
    path('auth/user/', user_view, name='user'),
    path('auth/users/', users_view,  name='users'),
    path('auth/user/<str:pk>/', user_detail_view, name='user_detail'),
    path('auth/user/<str:pk>/update/', user_update_view, name='user_update'),
    path('auth/user/<str:pk>/delete/', user_delete_view, name='user_delete'),
]
