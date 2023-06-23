from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import ValidationError
from django.core.paginator import Paginator
from datetime import datetime
from .forms import SignUpForm, MovieForm, ShowingForm, ScreenForm, ClubRegistration, BookingForm
from .models import Movie, Showing, Booking, Profile, Screen, ClubAccount

# Create your views here.
def home(request):
    showings = Movie.objects.latest('movie_name')
    return render(request, 'home.html', {'showings': showings})

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
    movie_list = Movie.objects.all().order_by('movie_name')
    p = Paginator(movie_list, 5)
    page_num = request.GET.get('page', 1)
    
    page = p.page(page_num)
 
    return render(request, 'movie.html', {'movie_list': page})

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

def search_movie(request):
    query = request.GET.get('q')
    results = Movie.objects.filter(movie_name__icontains=query) if query else []
    return render(request, 'movie.html', {'results': results, 'query': query})

# Showing CRUD
def showing(request):
    # Display only showings in the future.
    cur_dt = datetime.now() 
    showing_list = Showing.objects.filter(date_showing__gt=cur_dt.date()) | \
                   (Showing.objects.filter(date_showing=cur_dt.date(),
                   time_showing__gt=cur_dt.time())).order_by('date_showing')
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

def search_showing(request):
    # TODO:
    # Filter showings to only display upcoming.
    query = request.GET.get('q')
    results = Showing.objects.filter(movie__movie_name__icontains=query) if query else []
    return render(request, 'showing.html', {'results': results, 'query': query})
    
# BOOKING
def create_booking(request, showing_id):
    # TODO:
    # Needs more logic for handling reducing the number of avaliable seats after booking
    # and checking if there is still seats available before saving the booking.
    showing = Showing.objects.get(id=showing_id)
    form = BookingForm(showing=showing)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            seats = form.cleaned_data['seats']
            booking = Booking(user=request.user, showing=showing, seats=seats)
            booking.save()

            # Logic for reducing seats needs changing, reducing is fine for
            # non social distancing events but social distanced events will 
            # need to be recalculated every time.

            # showing.seats -= int(seats)
            # showing.save()

            messages.success(request, ("Booking added"))
            return redirect('home')
    return render(request, 'create_booking.html', {'showing': showing, 'form': form})

def process_booking(request, showing_id):
    showing = Showing.objects.get(id=showing_id)
    form = BookingForm(request.POST, showing=showing)

    if form.is_valid():
        selected_seats = []
        for seat in form.cleaned_data:
            if form.cleaned_data[seat]:
                selected_seats.append(seat)

        # Check seats are available and make unavailable to future customers
        for seat_num in selected_seats:
            for seat in showing.seat_layout:
                if seat['seat_num'] == seat_num:
                    seat['is_available'] = False
                    break
        showing.save()

        messages.success(request, ("Booking added"))
        return render(request, 'booking_confirm.html')
    messages.success(request, ("Something went wrong"))
    return render(request, 'booking_confirm.html')

def show_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'show_bookings.html', {'bookings': bookings})

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

# Club CRUD

def list_club(request):
    list = ClubAccount.objects.all()
    return render(request, 'club_list.html', {'list':list})

"""
def update_club(request, acc_id):
    club = ClubAccount.objects.get(pk=acc_id)
    form = ClubRegistration(request.POST or None, instance = club)
    if form.is_valid():
        form.save()
        messages.success(request, ("Update successful"))
        return redirect('list-club')
    return render(request, 'update_club.html',
                  {'club':club, 'form':form})

def delete_club(request, acc_id):
    club = ClubAccount.objects.get(pk=acc_id)
    club.delete()
    messages.success(request, ("Club Removed"))
    return redirect('list-club')

"""
