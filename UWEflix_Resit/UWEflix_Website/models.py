from django.contrib.auth.forms import ValidationError
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator
from datetime import datetime
import uuid

# Create user profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One user has one profile
    
    def __str__(self):
        return self.user.username
    
# Club Rep        
class ClubAccount(models.Model):
    account_ID = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    club_name = models.CharField(max_length=200)
    landline = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    street_number = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200 , blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    club_rep = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.club_name)
    
# Auto create user profile on sign up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user= instance )
        user_profile.save()
        
post_save.connect(create_profile, sender = User)

# Movie Database
class Movie(models.Model):
    movie_name = models.CharField(max_length = 200)
    movie_image = models.ImageField(null = True, blank=True, upload_to="images/") 
    description = models.CharField(max_length = 500)
    rating= models.CharField(max_length = 3)
    
    def __str__(self):
        return self.movie_name
    
# Showings Database
class Screen(models.Model):
    screen_num = models.PositiveIntegerField(validators=[MaxValueValidator(10)], unique=True)# Max 10 screens
    seats = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    
    def __str__(self):
        return str(self.screen_num)

    def save(self, *args, **kwargs):
        if self.pk and self.showing_set.filter(date_showing__gte=datetime.now()).exists():
            raise ValidationError("Cannot update when there is active showings.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.pk and self.showing_set.filter(date_showing__gte=datetime.now()).exists():
            raise ValidationError("Cannot delete when there is active showings.")
        super().delete(*args, **kwargs)

class Showing(models.Model):
    movie = models.ForeignKey(Movie, blank=True, null=True, on_delete=models.CASCADE)
    date_showing = models.DateField('Movie Showing Date')
    time_showing = models.TimeField('Movie Showing Time')
    screen = models.ForeignKey(Screen, blank=True, null=True, 
                               on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    social_distance = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return str(self.movie) + ' ' + str(self.date_showing) + ' ' + str(self.time_showing)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.social_distance:
                self.seats = self.screen.seats / 2
            else:
                self.seats = self.screen.seats
        super().save(*args, **kwargs)

# Booking DB
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE, blank=True, null=True)
    seats = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return str(self.user) + ' ' + str(self.showing)
    
    
