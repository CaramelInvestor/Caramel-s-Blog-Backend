# This handles the urls for the posts app
# --------------------------------

from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('list/', views.post_list, name='post_list'),
    path('detail/<slug>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('update/<slug>/', views.post_update, name='post_update'),
    path('delete/<slug>/', views.post_delete, name='post_delete'),
]
