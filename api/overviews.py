from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        
        'register': 'auth/register/',
        'login': 'auth/login/',
        'logout': 'auth/logout/',

        'List': 'blog-list/',
        'Create': 'blog-create/',
        'Detail': 'blog-detail/<str:pk>/',
        'Update': 'blog-update/<str:pk>/',
        'Delete': 'blog-list//<str:pk>/'
    }
    return Response(api_urls)