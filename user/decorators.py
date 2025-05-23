from django.shortcuts import redirect
from functools import wraps

def hod_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.user_type == 'head_of_department':
            return view_func(request, *args, **kwargs)
        return redirect('login')  # or a 403 page
    return _wrapped_view 

