from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return user_passes_test(lambda u: False)(view_func)(request, *args, **kwargs)
            
            user_role = request.user.profile.user_type
            if user_role not in allowed_roles:
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Role-specific decorators
def admin_required(view_func):
    return role_required(['admin'])(view_func)

def staff_required(view_func):
    return role_required(['admin', 'staff'])(view_func)

def head_of_department_required(view_func):
    return role_required(['admin', 'head_of_department'])(view_func)

def ict_required(view_func):
    return role_required(['admin', 'ict'])(view_func)

# Utility functions for checking roles
def is_admin(user):
    return user.is_authenticated and user.profile.user_type == 'admin'

def is_staff_member(user):
    return user.is_authenticated and user.profile.user_type in ['admin', 'staff']

def is_head_of_department(user):
    return user.is_authenticated and user.profile.user_type in ['admin', 'head_of_department']

def is_ict(user):
    return user.is_authenticated and user.profile.user_type in ['admin', 'ict'] 