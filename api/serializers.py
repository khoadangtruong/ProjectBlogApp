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
    id = IntegerField(required = False)
    user = CreatorSerializer(many = False, read_only = False)

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 
            'blog', 'body'
        ]
        read_only_fields = ['user', 'blog',]

class BlogSerializer(ModelSerializer):
    creator = CreatorSerializer(many = False, read_only = False)
    comments = CommentSerializer(many = True)
    category = CategorySerializer(many = False)

    class Meta:
        model = Blog
        fields = [
            'creator',
            'name', 
            'category', 
            'description', 
            'body', 
            'logo',
            'comments'
        ]

class BlogCreateSerializer(ModelSerializer):
    comments = SlugRelatedField(
        many = True,
        slug_field = 'body', 
        read_only = True
    )
    
    class Meta:
        model = Blog
        fields = [
            'name', 
            'category', 
            'description', 
            'body', 
            'logo',
            'comments'
        ]
        # depth = 1
        # read_only_fields = ['description',] # cannot assign value when create or update
        # extra_kwargs = {
        #     'description': {'write_only': True} # will not display in detail or list, uncomment this to see how it work
        # }
    
    # def create(self, validated_data):

    #     comments = validated_data.pop('comments')
    #     blog = Blog.objects.create(**validated_data)
    #     blog.save()

    #     for comment in comments:
    #         Comment.objects.create(**comment, blog = blog)
    #     return blog

    # def update(self, instance, validated_data):

    #     instance.name = validated_data.get('name', instance.name)
    #     instance.category = validated_data.get('category', instance.category)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.body = validated_data.get('body', instance.body)
    #     instance.save()
    #     return instance

class BlogUpdateSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'name', 
            'category', 
            'description', 
            'body',
            'logo'
        ]

class BlogDetailSerializer(ModelSerializer):

    comments = CommentSerializer(many = True)
    category = CategorySerializer(many = False)
    creator = CreatorSerializer(many = False)
    
    class Meta:
        model = Blog
        fields = [
            'id',
            'name', 
            'category', 
            'creator',
            'description', 
            'body', 
            'logo',
            'comments'
        ]
        # depth = 1