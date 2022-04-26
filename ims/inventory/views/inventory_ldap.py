from typing import DefaultDict
from django.http.response import HttpResponse
from .modules import *

logger = logging.getLogger('logs')  # Instantiating logger.

@login_required(login_url=base.LOGIN_URL)
def ldap(request):
    """LDAPS Account's"""
    data = defaultdict()
    data["content_template"] = 'inventory/ldap.html'
    allow = []
    dis = []
    users = User.objects.all()
    for user in users:
        if user.is_superuser == 0 and user.is_staff == 0:
            if user.is_active:
                allow.append(user)
                logger.debug(
                    'User added in active list by user - %s ' % request.user)
            else:
                logger.debug(
                    'User added in de-active list by user - %s ' % request.user)
                dis.append(user)
    data['allow'] = allow
    data['dis'] = dis
    return render(request, "inventory/dashboard.html", data)


@login_required(login_url=base.LOGIN_URL)
def disallow(request):
    """Disallow Account"""
    msg = ''
    if request.method == "POST":
        lis = request.POST.getlist('name')
        for li in lis:
            u = User.objects.get(username=li)
            u.is_active = 0
            u.save()
            msg = 'Added {0} to disallowed user accounts list'.format(
                u.username)
            messages.success(request, msg)
            logger.debug(msg)
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=base.LOGIN_URL)
def allow(request):
    """Allow Accounts"""
    msg = ''
    if request.method == "POST":
        lis = request.POST.getlist('name')
        for li in lis:
            u = User.objects.get(username=li)
            u.is_active = 1
            u.save()
            msg = 'Added {0} to Allowed user accounts list'.format(u.username)
            messages.success(request, msg)
            logger.debug(msg)
    return redirect(request.META['HTTP_REFERER'])