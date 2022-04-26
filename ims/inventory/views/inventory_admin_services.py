from typing import DefaultDict
from django.http.response import HttpResponse
from .modules import *
from .inventory_user_options import employee_obj

logger = logging.getLogger('logs')  # Instantiating logger.



@login_required(login_url=base.LOGIN_URL)
def device_information(request, allo_id):
    """ Superuser All request device information check."""

    data = defaultdict()
    if Group.objects.get(name='Superuser') in request.user.groups.all():
        try:
            data['content_template'] = "inventory/device_information.html"
            reports = Report.objects.get(id=allo_id)
            if reports.report_action == 'transfer':
                t = reports.employee.user.username
                msg = "Transfer to " + t
            elif reports.report_action == 'incorrect':
                msg = "Incorrect"
            elif reports.report_action == 'return_to_store':
                msg = "Return to store"
            elif reports.report_action == 'free_item':
                msg = "Free Item"
            data['allocation_items'] = reports
            data['msg'] = msg
            itemDetails = str(reports.allocation.service_tag.item_name)
            itemName = itemDetails.split(',')[0]
            itemDomain = itemDetails.split(',')[1]
            data['itemName'] = itemName
            data['itemDomain'] = itemDomain
            return render(request, "inventory/dashboard.html", data)
        except:
            return redirect('dashboard')
        logger.debug(
            'All request device information checked by user - %s ' % request.user)
    return render(request, "inventory/dashboard.html", data)


@login_required(login_url=base.LOGIN_URL)
def accept(request, allo_id):
    """Accept the Report request"""
    try:
        objs = Report.objects.get(id=allo_id)
    except:
        messages.error(request, "Object not Found")
        return redirect(request.META['HTTP_REFERER'])
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    x = datetime_ist.strftime('%Y:%m:%d %H:%M:%S')
    msg = ''
    if objs.report_action == 'transfer':
        Allocation.objects.filter(
            service_tag=objs.allocation.service_tag.id).delete()
        allo = Allocation(service_tag=objs.allocation.service_tag,
                          allot_to=objs.employee.user, date=timezone.now())
        allo.save()
        userEmployee = User.objects.get(username=str(objs.employee.user))
        device = Device.objects.get(id=objs.allocation.service_tag.id)
        device.employee = userEmployee
        device.save()
        set_transaction_logs(
            request, objs.allocation.service_tag.id, "Transferred", "Allocated to User -> "+ str(objs.employee.user))
        objs.delete()
        h = History_log(service_tag=objs.allocation.service_tag, employee=objs.employee, date=timezone.now(),
                        status="Allocated")
        h.save()
        messages.success(request, 'Request Accepted Successfully !!')
        logger.debug('Request Accepted Successfully !!')
        return redirect(request.META['HTTP_REFERER'])
    elif objs.report_action == 'incorrect' or objs.report_action == 'return_to_store' or objs.report_action == 'free_item':
        try:
            # de = Device.objects.get(
            #     iepl_id=objs.allocation.service_tag.iepl_id)
            # de.allocation_status = False
            # de.save()
            # h = History_log(service_tag=de, employee=objs.employee,
            #                 date=timezone.now(), status="Free")
            # h.save()
            # if objs.report_action == 'return_to_store':
            #     msg = "Returned To Store"
            # if objs.report_action == 'free_item':
            #     msg = 'Free'
            # set_transaction_logs(request, de.id, msg)
            # Allocation.objects.filter(
            #     service_tag=objs.allocation.service_tag.id).delete()
            # objs.delete()
            # messages.success(request, 'Request Accepted Successfully !!')
            # logger.debug('Request Accepted Successfully msg 2 !!')
            de = Device.objects.get(
                iepl_id=objs.allocation.service_tag.iepl_id)
            de.allocation_status = "Free"
            de.project = None
            de.employee = None
            de.save()
            h = History_log(service_tag=de, employee=objs.employee,
                            date=timezone.now(), status="Free")
            h.save()
            if objs.report_action == 'return_to_store':
                msg = "Returned To Store"
            if objs.report_action == 'free_item':
                msg = 'Free'
            set_transaction_logs(request, de.id, msg)
            Allocation.objects.filter(
                service_tag=objs.allocation.service_tag.id).delete()
            objs.delete()
            messages.success(request, 'Request Accepted Successfully !!')
            logger.debug('Request Accepted Successfully msg 2 !!')
        except:
            messages.error(request, 'Request Accepted Denied !!')
            logger.debug('Request Accepted Denied !!')
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=base.LOGIN_URL)
def reject(request, allo_id):
    """Reject the Report request"""
    try:
        objs = Report.objects.get(id=allo_id)
        allo = Allocation.objects.get(
            service_tag=objs.allocation.service_tag.id)
        allo.comments = "Request Rejected"
        userEmployee = User.objects.get(username=str(objs.created_by))
        transactionMessage = objs.report_action
        transactionMessage = transactionMessage.capitalize()
        transactionMessage += " Request Rejected"
        set_transaction_logs(
            request, objs.allocation.service_tag.id, transactionMessage, "Transfer Request is rejected")
        allo.save()
        objs.delete()
        messages.success(request, 'Request Rejected')
        logger.debug('Request Rejected')
    except:
        messages.error(request, 'Operation Failed')
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=base.LOGIN_URL)
def create_service(request, allo_id):
    """Create Service Request """
    devices = Device.objects.filter(service_tag__iexact=allo_id)
    cnt = 0
    cnt = Service.objects.filter(service_tag__in=devices).count()
    if cnt == 0:
        for objs in devices:
            c = Service(service_tag=objs, employee=employee_obj(request))
            c.save()
        messages.success(
            request, 'Your Request of Service Item is send to Superuser')
        logger.debug('Your Request of Service Item is send to Superuser')
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(
            request, 'Please Wait Your/Another user\'s request is pending')
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=base.LOGIN_URL)
def create_reject_service_view(request, allo_id):
    """Create reject service view feature"""
    data = defaultdict()
    data["content_template"] = "inventory/create_service_info.html"
    try:
        services = Service.objects.get(id=allo_id)
    except:
        return redirect(request.META['HTTP_REFERER'])
    data['services'] = services
    return render(request, "inventory/dashboard.html", data)


@login_required(login_url=base.LOGIN_URL)
def release_service(request, allo_id):
    """Relesed Request function"""
    objs = Devices.objects.get(service_tag=allo_id)
    username = request.user.get_username()
    cnt = Create_service.objects.filter(service_tag=objs).count()
    comments = "Release request from " + username
    if cnt == 0:
        c = Create_service(service_tag=objs, release=1, LDAP_ID=username)
        c.save()
        Allocation.objects.filter(service_tag=objs).update(comments=comments)
        messages.success(
            request, 'Your Request of releasing Item is send to Superuser')
        logger.debug('Your Request of releasing Item is send to Superuser')
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(
            request, 'Please Wait Your/Another user\'s request is pending')
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=base.LOGIN_URL)
def borrow_service(request, allo_id):
    """Borrow service request"""
    objs = Devices.objects.get(service_tag=allo_id)
    u = Allocation.objects.get(service_tag=objs)
    username = request.user.get_username()
    cnt = Create_service.objects.filter(service_tag=objs).count()
    comments = "Borrow request from " + username
    if cnt == 0:
        c = Create_service(service_tag=objs, borrow=1, LDAP_ID=username)
        c.save()
        Allocation.objects.filter(service_tag=objs).update(comments=comments)
        messages.success(
            request, 'Your Request of borrowing Item is send to Superuser')
        logger.debug('Your Request of borrowing Item is send to Superuser')
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(
            request, 'Please Wait Your/Another user\'s request is pending')
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=base.LOGIN_URL)
def accept_service(request, allo_id):
    """Accept the Create Service request. """

    services = Service.objects.get(id=allo_id)
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    x = datetime_ist.strftime('%Y:%m:%d %H:%M:%S')
    if Allocation.objects.filter(
            service_tag=services.service_tag):  # check for allocation is done or not, if not, then allote
        Allocation.objects.filter(service_tag=services.service_tag)
        messages.success(request, 'Create service Initiated')
        services.delete()
    else:  # create the allocation obj for the service request.
        a = Allocation(service_tag=services.service_tag,
                       allot_to=services.employee.user, comment="--")
        d = Device.objects.filter(service_tag=services.service_tag.service_tag)
        d.update(allocation_status=1)
        h = History_log(service_tag=services.service_tag,
                        employee_id=services.employee.user.id, status="Allocated")
        h.save()
        a.save()
        services.delete()
        messages.success(request, 'Request Accepted Successfully !!')
    return redirect('dashboard')


@login_required(login_url=base.LOGIN_URL)
def reject_service(request, allo_id):
    """Reject the Create Service request. """
    services = Service.objects.filter(id=allo_id)
    services.delete()
    messages.success(request, 'Request Rejected Successfully !!')

    return redirect('dashboard')