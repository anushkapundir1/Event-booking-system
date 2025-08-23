from django.contrib import admin
from .models import UserProfile  # Importing UserProfile model
from .models import Event, Category ,Booking # Importing Event and Category models

admin.site.register(UserProfile)  # Registering UserProfile model with the admin site
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Booking)
# Register your models here.
