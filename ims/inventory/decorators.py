from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied


def permission_denied_view(request):
    # print("OK in deco")
    raise PermissionDenied


def admin_required(view_func=None, login_url='permission_denied_view'):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    """
    # print("OK in second")
    actual_decorator = user_passes_test(
        lambda u: Group.objects.get(name='Superuser' ) in u.groups.all(),
        login_url="permission_denied_view"
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
