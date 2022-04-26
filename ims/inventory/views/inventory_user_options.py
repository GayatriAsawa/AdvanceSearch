from typing import DefaultDict
from django.http.response import HttpResponse
from .modules import *

logger = logging.getLogger('logs')  # Instantiating logger.

@login_required(login_url=base.LOGIN_URL)
def information(request, allo_id):
    """User-group device management"""

    data = defaultdict()
    # if Group.objects.get(name='User') in request.user.groups.all():
    data['content_template'] = "inventory/information.html"
    try:
        data["allocation_items"] = Allocation.objects.get(id=allo_id)
        data["users"] = User.objects.filter(is_active=True).order_by("id")
        currentAllocation = Allocation.objects.get(id=allo_id)
        itemDetails = str(currentAllocation.service_tag.item_name)
        itemName = itemDetails.split(',')[0]
        itemDomain = itemDetails.split(',')[1]
        data['itemName'] = itemName
        data['itemDomain'] = itemDomain
    except:
        return redirect("permission_denied_view")
    logger.debug('Device information viewed by user - %s ' % request.user)
    return render(request, 'inventory/dashboard.html', data)

@login_required(login_url=base.LOGIN_URL)
def employee_obj(request):
    """function to get employee_obj for current logged in user"""
    """ Usage- in case of 'ifm-ldap server and EmployeeMaster table are in consideration. Else use the django user. """
    return (EmployeeMaster.objects.get(user=request.user))


@login_required(login_url=base.LOGIN_URL)
def transfer(request, allo_id):
    """Transfer item feature."""
    if request.POST:
        ids = Allocation.objects.get(id=allo_id)
        cnt = Report.objects.filter(allocation=ids).count()
        if cnt == 0:
            emp = EmployeeMaster.objects.get(
                user_id=int(request.POST["mySelect"]))
            if str(emp) == str(request.user):
                messages.error(
                    request, 'You cannot Transfer the Item from the existing user to the same user again !')
                return redirect(request.META['HTTP_REFERER'])
            else:
                r = Report(allocation=ids, report_action='transfer',
                        employee=emp, created_by=request.user)
                r.save()
                mess = "Transfer Request to " + emp.user.username + " is sent to Superuser"
                messages.success(request, mess)
                logger.debug('Device transferred by user- %s ' % request.user)
                return redirect(request.META['HTTP_REFERER'])
        else:
            try:
                Report.objects.get(allocation=ids, report_action='free_item')
                messages.error(
                    request, 'Please Wait Your Freeing this item request is pending')
                return redirect(request.META['HTTP_REFERER'])
            except:
                try:
                    Report.objects.get(
                        allocation=ids, report_action='incorrect')
                    messages.error(
                        request, 'Please Wait Your Incorrect item request is pending')
                    return redirect(request.META['HTTP_REFERER'])
                except:
                    try:
                        Report.objects.get(
                            allocation=ids, report_action='return_to_store')
                        messages.error(
                            request, 'Please Wait Your Return to Store this item request is pending')
                        return redirect(request.META['HTTP_REFERER'])
                    except:
                        Report.objects.get(
                            allocation=ids, report_action='transfer')
                        messages.error(
                            request, 'Please Wait Your Transferring this item request is pending')
                        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=base.LOGIN_URL)
def free_item(request, allo_id):
    """Free item feature for user - home page."""
    try:
        ids = Allocation.objects.get(id=allo_id)
    except:
        txt = 'Object not found'
        messages.error(request, txt)
        return redirect(request.META['HTTP_REFERER'])
    cnt = Report.objects.filter(allocation=ids).count()
    if cnt == 0:
        r = Report(allocation=ids, report_action='free_item',
                   employee=employee_obj(request), created_by=request.user)
        user = ids.allot_to
        r.save()
        txt = 'Your Request of Freeing this Item is send to superuser'
        messages.success(request, txt)
        logger.debug(txt)
        return redirect(request.META['HTTP_REFERER'])
    else:
        try:
            Report.objects.get(allocation=ids, report_action='free_item')
            messages.error(
                request, 'Please Wait Your Freeing this item request is pending')
            return redirect(request.META['HTTP_REFERER'])
        except ObjectDoesNotExist:
            try:
                Report.objects.get(allocation=ids, report_action='incorrect')
                messages.error(
                    request, 'Please Wait Your Incorrect item request is pending')
                return redirect(request.META['HTTP_REFERER'])
            except ObjectDoesNotExistDoesNotExist:
                try:
                    Report.objects.get(
                        allocation=ids, report_action='return_to_store')
                    messages.error(
                        request, 'Please Wait Your Return to Store this item request is pending')
                    return redirect(request.META['HTTP_REFERER'])
                except ObjectDoesNotExist:
                    Report.objects.get(
                        allocation=ids, report_action='transfer')
                    messages.error(
                        request, 'Please Wait Your Transfering this item request is pending')
                    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=base.LOGIN_URL)
def return_to_store(request, allo_id):
    """Return to store feature"""
    ids = Allocation.objects.get(id=allo_id)
    cnt = Report.objects.filter(allocation=ids).count()
    if cnt == 0:
        r = Report(allocation=ids, report_action='return_to_store',
                   employee=employee_obj(request), created_by=request.user)
        r.save()
        messages.success(
            request, 'Your Request of Returning Item is send to Superuser')
        logger.debug('Your Request of Returning Item is send to Superuser')
        return redirect(request.META['HTTP_REFERER'])
    else:
        try:
            Report.objects.get(allocation=ids, report_action='free_item')
            messages.error(
                request, 'Please Wait Your Freeing this item request is pending')
            return redirect(request.META['HTTP_REFERER'])
        except:
            try:
                Report.objects.get(allocation=ids, report_action='incorrect')
                messages.error(
                    request, 'Please Wait Your Incorrect item request is pending')
                return redirect(request.META['HTTP_REFERER'])
            except:
                try:
                    Report.objects.get(
                        allocation=ids, report_action='return_to_store')
                    messages.error(
                        request, 'Please Wait Your Return to Store this item request is pending')
                    return redirect(request.META['HTTP_REFERER'])
                except:
                    Report.objects.get(
                        allocation=ids, report_action='transfer')
                    messages.error(
                        request, 'Please Wait Your Transfering this item request is pending')
                    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=base.LOGIN_URL)
def incorrect(request, allo_id):
    """ Incorrect item  Assignment """
    ids = Allocation.objects.get(id=allo_id)
    cnt = Report.objects.filter(allocation=ids).count()
    if cnt == 0:
        r = Report(allocation=ids, report_action='incorrect',
                   employee=employee_obj(request), created_by=request.user)
        r.save()
        messages.success(
            request, 'Your Request of Incorrect Item is send to Superuser')
        logger.debug('Your Request of Incorrect Item is send to Superuser')
        return redirect(request.META['HTTP_REFERER'])
    else:
        try:
            Report.objects.get(allocation=ids, report_action='free_item')
            messages.error(
                request, 'Please Wait Your Freeing this item request is pending')
            return redirect(request.META['HTTP_REFERER'])
        except:
            try:
                Report.objects.get(allocation=ids, report_action='incorrect')
                messages.error(
                    request, 'Please Wait Your Incorrect item request is pending')
                return redirect(request.META['HTTP_REFERER'])
            except:
                try:
                    Report.objects.get(
                        allocation=ids, report_action='return_to_store')
                    messages.error(
                        request, 'Please Wait Your Return to Store this item request is pending')
                    return redirect(request.META['HTTP_REFERER'])
                except:
                    Report.objects.get(
                        allocation=ids, report_action='transfer')
                    messages.error(
                        request, 'Please Wait Your Transfering this item request is pending')
                    return redirect(request.META['HTTP_REFERER'])
