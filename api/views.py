import coreapi
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.generics import ListAPIView

from blog.models import Blog
from .serializers import BlogSerializer
from .pagination import MyCustomPagination

class BlogViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put', 'get']:
            extra_fields  = [
                coreapi.Field('name'),
                coreapi.Field('category'),
                coreapi.Field('creator'),
                coreapi.Field('description'),
                coreapi.Field('body'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class BlogList(ListAPIView):

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = MyCustomPagination

    # def get(self, request):
    #     queryset = Blog.objects.all()
    #     serializer = BlogSerializer(queryset, many = True)
    #     return Response(serializer.data)

class BlogCreate(APIView):

    schema = BlogViewSchema()

    def post(self, request):
        serializer = BlogSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BlogDetail(APIView):

    def get(self, request, pk):
        blog = Blog.objects.get(pk = pk)
        serializer = BlogSerializer(blog, many = False)
        return Response(serializer.data)

class BlogUpdate(APIView):

    schema = BlogViewSchema()
    
    def put(self, request, pk):
        blog = Blog.objects.get(pk = pk)
        serializer = BlogSerializer(blog, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BlogDelete(APIView):

    def delete(self, request, pk):
        blog = Blog.objects.get(pk = pk)
        blog.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

