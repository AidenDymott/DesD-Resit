from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user , name = 'register'),
    #MOVIE PATHS
    path('movie', views.list_movie, name='movie'),
    path('show_movie/<movie_id>', views.show_movie, name='show-movie'),
    path('update_movie/<movie_id>', views.update_movie, name='update-movie'),
    path('add_movie', views.add_movie, name='add-movie'),
    path('delete_movie/<movie_id>', views.delete_movie, name='delete-movie'),
    #SHOWING PATHS
    path('showing', views.showing, name='showing'),
    path('show_showing/<showing_id>', views.show_showing, name='show-showing'),
    path('add_showing', views.add_showing, name='add-showing'),
    path('update_showing/<showing_id>', views.update_showing, name='update-showing'),
    path('delete_showing/<showing_id>', views.delete_showing, name='delete-showing'),
    # BOOKING PATHS
    path('booking', views.booking, name='booking'),
    path('booking_list', views.booking_list, name = 'booking-list'),
    path('view_booking/<booking_id', views.view_booking, name='view-booking'),
]
