from django.urls import path
from .import views

urlpatterns = [

    path('blog-list/', views.BlogList.as_view()),
    path('blog-create/', views.BlogCreate.as_view()),
    path('blog-detail/<str:pk>/', views.BlogDetail.as_view()),
    path('blog-update/<str:pk>/', views.BlogUpdate.as_view()),
    path('blog-delete/<str:pk>/', views.BlogDelete.as_view()),

]