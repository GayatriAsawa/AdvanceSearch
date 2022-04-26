"""filters.py file."""

import django_filters
from inventory.models import Device
from django_filters import CharFilter
from django_filters import OrderingFilter

class DeviceFilter(django_filters.FilterSet):
    o = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('project', 'project__project_id'),
            ('item_type', 'item_type'),
            ('manufacturer', 'manufacturer'),
            ('employee', 'employee'),
            ('location', 'location'),
            ('allocation_status', 'allocation_status'),
        ),

        # labels do not need to retain order
        field_labels={
            'project': 'Project',
            'item_type': 'Item-type',
            'manufacturer': 'Manufacturer',
            'employee': 'Employee',
            'location': 'Location',
            'allocation_status': 'allocation_status',
        })
    class Meta:
        model = Device
        fields = ['service_tag', 'item_type', 'manufacturer', 'project', 'employee', 'location', 'allocation_status']


