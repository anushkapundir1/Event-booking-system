from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserProfileForm, EventForm
from .models import Event, UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render( request, 'events/home.html')

def register(request):
    if request.method == 'POST':  # Check if the request method is POST
        # Create instances of the forms with the submitted data
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()   # Save the user first
            profile = user.userprofile   # Create the profile but don't save it yet
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile) # Associate the profile with the user
            profile_form.save() # Now save the profile
            messages.success(request, f'Registration successful and account created for {user.username}!')
            login(request, user) # Log the user in after registration
            return redirect('home')  # Redirect to home page after successful registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        user_form = UserRegistrationForm() # Initialize the form
        profile_form = UserProfileForm()  # Initialize the profile form
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form}) # Render the registration template with the forms

def event_list(request):
    events = Event.objects.all().order_by('date_time')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})