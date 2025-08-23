from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserProfileForm, EventForm, BookingForm
from .models import Event, Category, UserProfile, Booking
from django.contrib.auth.decorators import login_required
from django.db.models import Sum   # ✅ Correct import

# Home Page
def home(request):
    return render(request, 'events/home.html')


# User Registration
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = user.userprofile
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            profile_form.save()

            messages.success(request, f'Registration successful! Welcome {user.username} 🎉')
            login(request, user)  # Auto-login after registration
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# Event List
def event_list(request):
    category = request.GET.get('category')  # get category from query string
    if category:
        events = Event.objects.filter(category__name=category).order_by('date_time')
    else:
        events = Event.objects.all().order_by('date_time')

    categories = Category.objects.all()  # send all categories to template
    return render(request, 'events/event_list.html', {'events': events, 'categories': categories, 'selected_category': category})


# Event Detail
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


# Create Event
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


# Update Event
@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


# Delete Event
@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


# Book Event
@login_required
def book_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            seats = form.cleaned_data['seats']

            # ✅ Fix: use Sum directly
            booked_seats = Booking.objects.filter(event=event).aggregate(Sum('seats'))['seats__sum'] or 0

            if booked_seats + seats > event.capacity:
                messages.error(request, "Not enough seats available!")
            else:
                Booking.objects.create(user=request.user, event=event, seats=seats)
                messages.success(request, "Booking successful!")
                return redirect('my_bookings')
    else:
        form = BookingForm()

    return render(request, 'events/book_event.html', {'event': event, 'form': form})


# My Bookings
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'events/my_bookings.html', {'bookings': bookings})
