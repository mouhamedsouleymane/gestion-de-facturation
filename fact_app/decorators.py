"""
Decorators and mixins for authentication and authorization
"""
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin


def superuser_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in and is a superuser,
    redirecting to the login page if necessary.
    
    Args:
        function: The view function to decorate
        redirect_field_name: Name of the redirect field in the URL
        login_url: URL to redirect to for login
    
    Returns:
        Decorated function that checks superuser status
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Mixin for class-based views that require superuser status
    """

    def test_func(self):
        """Check if user is a superuser"""
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        """Handle when user doesn't have permission"""
        from django.contrib import messages
        from django.shortcuts import redirect
        from django.utils.translation import gettext_lazy as _
        
        messages.error(self.request, _("You do not have permission to access this page."))
        return redirect('admin:login')