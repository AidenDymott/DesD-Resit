from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user , name = 'register'),
    path('movie', views.list_movie, name='movie'),
    path('show_movie/<movie_id>', views.show_movie, name='show-movie'),
    path('update_movie/<movie_id>', views.update_movie, name='update-movie'),
    path('add_movie', views.add_movie, name='add-movie'),
    path('delete_movie/<movie_id>', views.delete_movie, name='delete-movie'),
       
]
