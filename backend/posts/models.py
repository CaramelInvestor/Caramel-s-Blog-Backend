from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from uuid import uuid4

# Create your models here.


class Post(models.Model):
    '''This model represents a post'''
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    author = models.ForeignKey(User, on_delete=CASCADE)
    content = models.TextField(null=False, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def num_likes(self):
        '''This method returns the number of post likes'''
        return self.likes.count()

    def __str__(self):
        """This method returns a string representation
        of the title object"""
        return self.title


class Comment(models.Model):
    '''This model represents a comment'''
    _id = models.AutoField(primary_key=True, editable=False)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    author = models.ForeignKey(User, on_delete=CASCADE)
    likes = models.ManyToManyField(
        User, related_name='comment_likes', blank=True)
    content = models.TextField(null=False, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def num_likes(self):
        '''This method returns the number of comment likes'''
        return self.likes.count()

    def __str__(self):
        """This method returns a string representation
        of the comment object"""
        return self.content


class Reply(models.Model):
    '''This model represents a reply'''
    _id = models.AutoField(primary_key=True, editable=False)
    comment = models.ForeignKey(Comment, on_delete=CASCADE)
    author = models.ForeignKey(User, on_delete=CASCADE)
    likes = models.ManyToManyField(
        User, related_name='reply_likes', blank=True)
    content = models.TextField(null=False, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def num_likes(self):
        '''This method returns the number of reply likes'''
        return self.likes.count()

    def __str__(self):
        """This method returns a string representation
        of the content object"""
        return self.content
