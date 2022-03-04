from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        
        'register': 'auth/register/',
        'login': 'auth/login/',
        'logout': 'auth/logout/',

        'List': 'blogs/',
        'Create': 'blogs/',
        'Detail': '<str:pk>/',
        'Update': '<str:pk>/',
        'Delete': '<str:pk>/'
    }
    return Response(api_urls)