# UWEFlix
A cinema booking system for a 3rd year module at UWE. Consists of 3 user roles,
each with different features; cinema manager, club representative and customers.


# Setup
```
docker-compose up --build
```

A manager user will have to be manually created.
```
python manage.py shell
```

```
from django.contrib.auth.models import User, Group

user = User.objects.create_user(username='testmanager', password='password')
group, _ = Group.objects.get_or_create(name='Manager')
user.groups.add(group)
user.save()
```

The site can be accessed at localhost:8000.
