from django.contrib.auth.decorators import user_passes_test

def not_logged_in_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, ("You dont have access to this page."))
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def group_required(group_name):
    def decorator(view_func):
        @user_passes_test(lambda user: 
                          user.groups.filter(name=group_name).exists(), 
                          login_url='login')
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
