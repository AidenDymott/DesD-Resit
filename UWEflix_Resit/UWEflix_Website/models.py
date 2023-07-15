from django.contrib.auth.forms import ValidationError
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
import json

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One user has one profile
    
    def __str__(self):
        return self.user.username

class Club(models.Model):
    club_name = models.CharField(max_length=200)
    landline = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    street_number = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200 , blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    club_rep = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(
            max_digits = 8, decimal_places = 2,
            validators=[MinValueValidator(limit_value=0)],
            blank=True, null=True)
    
    def __str__(self):
        return str(self.club_name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.account_balance = 0.00
        super().save(*args, **kwargs)

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user= instance )
        user_profile.save()
        
post_save.connect(create_profile, sender = User)

class Movie(models.Model):
    movie_name = models.CharField(max_length = 200)
    movie_image = models.ImageField(null = True, blank=True, upload_to="images/") 
    duration =  models.PositiveIntegerField('Duration', blank=True, null=True)
    description = models.CharField(max_length = 500)
    rating = models.CharField(max_length = 3)
    
    def __str__(self):
        return self.movie_name
    
class Screen(models.Model):
    screen_num = models.PositiveIntegerField(validators=[MaxValueValidator(10)], unique=True)# Max 10 screens
    rows = models.PositiveIntegerField(blank=True, null=True)
    columns = models.PositiveIntegerField(blank=True, null=True)
    seats = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return str(self.screen_num)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.seats = self.rows * self.columns
        if self.pk and self.showing_set.filter(date_showing__gte=datetime.now()).exists():
            raise ValidationError("Cannot update when there is active showings.")
        if self.pk:
            self.seats = self.rows * self.columns
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
    available_seats = models.PositiveIntegerField(blank=True, null=True)
    seat_layout = models.JSONField(default=list)
    social_distance = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return str(self.movie) + ' ' + str(self.date_showing) + ' ' + str(self.time_showing)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_seats = self.screen.seats

            seats = []
            for row in range(1, self.screen.rows+1):
                for column in range(1, self.screen.columns+1):
                    seat_num = f"{chr(64+row)}{column}"
                    seat_info = {'seat_num': seat_num, 'is_available': True}
                    seats.append(seat_info)
            self.seat_layout = seats
        super().save(*args, **kwargs)

    def check_available_seats(self, selected_seats):
        for seat_num in selected_seats:
            for seat in self.seat_layout:
                if seat['seat_num'] == seat_num:
                    if seat['is_available'] == False:
                        return False
        return True

    def assign_seats(self, selected_seats):
        for seat_num in selected_seats:
            for seat in self.seat_layout:
                if seat['seat_num'] == seat_num:
                    seat['is_available'] = False
                    break
        return

    def free_seats(self, selected_seats):
        for seat_num in selected_seats:
            print(seat_num)
            for seat in self.seat_layout:
                if seat['seat_num'] == seat_num:
                    seat['is_available'] = True
                    break
        return

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE, blank=True, null=True)
    seats = models.TextField()
    children = models.PositiveIntegerField(blank=True, null=True)
    student = models.PositiveIntegerField(blank=True, null=True)
    adult = models.PositiveIntegerField(blank=True, null=True)
    total_cost = models.DecimalField(
            max_digits = 8, decimal_places = 2,
            validators=[MinValueValidator(limit_value=0)],
            blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.seats = json.dumps(self.seats)
        super().save(*args, **kwargs)

    def get_seats(self):
        return json.loads(self.seats)

    def __str__(self):
        return str(self.user) + ' ' + str(self.showing)

class Ticket(models.Model):
    type = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(
            max_digits = 5, decimal_places = 2,
            validators=[MinValueValidator(limit_value=0)])

    def __str__(self):
        return str(self.type) + ' ' + str(self.price)

class Discount(models.Model):
    type = models.CharField(max_length=20, unique=True)
    perc = models.PositiveIntegerField()

    def __str__(self):
        return str(self.type) + ' ' + str(self.perc)
