""" This is context processor file for - direct usage of variables declared in base.py to use in templates."""


from django.conf import settings


def ims_context_processor(request):
    ims_dict = {
        'InventoryManagementSystem_version': settings.InventoryManagementSystem_version,
    }
    return ims_dict
