from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    email = models.EmailField(max_length = 256, null = True, blank = True)
    first_name = models.CharField(max_length= 256, null = True, blank = True)
    last_name = models.CharField(max_length= 256, null = True, blank = True)
    image = models.ImageField(default = 'avatar.svg', null = True, blank = True)

    def __str__(self):
        return f"{self.user.username}'s Profile"