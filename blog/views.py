from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import BlogForm
from .models import Category, Blog, Comment

# Create your views here.

# ========== Blog Index ==========
# ========== Blog Index ==========
# ========== Blog Index ==========

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blogs = Blog.objects.filter(
        Q(category__name__icontains = q) | 
        Q(name__icontains = q)
    )
    categories = Category.objects.all()
    blog_count = blogs.count()

    context = {
        'blogs': blogs,
        'categories': categories,
        'blog_count': blog_count
    }

    return render(request, 'blog/index.html', context)

# ========== Blog CRUD ==========
# ========== Blog CRUD ==========
# ========== Blog CRUD ==========

@login_required(login_url='login')
def blogCreate(request):
    categories = Category.objects.all()
    form = BlogForm()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name = category_name)

        Blog.objects.create(
            name = request.POST.get('name'),
            category = category,
            creator = request.user,
            description = request.POST.get('description'),
            body = request.POST.get('body'),
            logo = request.FILES.get('logo'),
        )
        return redirect('blog-index')

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'blog/blog_form.html', context)

def blog(request, pk):
    categories = Category.objects.all()
    blog = Blog.objects.get(pk = pk)
    blog_comments = blog.comment_set.all()
    participants = blog.participants.all()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            blog = blog,
            body = request.POST.get('body')
        )
        blog.participants.add(request.user)
        return redirect('blog-detail', pk = blog.id)

    context = {
        'blog': blog,
        'categories': categories,
        'blog_comments': blog_comments,
        'participants': participants
    }
    return render(request, 'blog/blog.html', context)

def blogUpdate(request, pk):
    blog = Blog.objects.get(pk = pk)
    form = BlogForm(instance = blog)
    categories = Category.objects.all()

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name = category_name)
        blog.name = request.POST.get('name')
        blog.category = category
        blog.creator = request.user
        blog.description = request.POST.get('description')
        blog.body = request.POST.get('body')
        blog.save()
        return redirect('blog-detail', pk = blog.id)

    context = {
        'form': form,
        'categories': categories,
        'blog': blog,
    }
    return render(request, 'blog/blog_form.html', context)


def blogDelete(request, pk):
    blog = Blog.objects.get(pk = pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog-index')

    context = {
        'obj': blog
    }

    return render(request, 'blog/delete.html', context)

def commentDelete(request, pk):
    comment = Comment.objects.get(pk = pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog-detail', pk = comment.blog.id)
    
    context = {
        'obj': comment
    }

    return render(request, 'blog/delete.html', context)