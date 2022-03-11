from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from .tasks import db_health_check_task

# Create your views here.
def health_check_func(request):
    db_health_check_task.delay()
    return HttpResponse('Checked')
