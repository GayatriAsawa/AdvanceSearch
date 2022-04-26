from typing import DefaultDict
from django.http.response import HttpResponse
from .modules import *

logger = logging.getLogger('logs')  # Instantiating logger.

def custom_view(request, template='inventory/dashboard.html'):
    context = {
        'InventoryManagementSystem_version': InventoryManagementSystem_version}
    return render_to_response(template, context)


def home(request):
    return render(request, 'inventory/login.html')

@login_required(login_url=base.LOGIN_URL)
def dashboard(request):
    """Dashboard for Admin and Superuser.
    Consider Superuser group for all admin related rights assignment."""
    data = defaultdict()
    data['content_template'] = 'inventory/device_list.html'
    data['user'] = request.user
    user_group = request.user.groups.all().values('name')
    data['user_groups'] = [i['name'] for i in user_group]
    data['InventoryManagementSystem_version'] = InventoryManagementSystem_version
    """Check for superuser account access for current logged-in user."""
    if Group.objects.get(name='Superuser') in request.user.groups.all():
        data["transactions"] = Logs.objects.all().order_by("-id")
        data["items_list"] = Device.objects.all().order_by("-id")
        data["reports"] = Report.objects.all()
        data["services"] = Service.objects.all()
        data["my_items"] = Allocation.objects.filter(allot_to=request.user)
        data["SUDO"] = 1
        logger.debug('Superuser page view for user - %s ' % request.user)
        return render(request, "inventory/dashboard.html", data)
    else:
        """Dashboard for user only."""
        data["transactions"] = Logs.objects.all().order_by("-id")[:5]
        data["items_list"] = Device.objects.all().order_by("-id")
        data["my_items"] = Allocation.objects.filter(allot_to=request.user)
        data['SUDO'] = 0
        logger.debug('User page view - %s ' % request.user)
        return render(request, "inventory/dashboard.html", data)


def grey_page(request):
    """Gray Page for user only."""
    data = defaultdict()
    data['content_template'] = 'grey_page.html'
    data['user'] = request.user
    return render(request, "inventory/dashboard.html", data)

def projectData(request):
    if (request.GET['project_id'] == "---------"):
        return HttpResponse("")
    temp = ProjectMaster.objects.filter(project_id = request.GET['project_id'])
    return HttpResponse(temp[0].name)