from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def not_logged_in_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, ("You dont have access to this page."))
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        return wrapper
    return decorator
