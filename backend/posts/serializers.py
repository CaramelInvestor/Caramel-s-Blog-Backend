'''This module contains the serializers for the posts app'''

from rest_framework.serializers import ModelSerializer
from .models import Post, Comment


class PostSerializer(ModelSerializer):
    '''Serializer for the Post model'''
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    '''Serializer for the Comment model'''
    class Meta:
        model = Comment
        fields = '__all__'


class ReplySerializer(ModelSerializer):
    '''Serializer for the Reply model'''
    class Meta:
        model = Comment
        fields = '__all__'