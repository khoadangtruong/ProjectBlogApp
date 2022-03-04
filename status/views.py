from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse


# Create your views here.
def health_check_func(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return HttpResponse('Ok')
    except Exception as ex:
        return HttpResponse(ex)

