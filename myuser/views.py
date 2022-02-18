from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

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

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('blog-index')
        else:
            messages.error(request, 'Opps! Some thing wrong')
    
    context = {
        'form': form
    }

    return render(request, 'myuser/register.html', context)