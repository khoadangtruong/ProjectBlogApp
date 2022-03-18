from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from blog.models import Blog, Comment
from .serializers import (
    BlogSerializer,
    
)
from rest_framework.permissions import IsAuthenticated

class BlogAPIView(ListCreateAPIView):

    queryset = Blog.objects \
    .select_related('creator') \
    .prefetch_related('comment_set').all()

    serializer_class = BlogSerializer

    permission_classes = [IsAuthenticated]

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = self.serializer_class(queryset, many = True)
    #     return Response(serializer.data)


    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save(creator = self.request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BlogDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Blog.objects.select_related('creator').prefetch_related('comment_set').all()
    serializer_class = BlogSerializer

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

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, pk = pk)
        if request.user == blog.creator:
            blog.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response('You are not allowed to delete this blog!')