from django.urls import path
from .import views, user_views, overviews
from rest_framework.authtoken import views as token_views


urlpatterns = [

    path('', overviews.apiOverview, name='api-overview'),

    path('auth/login/', user_views.LoginView.as_view()),
    path('auth/logout/', user_views.LogoutView.as_view()),
    path('auth/register/', user_views.RegisterView.as_view()),
    path('api-token-auth/', token_views.obtain_auth_token),

    path('blog-list/', views.BlogList.as_view()),
    path('blog-create/', views.BlogCreate.as_view()),
    path('blog-detail/<str:pk>/', views.BlogDetail.as_view()),
    path('blog-update/<str:pk>/', views.BlogUpdate.as_view()),
    path('blog-delete/<str:pk>/', views.BlogDelete.as_view()),

]