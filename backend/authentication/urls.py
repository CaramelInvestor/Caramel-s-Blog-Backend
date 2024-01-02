# This handles the urls for the auth app
# ---------------------------------------------

from django.urls import path
from .views import *

urlpatterns = [
    path('auth/routes/', routes),
    path('auth/login/', login_view),
    path('auth/logout/', logout_view),
    path('auth/register/', register_view),
    path('auth/user/', user_view),
    path('auth/users/', users_view),
    path('auth/user/<str:pk>/', user_detail_view),
    path('auth/user/<str:pk>/update/', user_update_view),
    path('auth/user/<str:pk>/delete/', user_delete_view),
]
