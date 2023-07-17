import random
from datetime import datetime, timedelta

from django.utils import timezone
from UWEflix_Website.models import Movie, Screen, Showing

def add_random_showings():
    movies = Movie.objects.all()
    screens = Screen.objects.all()

    for _ in range(250):
        random_movie = random.choice(movies)
        random_screen = random.choice(screens)

        random_date = timezone.now() + timedelta(days=random.randint(1, 60))
        random_hour = random.randint(8, 22)
        random_time = datetime.strptime(f"{random_hour:02d}:00", "%H:%M").time()

        showing = Showing(
            movie=random_movie,
            date_showing=random_date.date(),
            time_showing=random_time,
            screen=random_screen,
        )
        showing.save()

add_random_showings()
