# functions that can be reused throughout the applications

from .models import Device, Logs, DecomissionedItems


def decomission_delete(request, ins = None, status = False):
    """function called on decomission/delete of item."""
    try:
        device = Device.objects.get(pk = int(ins))
        new_device = DecomissionedItems(
            iepl_id = device.iepl_id,
            service_tag = device.service_tag,
            item_type = device.item_type,
            host_name = device.host_name,
            po_number = device.po_number,
            po_date = device.po_date,
            manufacturer = device.manufacturer,
            model_no = device.model_no,
            project = device.project,
            location = device.location,
            desk_no = device.desk_no,
            asset_code = device.asset_code,
            cpu = device.cpu,
            cpu_speed = device.cpu_speed,
            monitor_model = device.monitor_model,
            os = device.os,
            ram = device.ram,
            hdd = device.hdd,
            extra_monitor_model = device.extra_monitor_model,
            status = status,
            created_by=request.user
        )
        new_device.save()
        return True
    except:
        return False


def set_transaction_logs(request, ins = None, status = "Added", detail_info = "State Default Argu", allot_to = None,):
    """function for setting transaction logs"""
    try:
        device = Device.objects.get(pk = int(ins))
        if allot_to is not None:
            log = Logs(
                device=device,
                status=status,
                user=request.user,
                allot_to_id = int(allot_to),
                details = detail_info
            )
            log.save()
        else:
            log = Logs(
                device=device,
                status=status,
                user=request.user,
                details = detail_info
            )
            log.save()
        return True
    except:
        return False
