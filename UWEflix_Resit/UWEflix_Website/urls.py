from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user , name = 'register'),
    path('club_register', views.club_register, name='register-club'),
    #MOVIE PATHS
    path('movie', views.list_movie, name='movie'),
    path('show_movie/<movie_id>', views.show_movie, name='show-movie'),
    path('update_movie/<movie_id>', views.update_movie, name='update-movie'),
    path('add_movie', views.add_movie, name='add-movie'),
    path('delete_movie/<movie_id>', views.delete_movie, name='delete-movie'),
    path('search_movie', views.search_movie, name='search-movie'),
    #SHOWING PATHS
    path('showing', views.showing, name='showing'),
    path('show_showing/<showing_id>', views.show_showing, name='show-showing'),
    path('add_showing', views.add_showing, name='add-showing'),
    path('update_showing/<showing_id>', views.update_showing, name='update-showing'),
    path('delete_showing/<showing_id>', views.delete_showing, name='delete-showing'),
    # BOOKING PATHS
    path('booking', views.booking, name='booking'),
    path('booking_list', views.booking_list, name = 'booking-list'),
    path('view_booking/<booking_id>', views.view_booking, name='view-booking'),
    path('cancel_booking/<booking_id>', views.canceL_booking, name='cancel-booking'),
    
    # SCREEN PATHS
    path('screen', views.screen, name='screen'),
    path('add_screen', views.add_screen, name='add-screen'),
    path('update_screen/<screen_id>', views.update_screen, name='update-screen'),
    path('delete_screen/<screen_id>', views.delete_screen, name='delete-screen'),    
]
