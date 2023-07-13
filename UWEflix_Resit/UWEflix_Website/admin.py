from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import (Profile, Movie, Showing, Booking, Screen, Club, 
                     Ticket, Discount)

# Combine profile and user info
class ProfileInline(admin.StackedInline):
    model = Profile
    
# Extends User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = [ "username" ]
    inlines = [ProfileInline]
    
# Unregister User Temp
admin.site.unregister(User)

# Register Models
admin.site.register(User, UserAdmin)
admin.site.register(Movie)
admin.site.register(Showing)
admin.site.register(Booking)
admin.site.register(Screen)
admin.site.register(Club)
admin.site.register(Ticket)
admin.site.register(Discount)

# Combine profile and user info
class ProfileInline(admin.StackedInline):
    model = Profile
