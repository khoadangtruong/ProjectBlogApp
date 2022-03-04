from django.urls import path
from .import views, user_views, overviews
from rest_framework.authtoken import views as token_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path('', overviews.apiOverview, name = 'api-overview'),

    path('auth/login/', user_views.LoginView.as_view(), name = 'api_login'),
    path('auth/logout/', user_views.LogoutView.as_view(), name = 'api_logout'),
    path('auth/register/', user_views.RegisterView.as_view(), name = 'api_register'),
    # path('api-token-auth/', token_views.obtain_auth_token),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('blogs/', views.BlogAPIView.as_view(), name = 'blogs'),
    path('<str:pk>/', views.BlogDetailAPIView.as_view(), name = 'detail'),


]