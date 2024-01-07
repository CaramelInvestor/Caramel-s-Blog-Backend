# This handles the urls for the auth app
# ---------------------------------------------


from django.urls import path
from .views import *

urlpatterns = [
    path('users/routes/', routes, name='routes'),
    path('users/', users_view,  name='users'),
    path('user/', user_view, name='user'),
    path('user/<str:pk>/', user_detail_view, name='user_detail'),
    path('user/<str:pk>/update/', user_update_view, name='user_update'),
    path('user/<str:pk>/delete/', user_delete_view, name='user_delete'),
    path('user/login/', login_view, name='login'),
    path('user/logout/', logout_view, name='logout'),
    path('user/register/', register_view, name='register'),
]
