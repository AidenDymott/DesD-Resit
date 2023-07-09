from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import ValidationError
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime, timedelta, date
from .forms import (SignUpForm, PaymentForm, MovieForm, ShowingForm, 
                    ScreenForm, ClubForm, BookingForm, TicketForm)
from .models import Movie, Showing, Booking, Ticket, Screen, Club
from .decorators import group_required, not_logged_in_required

def home(request):
    showings = Movie.objects.latest('movie_name')
    return render(request, 'home.html', {'showings': showings})

@not_logged_in_required
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in."))
            return redirect('home')
        else:
            messages.success(request, ("Error logging in."))
            return redirect('login')   
    else:
        return render(request, 'login_user.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out."))    
    return redirect('home')

@not_logged_in_required
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login user on sign up
            user = authenticate(username = username, password = password)
            group = Group.objects.get(name="Customer")
            user.groups.add(group)
            messages.success(request, ("Sign up successful"))
            login(request, user)
            return redirect('home')     
    return render(request, 'register.html', {'form':form})

@not_logged_in_required
def club_register(request):
    register_form = SignUpForm()
    club_form = ClubForm()
    if request.method == 'POST':
        register_form = SignUpForm(request.POST)
        club_form = ClubForm(request.POST)
        if register_form.is_valid() and club_form.is_valid():
            register_form.save()

            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password1']
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user)
                group = Group.objects.get(name="Club Representative")
                user.groups.add(group)

                club = club_form.save(commit=False)
                club.club_rep = request.user
                club.save()
                messages.success(request, ("Club sign up successful"))
                return redirect('home')
    return render(request, 'register_club.html', {'register_form': register_form,
                                                  'club_form': club_form})

# Movie views
def list_movie(request):
    movie_list = Movie.objects.all().order_by('movie_name')
    p = Paginator(movie_list, 5)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    return render(request, 'movie.html', {'movie_list': page})

def show_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    return render(request, 'show_movie.html', {'movie': movie})

def search_movie(request):
    query = request.GET.get('q')
    movies = Movie.objects.filter(movie_name__icontains=query) if query else []
    return render(request, 'movie.html', {'movie_list': movies, 
                                          'query': query})

@login_required(login_url="login")
@group_required("Manager")
def add_movie(request):
    form = MovieForm()
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, ("New movie added"))
            return redirect('movie')   
    return render(request, 'add_movie.html', {'form':form})

@login_required(login_url="login")
@group_required("Manager")
def update_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    form = MovieForm(request.POST or None, instance=movie)
    if form.is_valid():
            form.save()
            messages.success(request, ("Update successful"))
            return redirect('movie')
    return render(request, 'update_movie.html', {'movie': movie, 'form':form})

@login_required(login_url="login")
@group_required("Manager")
def delete_movie(request, movie_id):
    # TODO:
    # Reject request to delete when there is active showings for the current
    # movie.
    movie = Movie.objects.get(pk=movie_id)
    movie.delete()
    messages.success(request, ("Deletion successful"))
    return redirect('movie')

# Showing views
def showing(request, year=None, month=None, day=None):
    if year and month and day:
        date_to_get = date(int(year), int(month), int(day))
    else:
        date_to_get = datetime.now().date()

    date_list = []
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=5)
    while current_date < end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    showing_list = Showing.objects.filter(date_showing=date_to_get).order_by('time_showing')

    return render(request, 'showing.html', {'showing_list': showing_list,
                                            'date_list': date_list})

def show_showing(request, showing_id):
    showing = Showing.objects.get(pk=showing_id)
    return render(request, 'list_showing.html', {'showing':showing})

def search_showing(request):
    # TODO:
    # Filter showings to only display upcoming.
    query = request.GET.get('q')
    showings = Showing.objects.filter(movie__movie_name__icontains=query) if \
        query else []
    return render(request, 'showing.html', {'showing_list': showings, 
                                            'query': query})

@login_required(login_url="login")
@group_required("Manager")
def add_showing(request):
    form = ShowingForm()
    if request.method == "POST":
        form = ShowingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("New showing added")) 
            return redirect('showing')
    return render(request, 'add_showing.html', {'form':form})

@login_required(login_url="login")
@group_required("Manager")
def update_showing(request, showing_id):
    showing = Showing.objects.get(pk=showing_id)
    form = ShowingForm(request.POST or None, instance=showing)
    if form.is_valid():
        form.save()
        messages.success(request, ("Update successful"))
        return redirect('showing')
    return render(request, 'update_showing.html',
                  {'showing':showing, 'form':form})

@login_required(login_url="login")
@group_required("Manager")
def delete_showing(request, showing_id):
    # TODO:
    # Either disallow deleting a showing with active bookings or send an email
    # refunding the customer.
    showing = Showing.objects.get(pk=showing_id)
    showing.delete()
    messages.success(request, ("Deletion successful"))
    return redirect('showing')
    
# Booking views
@login_required(login_url="login")
@permission_required("UWEflix_Website.add_booking", login_url="login")
def create_booking(request, showing_id):
    showing = Showing.objects.get(id=showing_id)
    booking_form = BookingForm(showing=showing)
    # Redirect to club booking if the user is a club representative
    if request.user.groups.filter(name="Club Representative").exists():
        # Club tickets are always (student - discount).
        ticket = Ticket.objects.get(type="student")
        context = { 'booking_form': booking_form,
                    'showing': showing,
                    'ticket': ticket}
        return render(request, 'create_club_booking.html', context)

    payment_form = PaymentForm()
    tickets = Ticket.objects.all()
    context = { 'booking_form': booking_form,
                'payment_form': payment_form,
                'showing': showing,
                'tickets': tickets}
    return render(request, 'create_booking.html', context)

@login_required(login_url="login")
@group_required("Customer")
def process_booking(request, showing_id):
    showing = Showing.objects.get(id=showing_id)
    booking_form = BookingForm(request.POST, showing=showing)
    payment_form = PaymentForm(request.POST)

    if booking_form.is_valid() and payment_form.is_valid():
        selected_seats = []
        for seat in booking_form.cleaned_data:
            if booking_form.cleaned_data[seat]:
                selected_seats.append(seat)

        num_children = payment_form.cleaned_data['children']
        num_students = payment_form.cleaned_data['students']
        num_adults = payment_form.cleaned_data['adults']
        total_tickets = num_children + num_students + num_adults
        
        # Handle some cases where there is incompatible data
        if len(selected_seats) == 0:
            messages.success(request, ('No seats selected.'))
            return redirect('create-booking', showing_id)

        if total_tickets != len(selected_seats):
            messages.success(request, ('''Amount of tickets and seats did not 
                                       match.'''))
            return redirect('create-booking', showing_id)

        card_number = payment_form.cleaned_data['card_number']
        if not is_valid_card_number(card_number):
            messages.success(request, ('Invalid card number'))
            return redirect('create-booking', showing_id)

        if not showing.check_available_seats(selected_seats):
            messages.success(request, ('''Sorry but those seats were
                                       taken while you were creating
                                       a booking'''))
            return redirect('create-booking', showing_id)
        
        showing.assign_seats(selected_seats)
        showing.available_seats -= len(selected_seats)

        # Payment processing should happen here.
        adult_price = int(Ticket.objects.get(type='adult').price)
        child_price = int(Ticket.objects.get(type='child').price)
        student_price = int(Ticket.objects.get(type='student').price)
        total_price = (adult_price*num_adults) + (child_price*num_children) + \
                (student_price*num_students)

        # Once payment has happened save the booking.
        booking = Booking(user=request.user, showing=showing,
                          seats=selected_seats)
        showing.save()
        booking.save()

        messages.success(request, ("Booking added"))
        return render(request, 'booking_confirm.html')
    messages.success(request, ("Something went wrong"))
    return render(request, 'booking_confirm.html')

def is_valid_card_number(card_number):
    reversed = card_number[::-1]
    doubled = []
    for index, digit in enumerate(reversed):
        if index % 2 == 1:
            tmp = int(digit) * 2
            if tmp > 9:
                tmp -= 9
            doubled.append(tmp)
        else:
            doubled.append(int(digit))
    return sum(doubled) % 10 == 0

@login_required(login_url="login")
@group_required("Club Representative")
def process_club_booking(request, showing_id):
    showing = Showing.objects.get(id=showing_id)
    club = Club.objects.get(club_rep = request.user)
    booking_form = BookingForm(request.POST, showing=showing)

    if booking_form.is_valid():
        selected_seats = []
        for seat in booking_form.cleaned_data:
            if booking_form.cleaned_data[seat]:
                selected_seats.append(seat)
        total_tickets = len(selected_seats)
        
        # TODO:
        # Update with discount when added to models.
        total_cost = len(selected_seats) * float(Ticket.objects.get(
                                                 type="student").price)
        club_funds = float(club.account_balance)
        
        # Handle some cases where there is incompatible data
        if total_tickets == 0:
            messages.success(request, ('No seats selected.'))
            return redirect('create-booking', showing_id)
        if total_tickets < 10:
            messages.success(request, ('A club booking requires 10 seats.'))
            return redirect('create-booking', showing_id)
        if total_cost > club_funds:
            messages.success(request, ('Not enough funds in account.'))
            return redirect('create-booking', showing_id)

        if not showing.check_available_seats(selected_seats):
            messages.success(request, ('''Sorry but those seats were
                                       taken while you were creating
                                       a booking'''))
            return redirect('create-booking', showing_id)
        
        showing.assign_seats(selected_seats)
        showing.available_seats -= len(selected_seats)

        booking = Booking(user=request.user, showing=showing,
                          seats=selected_seats)
        showing.save()
        booking.save()

        messages.success(request, ("Booking added"))
        return render(request, 'booking_confirm.html')
    messages.success(request, ("Something went wrong"))
    return render(request, 'booking_confirm.html')

def show_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'show_bookings.html', {'bookings': bookings})

# SCREEN CRUD
@login_required(login_url="login")
@group_required("Manager")
def screen(request):
    list = Screen.objects.all()
    return render(request, 'screen.html', {'list':list})

@login_required(login_url="login")
@group_required("Manager")
def add_screen(request):
    form = ScreenForm()
    if request.method == "POST":
        form = ScreenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Screen Added successfully"))
            return redirect('screen')
    return render(request, 'add_screen.html', {'form':form})

@login_required(login_url="login")
@group_required("Manager")
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
    
@login_required(login_url="login")
@group_required("Manager")
def delete_screen(request, screen_id):
    try:
        screen = Screen.objects.get(pk=screen_id)
        screen.delete()
        messages.success(request, ("Screen Deleted"))
    except ValidationError:
        screen = Screen.objects.get(pk=screen_id)
        messages.success(request, ("Cannot delete screen with active showings"))
    return redirect('screen')

# Club views
@login_required(login_url="login")
@group_required("Club Representative")
def my_club(request):
    club = Club.objects.get(club_rep = request.user)
    return render(request, 'my_club.html', {'club': club })

@login_required(login_url="login")
@group_required("Manager")
def list_club(request):
    club = Club.objects.all()
    return render(request, 'club_list.html', {'club':club})

@login_required(login_url="login")
@group_required("Manager")
def update_club(request, club_id):
    club = Club.objects.get(pk=club_id)
    form = ClubForm(request.POST or None, instance=club)
    if form.is_valid():
        form.save()
        messages.success(request, ("Update successful"))
        return redirect('list-club')
    return render(request, 'update_club.html',
                  {'club':club, 'form':form})

@login_required(login_url="login")
@group_required("Manager")
def delete_club(request, club_id):
    club = Club.objects.get(pk=club_id)
    club.delete()
    messages.success(request, ("Club Removed"))
    return redirect('list-club')

@login_required(login_url="login")
@group_required("Manager")
def edit_ticket_prices(request):
    form = TicketForm(initial = {
                       "adult": Ticket.objects.get(type='adult').price,
                       "child": Ticket.objects.get(type='child').price,
                       "student": Ticket.objects.get(type='student').price}) 
    if request.method == "POST":
        # TODO:
        # Make this update ticket prices.
        pass
    return render(request, 'edit_tickets.html', {'form':form})
