from django.db import models
from django.contrib.auth.models import User  # Importing User model for user-related fields
# Create your models here.

class UserProfile(models.Model): # User profile model to extend User functionality
    user= models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', default='profiles/default.png', blank=True, null=True)
    bio= models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
