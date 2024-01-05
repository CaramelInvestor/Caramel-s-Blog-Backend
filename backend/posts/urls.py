# This handles the urls for the posts app
# --------------------------------

from django.urls import path
from .views import *

urlpatterns = [
    path('posts/routes/', routes, name='routes'),
    path('posts/', post_list, name='post_list'),
    path('posts/<str:pk>/', post_detail, name='post_detail'),
    path('posts/create/', post_create, name='post_create'),
    path('posts/update/<str:pk>/', post_update, name='post_update'),
    path('posts/delete/<str:pk>/', post_delete, name='post_delete'),
    path('posts/<str:pk>/like/', post_like, name='post_like'),
    path('posts/<str:pk>/unlike/', post_unlike, name='post_unlike'),
    path('posts/<str:pk>/comments/', post_comments, name='post_comments'),
    path('posts/<str:pk>/comments/<str:comment_pk>/',
         comment_detail, name='comment_detail'),
    path('posts/<str:pk>/comments/create/',
         comment_create, name='comment_create'),
    path('posts/<str:pk>/comments/update/<str:comment_pk>/',
         comment_update, name='comment_update'),
    path('posts/<str:pk>/comments/delete/<str:comment_pk>/',
         comment_delete, name='comment_delete'),
    path('posts/<str:pk>/comments/<str:comment_pk>/like/',
         comment_like, name='comment_like'),
    path('posts/<str:pk>/comments/<str:comment_pk>/unlike/',
         comment_unlike, name='comment_unlike'),
    path('posts/<str:pk>/comments/<str:comment_pk>/replies/',
         comment_replies, name='comment_replies'),
    path('posts/<str:pk>/comments/<str:comment_pk>/replies/<str:reply_pk>/',
         reply_detail, name='reply_detail'),
    path('posts/<str:pk>/comments/<str:comment_pk>/replies/create/',
         reply_create, name='reply_create'),
    path('posts/<str:pk>/comments/<str:comment_pk>/replies/update/<str:reply_pk>/',
         reply_update, name='reply_update'),
    path('posts/<str:pk>/comments/<str:comment_pk>/replies/delete/<str:reply_pk>/',
         reply_delete, name='reply_delete'),
    path('posts/<str:pk>/comments/<str:comment_pk>/replies/<str:reply_pk>/like/',
         reply_like, name='reply_like'),
    path('posts/<str:pk>/comments/<str:comment_pk>/replies/<str:reply_pk>/unlike/',
         reply_unlike, name='reply_unlike'),

]
