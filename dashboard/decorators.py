from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_fun):
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_fun(request, *args, **kwargs)
        else:
            messages.warning(request,"Login required...")
            return redirect('dashboard:login')
    return wrapper_fun


from django.contrib.auth.decorators import \
    user_passes_test  # user_passes_test is a built-in Django decorator that checks whether a user passes a given test. If the test fails, the user is redirected to a login page or a specified URL
from django.core.exceptions import \
    PermissionDenied  # This is an exception that can be raised when a user does not have the required permissions to access a particular view.


# def admin_required(function=None):
#     """
#     Decorator for views that checks that the user is logged in and is an admin,
#     redirecting to the home page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_admin,
#         # The lambda function lambda u: u.is_active and u.is_admin is the test. It checks if: u.is_active: The user account is active. u.is_admin: The user is an admin.
#         login_url='dashboard:login',
#         redirect_field_name=None
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator
