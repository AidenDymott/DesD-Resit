from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator

# Create user profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One user has one profile
    
    def __str__(self):
        return self.user.username
    
# Auto create user profile on sign up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user= instance )
        user_profile.save()
        
post_save.connect(create_profile, sender = User)

# Movie Database
class Movie(models.Model):
    movie_name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    rating= models.CharField(max_length = 3)
    
    def __str__(self):
        return self.movie_name
    
# Showings Database

class Screen(models.Model):
    screen_num = models.PositiveIntegerField(validators=[MaxValueValidator(10)], unique=True)# Max 10 screens
    seats = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return str(self.screen_num)

class Showing(models.Model):
    movie = models.ForeignKey(Movie, blank=True, null=True, on_delete=models.CASCADE)
    date_showing = models.DateTimeField('Movie Showing Date')
    time_showing = models.DateTimeField('Movie Showing Time')
    seats = models.IntegerField()
    
    def __str__(self):
        return str(self.movie) + ' ' + str(self.date_showing) + ' ' + str(self.time_showing)

# Booking DB

class Booking(models.Model):
    booked_movie = models.ForeignKey(Movie, blank=True, null=True, on_delete=models.CASCADE, related_name='bmovie')
    viewing_date = models.ForeignKey(Showing, blank=True, null=True, on_delete=models.CASCADE ,related_name='bdate')
    viewing_time = models.ForeignKey(Showing, blank=True, null=True, on_delete=models.CASCADE ,related_name='btime')
    booked_seats = models.ForeignKey(Showing, blank=True, null=True, on_delete=models.CASCADE, related_name='bseats')
    
    def __str__(self):
        return str(self.booked_movie) + ' ' + str(self.viewing_date) + ' ' + str(self.booked_seats)
    
    