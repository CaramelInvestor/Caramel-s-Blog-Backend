'''This file contains the views for the posts app'''

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['POST'])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return Response(status=204)
