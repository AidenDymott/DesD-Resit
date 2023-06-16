from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, ValidationError
from django import forms
from django.http import HttpResponseRedirect
from django.utils import timezone
from . forms import SignUpForm, MovieForm, ShowingForm, BookingForm, ScreenForm, ClubRegistration
from .models import Movie, Showing, Booking, Profile, Screen

# Create your views here.
def home(request):
    imaget = Movie.objects.all()
    return render(request, 'home.html', {'imaget':imaget})

#User Sign in
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!!!"))
            return redirect('home')
        else:
            messages.success(request, ("Error logging in!!!"))
            return redirect('login')   
    else:
        return render(request, 'login_user.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!!"))    
    return redirect('home')

# Customer Registration Form
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Log in User on sign up
            user = authenticate(username = username, password = password)
            messages.success(request, ("Sign up successful"))
            login(request, user)
            return redirect('home')     
    return render(request, 'register.html', {'form':form})

# Club Registration
def club_register(request):
    form = ClubRegistration()
    if request.method == 'POST':
        form = ClubRegistration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Club sign up successful"))
            return redirect('home')
    
    return render(request, 'register_club.html', {'form':form})

# Movie CRUDs
def list_movie(request):
    movie_list = Movie.objects.all()
    return render(request, 'movie.html', {'movie_list': movie_list})

def add_movie(request):
    form = MovieForm()
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, ("New movie added"))
            return redirect('movie')   
    return render(request, 'add_movie.html', {'form':form})
    
def show_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    return render(request, 'show_movie.html', {'movie': movie})

def update_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    form = MovieForm(request.POST or None, instance=movie)
    if form.is_valid():
            form.save()
            messages.success(request, ("Update successful"))
            return redirect('movie')
    return render(request, 'update_movie.html', {'movie': movie, 'form':form})

def delete_movie(request, movie_id):
    # TODO:
    # Reject request to delete when there is active showings for the current
    # movie.
    movie = Movie.objects.get(pk=movie_id)
    movie.delete()
    messages.success(request, ("Deletion successful"))
    return redirect('movie')

# Showing CRUD
def showing(request):
    # Display only showings in the future.
    cur_dt = timezone.now()
    showing_list = Showing.objects.filter(date_showing__gt=cur_dt.date(),
                                          time_showing__gt=cur_dt.time())
    return render(request, 'showing.html', {'showing_list': showing_list})

def show_showing(request, showing_id):
    showing = Showing.objects.get(pk=showing_id)
    return render(request, 'list_showing.html', {'showing':showing})

def add_showing(request):
    form = ShowingForm()
    if request.method == "POST":
        form = ShowingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("New showing added")) 
            return redirect('showing')
    return render(request, 'add_showing.html', {'form':form})

def update_showing(request, showing_id):
    showing = Showing.objects.get(pk=showing_id)
    form = ShowingForm(request.POST or None, instance=showing)
    if form.is_valid():
        form.save()
        messages.success(request, ("Update successful"))
        return redirect('showing')
    return render(request, 'update_showing.html',
                  {'showing':showing, 'form':form})

def delete_showing(request, showing_id):
    # TODO:
    # Either disallow deleting a showing with active bookings or send an email
    # refunding the customer.
    showing = Showing.objects.get(pk=showing_id)
    showing.delete()
    messages.success(request, ("Deletion successful"))
    return redirect('showing')
    
# BOOKING
def booking(request):
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Booking successful"))
            return redirect('booking-list')
    return render(request, 'booking.html', {'form':form})

def booking_list(request):
    list = Booking.objects.all()
    return render(request, 'booking_list.html', {'list':list})

def view_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    return render(request, 'view_booking.html', {'booking':booking})

def canceL_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    booking.delete()
    messages.success(request, ("Booking Canceleld"))
    return redirect('booking-list')

# SCREEN CRUD
def screen(request):
    list = Screen.objects.all()
    return render(request, 'screen.html', {'list':list})

def add_screen(request):
    form = ScreenForm()
    if request.method == "POST":
        form = ScreenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Screen Added successfully"))
            return redirect('screen')
    return render(request, 'add_screen.html', {'form':form})

def update_screen(request, screen_id):
    try:
        screen = Screen.objects.get(pk=screen_id)
        form = ScreenForm(request.POST or None, instance=screen)
        if form.is_valid():
            form.save()
            messages.success(request, ("Update successful"))
            return redirect('screen')
    except ValidationError:
        screen = Screen.objects.get(pk=screen_id)
        messages.success(request, ("Cannot update screen with active showings"))
    return render(request, 'update_screen.html', {'screen':screen, 'form':form})
    
def delete_screen(request, screen_id):
    try:
        screen = Screen.objects.get(pk=screen_id)
        screen.delete()
        messages.success(request, ("Screen Deleted"))
    except ValidationError:
        screen = Screen.objects.get(pk=screen_id)
        messages.success(request, ("Cannot delete screen with active showings"))
    return redirect('screen')
