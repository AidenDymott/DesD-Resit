from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import HttpResponseRedirect
from . forms import SignUpForm, MovieForm
from .models import Movie

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

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

# Movie CRUDs
def list_movie(request):
    movie_list = Movie.objects.all()
    return render(request, 'movie.html', {'movie_list': movie_list})

def add_movie(request):
    submitted = False
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_movie?submitted=True')
    else:
        form = MovieForm
        if 'submitted' in request.GET:
            submitted = True    
    return render(request, 'add_movie.html', {'form':form, 'submitted':submitted})
    
def show_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    return render(request, 'show_movie.html', {'movie': movie})

def update_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    form = MovieForm(request.POST or None, instance=movie)
    if form.is_valid():
            form.save()
            return redirect('movie')
    return render(request, 'update_movie.html', {'movie': movie, 'form':form})

def delete_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    movie.delete()
    return redirect('movie')