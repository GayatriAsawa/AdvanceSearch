"""forms.py file."""

from django.forms import *
from django.forms import ValidationError
from inventory.models import Device


class DeviceForm(ModelForm):

    class Meta:
        
        Choices = (
             (True,'Yes'),
             (False,'No')
        )
        
    
        
        
        monitor_manufacturer_ch = (
             ('DELL','DELL'),
             ('LENOVO','LENOVO'),
             ('ASUS','ASUS'),
             ('LG','LG'),
        )
        port_options = [
            ('1-HDMI','1-HDMI'),
            ('2-HDMI','2-HDMI'),
            ('3-HDMI','3-HDMI'),
            ('4-HDMI','4-HDMI'),

            ('1-VGA','1-VGA'),
            ('2-VGA','2-VGA'),
            ('3-VGA','3-VGA'),
            ('4-VGA','4-VGA'),

            ('1-Display Port','1-Display Port'),
            ('2-Display Port','2-Display Port'),
            ('3-Display Port','3-Display Port'),
            ('4-Display Port','4-Display Port'),
        ]
        model = Device
        fields = ('item_name','description', 'project','allocation_status','location',
                    'employee','manufacturer','manufacturer_part_no','comment','to_be_reimbursed',
                    'service_tag', 'item_type', 'host_name','local_admin','rent',
                    'model_no','cpu_type','cpu_speed','display_output',
                    'monitor_make','monitor_size', 'ram','storage','os',                                   
                    'customer_property',
                    'desk_no',  'asset_code',   'monitor_model',
                    'hdd', 'extra_monitor_model', 'warranty_expiry_date', 'po_year', 'po_initials', 'po_srno',
                    'floor_number','loc_type','loc_number',
                    'gin_year', 'gin_initials', 'gin_srno','monitor_manufacturer', 'subsidiary')

        widgets = {
            # ,'data-bv-callback':"true",,'gin_iqar_no'
            #     'data-bv-callback-message':"Wrong answer",
            #     'data-bv-callback-callback':"specialValidation" ,'style':"text-transform: uppercase"
            'item_name' : Select(attrs={'class': 'form-control', 'required': 'true','style':''}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'po_srno': NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'po_year' : Select(attrs={'class': 'form-control', 'required': 'true'}),
            'po_initials' : Select(attrs={'class': 'form-control', 'required': 'true'}),
            'manufacturer': Select(attrs={'class': 'form-control', 'required': 'true'}),
            'manufacturer_part_no': Select(attrs={'class': 'form-control', 'required': 'true'}),
            'to_be_reimbursed'  : Select(attrs={'class': 'form-control', 'required': 'true'},
                                        choices=Choices),
            'service_tag': TextInput(attrs={'class': 'form-control', 'required': 'true','style':'' }),
            'item_type': Select(attrs={'class': 'form-control', 'required': 'true'}),
            'rent': NumberInput(attrs={'class': 'form-control', 'required': 'true', 'placeholder': 'in INR'}),
            'cpu': NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'cpu_type': Select(attrs={'class': 'form-control', 'required': 'true'}),
            'cpu_speed': TextInput(attrs={'class': 'form-control', 'placeholder': 'in GHz'}),
            'display_output': TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'monitor_make': TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'monitor_size': TextInput(attrs={'class': 'form-control', 'placeholder': 'in cm'}),
            'ram': Select(attrs={'class': 'form-control', 'required': 'true'}),
            'hdd': TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'storage': TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'os': Select(attrs={'class': 'form-control', 'required': 'true'}),
            'warranty_expiry_date': DateInput(attrs={'class': 'form-control', 'required': 'true' ,'type' : "date"}),
            'customer_property': Select(attrs={'class': 'form-control', 'required': 'true'}, choices=Choices),
            'subsidiary': Select(attrs={'class': 'form-control', 'required': 'true'}),
            'monitor_model': TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'monitor_manufacturer' : Select(attrs={'class': 'form-control', 'required': 'true'},choices= monitor_manufacturer_ch), 
            'extra_monitor_model': TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            

            'gin_year' : Select(attrs={'class': 'form-control', 'required': 'false'}),
            'gin_initials' : Select(attrs={'class': 'form-control', 'required':'false'}),
            'gin_srno': NumberInput(attrs={'class': 'form-control', 'required':'false'}),
            # 'gin_iqar_no':TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'host_name': TextInput(attrs={'class': 'form-control',  'required': 'false'}),
             
            
            'model_no': TextInput(attrs={'class': 'form-control'}), 

            'project': Select(attrs={'class': 'form-control', 'onchange': 'getProject()', 'required':'false'}),
            'employee': Select(attrs={'class': 'form-control', 'required': 'false'}),
            'floor_number': Select(attrs={'class': 'form-control', 'required': 'false'}),
            'loc_type': Select(attrs={'class': 'form-control', 'required': 'false'}),
            'loc_number': NumberInput(attrs={'class': 'form-control', 'required': 'false'}),
            'location': Select(attrs={'class': 'form-control', 'required': 'false'}),
            'desk_no': TextInput(attrs={'class': 'form-control', 'required': 'false'}),
            'local_admin': TextInput(attrs={'class': 'form-control'}),
        
            'asset_code': TextInput(attrs={'class': 'form-control'}), 
            'allocation_status': Select(attrs={'class': 'form-control'}),
            
            'comment': TextInput(attrs={'class': 'form-control'}),
            
            
            
            
            ##For hardware
            # 'customer_property': Select(attrs={'class': 'form-control', 'required': 'true'}, choices=((0, 'No'), (1, 'Yes'))),
            
        }
