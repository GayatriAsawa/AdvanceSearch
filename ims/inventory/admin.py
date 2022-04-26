"""admin.py file."""

from django.contrib import admin
from django.contrib.auth.models import User
from .models import CPUTYPE, OSS, RAMS, ItemName, ManufacturerPart, SubsidiaryMaster, ProjectMaster, EmployeeMaster, Item_type, Manufacturer, Location, Device, \
    Allocation, Report, Service, History_log, poYear, poIni
from adminsortable.admin import SortableAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class ProjectMasterAdmin(admin.ModelAdmin):
    search_fields = ['project_id']
    list_display = ['name', 'project_id', 'subsidiary1']

class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['username', 'first_name', 'last_name']

class EmployeeMasterAdmin(admin.ModelAdmin):
    model = EmployeeMaster
    search_fields = ['user__username']

class DeviceAdmin(SortableAdmin,admin.ModelAdmin):
    pass
    model = Device
    list_display = ('iepl_id', 'service_tag', 'project', 'item_type','allocation_status')
    list_filter = ['item_type', 'project', 'allocation_status' ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(SubsidiaryMaster)
admin.site.register(EmployeeMaster, EmployeeMasterAdmin)
admin.site.register(ProjectMaster, ProjectMasterAdmin)
admin.site.register(Item_type)
admin.site.register(Manufacturer)
admin.site.register(Location)
admin.site.register(poYear)
admin.site.register(poIni)

admin.site.register(ItemName)
admin.site.register(CPUTYPE)
admin.site.register(RAMS)
admin.site.register(ManufacturerPart)

admin.site.register(OSS)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Allocation)
admin.site.register(Report)
admin.site.register(Service)
admin.site.register(History_log)
admin.site.site_header = 'Inventory Management System - Admin Site'