from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.dispatch import receiver
from .models import UserProfile



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:    # Check if the user is newly created
        UserProfile.objects.create(user=instance)   # Create a UserProfile instance for the new user

@receiver(post_save, sender=User)    # Signal to save UserProfile after User is saved
def save_user_profile(sender, instance, created, **kwargs):   # Check if the user is newly created
    instance.userprofile.save()