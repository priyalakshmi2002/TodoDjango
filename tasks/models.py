from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField()
    password1 = models.CharField(max_length=10)
    password2 = models.CharField(max_length=10)
    
    def __str__(self):
        return self.user.username

    

