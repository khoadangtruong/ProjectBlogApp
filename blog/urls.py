from django.urls import path

from .import views

urlpatterns = [
    path('', views.index, name = 'blog-index'),
    path('blog-create/', views.blogCreate, name = 'blog-create'),
    path('blog-detail/<str:pk>', views.blog, name = 'blog-detail'),
    path('blog-delete/<str:pk>', views.blogDelete, name = 'blog-delete'),
    path('comment-delete/<str:pk>', views.commentDelete, name = 'comment-delete'),
    path('blog-update/<str:pk>', views.blogUpdate, name = 'blog-update'),

]
