from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from .tasks import send_confirmation_mail_task

# Create your views here.

def userLogin(request):

    if request.user.is_authenticated:
        return redirect('blog-index')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist!')
        
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('blog-index')
        else:
            messages.error(request, 'Username or Password does not exist!')

    return render(request, 'myuser/login.html')

def userLogout(request):

    logout(request)
    return redirect('blog-index')

def userRegister(request):

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # send_confirmation_mail_task.delay(user.email)
            return redirect('blog-index')
        else:
            messages.error(request, 'Opps! Some thing wrong')
    
    context = {
        'form': form
    }

    return render(request, 'myuser/register.html', context)

@login_required(login_url = 'login')
def profile(request):
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'myuser/profile.html', context)

# def schedule_mails(request):
#     schedule, created = CrontabSchedule.objects.get_or_create(hour = 16, minute = 30)
#     task = PeriodicTask.objects.create(
#         crontab = schedule, 
#         task = 'send_all_mail_task', 
#         name = 'schedule_mails_task_1'
#     )
#     return HttpResponse('Done')

