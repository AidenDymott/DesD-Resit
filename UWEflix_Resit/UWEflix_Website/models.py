from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

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
