from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated


from blog.models import Blog
from .serializers import (
    BlogCreateSerializer, 
    BlogDetailSerializer,
    BlogUpdateSerializer
)
from .pagination import MyCustomPagination

class BlogList(ListAPIView):
    
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    pagination_class = MyCustomPagination

class BlogCreate(CreateAPIView):
    
    serializer_class = BlogCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save(creator = self.request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class BlogDetail(RetrieveAPIView):

    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer

    # def get(self, request, pk):
    #     blog = get_object_or_404(Blog, pk = pk)
    #     serializer = BlogDetailSerializer(blog, many = False)
    #     return Response(serializer.data)

class BlogUpdate(UpdateAPIView):

    queryset = Blog.objects.all()
    serializer_class = BlogUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        blog = get_object_or_404(Blog, pk = pk)
        serializer = self.serializer_class(blog, data = request.data)
        if request.user == blog.creator:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('You are not allowed to edit this blog!')

class BlogDelete(DestroyAPIView):

    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, pk = pk)
        if request.user == blog.creator:
            blog.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response('You are not allowed to delete this blog!')
