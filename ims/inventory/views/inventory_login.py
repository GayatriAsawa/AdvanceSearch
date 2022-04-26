from typing import DefaultDict
from django.http.response import HttpResponse
from .modules import *

logger = logging.getLogger('logs')  # Instantiating logger.

def login(request):
    """function for login feature using ifm LDAP server"""

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        message = check_credentials(username, password)
        if message == 'loggedin':  # check for server response in terms of user_auth.
            user = auth.authenticate(username=username, password=password)
            if user is None:
                try:
                    user_obj = User.objects.get(username=username)
                    user_obj.set_password(password)
                    user_obj.save()
                    user = auth.authenticate(username=username, password=password)
                    logger.debug('Login successful for user - %s ' % user)
                except ObjectDoesNotExist:
                    user_obj = User.objects.create_user(username, 'Null@123', password)
                    employee = EmployeeMaster.objects.create(
                        user=user_obj)  # create employee obj too on user creation.
                    employee.save()
                    user = auth.authenticate(username=username, password=password)
                    (Group.objects.get(name='User')).user_set.add(user)
                    logger.debug('Created user - %s ' % user)
                auth.login(request, user)
                logger.debug('Login successful for user - %s ' % user)
                return redirect('dashboard')
            if user is not None:
                try:
                    user_obj = User.objects.get(username=username)
                    user_obj.set_password(password)
                    user_obj.save()
                    user = auth.authenticate(username=username, password=password)
                    logger.debug('Login successful for user - %s ' % user)
                except ObjectDoesNotExist:
                    user_obj = User.objects.create_user(username, 'Null@123', password)
                    employee = EmployeeMaster.objects.create(
                        user=user_obj)  # create employee obj too on user creation.
                    employee.save()
                    user = auth.authenticate(username=username, password=password)
                    (Group.objects.get(name='User')).user_set.add(user)
                auth.login(request, user)
                return redirect('dashboard')
            else:
                logger.debug('Unknown error for user - %s ' % user)
                messages.info(request, 'Account is deactivated, Please contact Superuser')
                return render(request, 'inventory/login.html')
        else:
            logger.debug('Login failed for user - ')
            messages.info(request, 'Invalid Username or Password')
            return render(request, 'inventory/login.html')
    else:
        return render(request, 'inventory/login.html')

#
# def login(request):
#     """Login function for all user."""
#
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#         # print(user)
#         if user is not None:
#             if user.is_active:
#                 # print("1223")
#                 auth.login(request, user)
#                 return redirect('dashboard')
#             else:
#                 # print("LOGIN1")
#                 messages.info(
#                     request, 'Account is deactivated Please contact superuser/Admin')
#                 return render(request, 'inventory/login.html')
#         else:
#             messages.info(request, 'Invalid Username or Password')
#             return render(request, 'inventory/login.html')
#     else:
#         return render(request, 'inventory/login.html')
#

def logout(request):
    """Logout Function for all users."""
    auth.logout(request)
    logger.debug('Log-out successful for user - %s ' % request.user)
    return redirect('/')


def login_option(request, user_id):
    """Login option feature."""
    user = User.objects.get(id=user_id)
    if user.groups.filter(name='Admin').exists():
        admin = 1
    else:
        admin = 0
    if user.groups.filter(name='Superuser').exists():
        superuser = 1
    else:
        superuser = 0
    return render(request, 'login_option.html', {'id': user.id,
                                                 'admin': admin,
                                                 'superuser': superuser,
                                                 })