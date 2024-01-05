'''This file contains the views for the posts app'''

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import PostSerializer, CommentSerializer, ReplySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound


@api_view(['GET'])
def routes(request):
    '''This function returns the available routes'''
    routes = [
        {
            'Endpoint': '/posts/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of posts'
        },
        {
            'Endpoint': '/posts/<str:pk>/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single post object'
        },
        {
            'Endpoint': '/posts/create/',
            'method': 'POST',
            'body': {
                'body': "string",
                'title': "string",
                'image': "string",
                'author': "string",
            },
            'description': 'Creates a new post with data sent in the post request'
        },
        {
            'Endpoint': '/posts/update/<str:pk>/',
            'method': 'PUT',
            'body': {
                'body': "string",
                'title': "string",
                'image': "string",
                'author': "string",
            },
            'description': 'Updates a post with data sent in the post request'
        },
        {
            'Endpoint': '/posts/delete/<str:pk>/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes a post'
        },
        {
            'Endpoint': '/posts/<str:pk>/like/',
            'method': 'GET',
            'body': None,
            'description': 'Increments the like count of a post by 1'
        },
        {
            'Endpoint': '/posts/<str:pk>/unlike/',
            'method': 'GET',
            'body': None,
            'description': 'Decrements the like count of a post by 1'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of comments for a post'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/create/',
            'method': 'POST',
            'body': {
                'body': "string",
                'author': "string",
            },
            'description': 'Creates a new comment for a post with data sent in the post request'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/update/<str:comment_pk>/',
            'method': 'PUT',
            'body': {
                'body': "string",
                'author': "string",
            },
            'description': 'Updates a comment for a post with data sent in the post request'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/delete/<str:comment_pk>/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes a comment for a post'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/<str:comment_pk>/like/',
            'method': 'GET',
            'body': None,
            'description': 'Increments the like count of a comment by 1'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/<str:comment_pk>/unlike/',
            'method': 'GET',
            'body': None,
            'description': 'Decrements the like count of a comment by 1'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/<str:comment_pk>/replies/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of replies for a comment'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/<str:comment_pk>/replies/create/',
            'method': 'POST',
            'body': {
                'body': "string",
                'author': "string",
            },
            'description': 'Creates a new reply for a comment with data sent in the post request'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/<str:comment_pk>/replies/update/<int:reply_pk>/',
            'method': 'PUT',
            'body': {
                'body': "string",
                'author': "string",
            },
            'description': 'Updates a reply for a comment with data sent in the post request'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/<str:comment_pk>/replies/delete/<str:reply_pk>/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes a reply for a comment'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/<str:comment_pk>/replies/<str:reply_pk>/like/',
            'method': 'GET',
            'body': None,
            'description': 'Increments the like count of a reply by 1'
        },
        {
            'Endpoint': '/posts/<str:pk>/comments/<str:comment_pk>/replies/<str:reply_pk>/unlike/',
            'method': 'GET',
            'body': None,
            'description': 'Decrements the like count of a reply by 1'
        },
    ]
    return Response(routes)


@api_view(['GET'])
def post_list(request):
    try:
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def post_detail(request, pk):
    try:
        post = get_object_or_404(Post, _id=pk)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request):
    try:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def post_update(request, pk):
    try:
        post = get_object_or_404(Post, _id=pk)
        serializer = PostSerializer(instance=post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except NotFound:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):

    try:
        post = get_object_or_404(Post, _id=pk)
        post.delete()
        return Response({'message': 'Post deleted'}, status=status.HTTP_204_NO_CONTENT)
    except NotFound:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_like(request, pk):
    try:
        post = get_object_or_404(Post, _id=pk)
        post.likes.add(request.user)
        return Response({'message': 'Post liked'}, status=status.HTTP_200_OK)
    except NotFound:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)\



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_unlike(request, pk):
    try:
        post = get_object_or_404(Post, _id=pk)
        post.likes.remove(request.user)
        return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
    except NotFound:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)\



@api_view(['GET'])
def post_comments(request, pk):
    try:
        post = get_object_or_404(Post, _id=pk)
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    except NotFound:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def comment_detail(request, pk, comment_pk):
    try:
        comment = get_object_or_404(Comment, _id=comment_pk, post=pk)
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)
    except NotFound:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, pk):
    try:
        post = get_object_or_404(Post, _id=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except NotFound:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_update(request, pk, comment_pk):
    try:
        comment = get_object_or_404(Comment, _id=comment_pk, post=pk)
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except NotFound:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, pk, comment_pk):
    try:
        comment = get_object_or_404(Comment, _id=comment_pk, post=pk)
        comment.delete()
        return Response({'message': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)
    except NotFound:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_like(request, pk, comment_pk):
    try:
        comment = get_object_or_404(Comment, _id=comment_pk, post=pk)
        comment.likes.add(request.user)
        return Response({'message': 'Comment liked'}, status=status.HTTP_200_OK)
    except NotFound:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_unlike(request, pk, comment_pk):
    try:
        comment = get_object_or_404(Comment, _id=comment_pk, post=pk)
        comment.likes.remove(request.user)
        return Response({'message': 'Comment unliked'}, status=status.HTTP_200_OK)
    except NotFound:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def comment_replies(request, pk, comment_pk):
    try:
        comment = get_object_or_404(Comment, _id=comment_pk, post=pk)
        replies = comment.reply_set.all()
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)
    except NotFound:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def reply_detail(request, pk, comment_pk, reply_pk):
    try:
        reply = get_object_or_404(
            Reply, _id=reply_pk, comment__post=pk, comment=comment_pk)
        serializer = ReplySerializer(reply, many=False)
        return Response(serializer.data)
    except NotFound:
        return Response({'error': 'Reply not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reply_create(request, pk, comment_pk):
    try:
        comment = get_object_or_404(Comment, _id=comment_pk, post=pk)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, comment=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except NotFound:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reply_update(request, pk, comment_pk, reply_pk):
    try:
        reply = get_object_or_404(
            Reply, _id=reply_pk, comment__post=pk, comment=comment_pk)
        serializer = ReplySerializer(instance=reply, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except NotFound:
        return Response({'error': 'Reply not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reply_delete(request, pk, comment_pk, reply_pk):
    try:
        reply = get_object_or_404(
            Reply, _id=reply_pk, comment__post=pk, comment=comment_pk)
        reply.delete()
        return Response({'message': 'Reply deleted'}, status=status.HTTP_204_NO_CONTENT)
    except NotFound:
        return Response({'error': 'Reply not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reply_like(request, pk, comment_pk, reply_pk):
    try:
        reply = get_object_or_404(
            Reply, _id=reply_pk, comment__post=pk, comment=comment_pk)
        reply.likes.add(request.user)
        return Response({'message': 'Reply liked'}, status=status.HTTP_200_OK)
    except NotFound:
        return Response({'error': 'Reply not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reply_unlike(request, pk, comment_pk, reply_pk):
    try:
        reply = get_object_or_404(
            Reply, _id=reply_pk, comment__post=pk, comment=comment_pk)
        reply.likes.remove(request.user)
        return Response({'message': 'Reply unliked'}, status=status.HTTP_200_OK)
    except NotFound:
        return Response({'error': 'Reply not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
