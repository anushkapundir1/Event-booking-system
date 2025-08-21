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
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title    
