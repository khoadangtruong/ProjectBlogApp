from django.db import models
# from myuser.models import User
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 256)

    def __str__(self):
        return self.name

class Blog(models.Model):
    name = models.CharField(max_length = 256)
    slug = models.SlugField(null = True, blank = True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
    creator = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    participants = models.ManyToManyField(User, related_name = 'participants', blank = True)
    description = models.TextField()
    body = models.TextField()
    logo = models.ImageField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name
    
    @property
    def comments(self):
        return self.comment_set.all()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return self.body[:50]