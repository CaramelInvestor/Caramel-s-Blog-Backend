'''This file contains the views for the auth app'''''

from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET'])
def routes(request):
    '''This view handles the routes'''
    routes = [
        {
            'Endpoint': '/user/register',
            'method': 'POST',
            'body': {
                'username': '',
                'email': '',
                'password': '',
                'password2': ''
            }
        },
        {
            'Endpoint': '/user/login',
            'method': 'POST',
            'body': {
                'username': '',
                'password': ''
            }
        },
        {
            'Endpoint': '/user/logout',
            'method': 'POST',
            'body': None
        },
        {
            'Endpoint': '/user',
            'method': 'GET',
            'body': None
        },
        {
            'Endpoint': '/users',
            'method': 'GET',
            'body': None
        },
        {
            'Endpoint': '/user/<str:pk>',
            'method': 'GET',
            'body': None
        },
        {
            'Endpoint': '/user/<str:pk>/update',
            'method': 'PUT',
            'body': {
                'username': '',
                'email': ''
            }
        },
        {
            'Endpoint': '/user/<str:pk>/delete',
            'method': 'DELETE',
            'body': None
        },
    ]
    return Response(routes)


@api_view(['POST'])
def register_view(request):
    '''This view handles the registration of a user'''
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        if password == password2:
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if User.objects.filter(email=email).exists():
                    return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.save()
                    return Response({'status': 'User created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login_view(request):
    '''This view handles the login of a user'''
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'status': 'Logged in'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid login details'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """This view handles the log out of a user"""
    logout(request)
    return Response({'status': 'Logged out'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    '''This view handles the viewing of a user'''
    try:
        user = request.user
        return Response({'id': user.id, 'username': user.username, 'email': user.email}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_view(request):
    '''This view handles the viewing of all users'''
    try:
        users = User.objects.all()
        data = []
        for user in users:
            data.append(
                {'id': user.id, 'username': user.username, 'email': user.email})
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail_view(request, pk):
    '''This view handles the viewing of a user'''
    try:
        user = User.objects.get(id=pk)
        return Response({'id': user.id, 'username': user.username, 'email': user.email}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update_view(request, pk):
    '''This view handles the updating of a user'''
    try:
        user = User.objects.get(id=pk)
        user.username = request.data.get('username')
        user.email = request.data.get('email')
        user.save()
        return Response({'status': 'User updated'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete_view(request, pk):
    '''This view handles the deleting of a user'''
    try:
        user = User.objects.get(id=pk)
        user.delete()
        return Response({'status': 'User deleted'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
