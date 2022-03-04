from rest_framework.serializers import (
    ModelSerializer, 
    IntegerField, 
    SlugRelatedField,
)
from django.contrib.auth.models import User
from blog.models import Category, Blog, Comment

class CreatorSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username',]

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name',]

class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body']

class BlogSerializer(ModelSerializer):
    creator = CreatorSerializer(many = False, read_only = True)
    comments = CommentSerializer(many = True, read_only = True)
    
    class Meta:
        model = Blog
        fields = [
            'id',
            'creator',
            'name', 
            'category', 
            'description', 
            'body', 
            'logo',
            'comments'
        ]