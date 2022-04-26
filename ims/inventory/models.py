"""moedls.py file."""

import decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import *
from datetime import date
import re
from django.db import models
from django.utils import timezone
# from django_mysql.models import ListCharField

#validation functions
# Create your models here.
def validate_decimals_cpu_speed(value):
    d = decimal.Decimal(str(value))
    print(d.as_tuple().exponent)
    if(d.as_tuple().exponent < -3):
        raise ValidationError(
            _('%(value)s Enter only upto three decimals'),
            params={'value': value},
        )

        
def validate_decimals_monitor_size(value):
    d = decimal.Decimal(str(value))
    if( d.as_tuple().exponent < -2 ):
        raise ValidationError(
            _('%(value)s Enter only upto two decimals'),
            params={'value': value},
        )  


def Disp(value):
    txt = value
    patt =  (txt.split('|'))
    for each in patt:
        each = each.strip()
        if(re.match(r"\d-\D",each) == None ):
            raise ValidationError(
            _('%(value)s Invalid Format Please follow x-opt|x-opt|x-opt type of format'),
            params={'value': value},
        )


def storage(value):
    txt = value
    patt =  (txt.split('|'))
    for each in patt:
        each = each.strip()
        if(re.match(r"\D-\d",each) == None ):
            raise ValidationError(
            _('%(value)s Invalid Format Please follow opt-x|opt-x|opt-x type of format'),
            params={'value': value},
        )


def service_tag_validator(value):
    if not value.isupper():
        raise ValidationError(
            _('please enter text in uppercase'),
            params={'value': value},
        )


def item_type_validator(value):
    
    for i in value:
        if i.isalpha():
            pass
        elif i == '_':
            pass
        else:
            raise ValidationError(
            _('%(value)s invalid'),
            params={'value': value},
        )


def item_name_validator(value):        
    for i in value:
        if i.isalnum():
            pass
        elif i == '_':
            pass
        else:
            raise ValidationError(
            _('%(value)s invalid'),
            params={'value': value},
        )


def project_status_validator(value):
    # print(value)
    for i in value:
        
        if i.isalnum():
            # print(i)
            pass
        elif i == '_' or i == ' ':
            pass
        else:
            raise ValidationError(
            _('%(value)s invalid'),
            params={'value': value},
        )


def username_validator(value):
    if not value.islower():
        raise ValidationError(
            _('%(value)s invalid'),
            params={'value': value},
        )

# Create your models here.


class SubsidiaryMaster(models.Model):
    """ Subsidiary master data model. """ 
    title = models.CharField(max_length=200)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Subsidiary"


class ProjectMaster(models.Model):
    """ Project master data model. """
    project_status_choices = (
        ('Active', 'Active'),
        ('On_hold', 'On_hold'),
        ('Suspended', 'Suspended'),
        ('Completed', 'Completed'),
    )
    name = models.CharField(max_length =255, blank = False, default='Not Assigned to Any Project')
    project_id = models.PositiveIntegerField(unique=True, validators=[
            MaxValueValidator(99999999),
            MinValueValidator(0)
        ], default = 0)
    subsidiary1 = models.ForeignKey(SubsidiaryMaster, on_delete=models.CASCADE)
    project_status = models.CharField(choices=project_status_choices, max_length=64, default='Active' ) #validators=[project_status_validator]

    def __str__(self):
        return str(self.project_id)

    class Meta:
        verbose_name_plural = 'Project'


class EmployeeMaster(models.Model):
    """ Employee master data model. """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)  

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Employee'


class Item_type(models.Model):
    """ Item type data list. """
    title = models.CharField(max_length=64, validators=[item_type_validator])

    def __str__(self):
        return self.title


class Manufacturer(models.Model):
    """ Manufacturer data list. """
    title = models.CharField(max_length=64, validators=[project_status_validator])

    def __str__(self):
        return self.title


class ManufacturerPart(models.Model):
    """ Manufacturer data list. """
    title = models.CharField(max_length=64,validators=[project_status_validator])

    def __str__(self):
        return self.title


class Location(models.Model):
    """ Location  data list. """
    location = models.CharField(max_length=150,default="1F-Q0")

    def __str__(self):
        return self.location


class ItemName(models.Model):
    """ Location  data list. """
    item_category_choices = (
        ('IT','IT'),
        ('Hardware', 'Hardware'),
        ('Administration', 'Administration'),
    )
    title = models.CharField(max_length=64,blank=True, validators=[item_name_validator])
    item_category = models.CharField(choices=item_category_choices, max_length=20, default = 'IT')
    def __str__(self):
        return (self.title + "," + self.item_category)


class CPUTYPE(models.Model):
    title = models.CharField(max_length=64,blank=True)

    def __str__(self):
        return self.title


class RAMS(models.Model):
    title = models.CharField(max_length=64,blank=True)

    def __str__(self):
        return self.title


class OSS(models.Model):
    title = models.CharField(max_length=64,blank=True)

    def __str__(self):
        return self.title

# class poNumber(models.Model):
#     po_year = models.CharField(max_length=5,blank=True)
#     po_initials = models.CharField(max_length=2,blank=True)
#     po_srno = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, null=True)


class poYear(models.Model):
    title = models.CharField(max_length=64,blank=True)

    def __str__(self):
        return self.title


class poIni(models.Model):
    title = models.CharField(max_length=64,blank=True)

    def __str__(self):
        return self.title





class Device(models.Model):
    """Device data model."""

    # iepl_id = models.CharField(db_index=True, blank=False, null=False)
    class Meta(object):
        ordering = ['iepl_id']

    local_admin_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('NA', 'NA'),
    )
    
    loc_type_choices = [
            ('D','Desk'),
            ('S','Cupboard'),
            ('Q','Incomming Quality Control'),
            ('E','External'),
    ]
    allocation_status_choices = (
        ('IQC','IQC'),
        ('Allocated', 'Allocated'),
        ('Decommissioned', 'Decommissioned'),
        ('Free', 'Free'),
        ('Needs Maintainence', 'Needs Maintainence'),
        ('Repair/Replace', 'Repair/Replace'),
    )

    loc_floor_choices = [
            ('1F','1'),
            ('2F','2'),
            ('3F','3'),
            ('4F','4'),
    ]
    # ! COMMON FIELDS 
    iepl_id = models.CharField(max_length=100, unique=True, verbose_name='iepl_id')
    item_name = models.ForeignKey(ItemName, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=512,blank=True)   
    # po_year = models.CharField(max_length=5,blank=True)
    po_year = models.ForeignKey(poYear, on_delete=models.CASCADE, related_name='po_year')
    po_initials = models.ForeignKey(poIni, on_delete=models.CASCADE, related_name='po_initials')
    # po_initials = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='po_initials')
    po_srno = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, null=True, verbose_name="PO Number : Serial Number")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, blank=True, null=True)
    manufacturer_part_no =  models.ForeignKey(ManufacturerPart, on_delete=models.CASCADE, blank=True, null=True)
    to_be_reimbursed = models.BooleanField(default=False,blank=True,null=True)


    project = models.ForeignKey(ProjectMaster, on_delete=models.CASCADE, blank=True, null=True, default='None') ##CONTAINES BOTH ID AND NAME
    allocation_status = models.CharField(choices=allocation_status_choices, max_length=20, default = 'IQC')
    floor_number = models.CharField(choices=loc_floor_choices ,max_length=2, null=True, blank=True, default='1F')
    loc_type = models.CharField(choices =loc_type_choices ,max_length=1, null=True, blank= True, default = 'Q')
    loc_number = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, null=True, default=0)
    location = models.CharField(max_length=64,blank=True,null=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default='None')
    
    comment = models.CharField(max_length=512, blank=True, null=True, validators=[project_status_validator])
    created_on = models.DateTimeField(default=timezone.now, null=True)
    gin_year = models.ForeignKey(poYear, on_delete=models.CASCADE, related_name='gin_year', null=True, blank= True)
    gin_initials = models.ForeignKey(poIni, on_delete=models.CASCADE, related_name='gin_initials', null=True, blank= True)
    gin_srno = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], null=True, blank= True)
    # gin_iqar_no = models.CharField(max_length=64, blank=True, null=True)
    
    modified_on = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name='created_by'
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name='modified_by'
    )

    # ! IT FIELDS 
    service_tag = models.CharField(max_length=64, blank=True, null=True, validators=[service_tag_validator]) # todo uppercase in forms or html
    item_type = models.ForeignKey(Item_type, on_delete=models.CASCADE, blank=True, null=True)
    host_name = models.CharField(max_length=64, default='NA', blank=True, null=True)    
    local_admin = models.CharField(max_length=64, blank=True, null=True) # will do
    rent = models.PositiveIntegerField(default=None, blank=True, null=True)
    cpu_type = models.ForeignKey(CPUTYPE, on_delete=models.CASCADE, blank=True, null=True)
    cpu_speed = models.FloatField(max_length=100, blank=True, null=True, validators=[validate_decimals_cpu_speed])
    display_output = models.CharField(max_length=64, blank=True, null=True, validators=[Disp])
    monitor_manufacturer = models.CharField(max_length=64, blank=True, null=True)
    monitor_make =  models.CharField(max_length=64, blank=True, null=True)
    monitor_size = models.FloatField( blank=True, null=True,validators = [validate_decimals_monitor_size])
    ram = models.ForeignKey(RAMS, on_delete=models.CASCADE, blank=True, null=True)
    # loc_number = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, null=True)
    storage = models.CharField(max_length=64, blank=True, null=True, validators=[storage])
    #storage = models.ForeignKey(STORAGE, on_delete=models.CASCADE, max_length=64, blank=True, null=True, validators=[storage])
    os = models.ForeignKey(OSS, on_delete=models.CASCADE, blank=True, null=True)
    warranty_expiry_date = models.DateField(default=date.today(), blank= True, null= True)
        
    #!HARDWARE FIELDS
    #todo Subsidiary field in common project
    subsidiary = models.ForeignKey(
        SubsidiaryMaster, on_delete=models.CASCADE, blank=True, null=True)
    customer_property = models.BooleanField(default=False,blank=True,null=True)
                               

    # Subsidiary  
    # subsidiary = models.ForeignKey(SubsidiaryMaster, on_delete=models.CASCADE)

    #!EXTRAS
    po_date = models.DateTimeField(default=timezone.now, null=True)    
    model_no = models.CharField(max_length=150, blank=True, null=True)        
    desk_no = models.CharField(max_length=50, blank=True, null=True)    
    asset_code = models.CharField(max_length=100, default='NA', blank=True, null=True)
    cpu = models.FloatField(max_length=100, default=00, blank=True, null=True)    
    monitor_model = models.CharField(max_length=100, default='NA', blank=True, null=True)        
    hdd = models.CharField(max_length=100, default='NA', blank=True, null=True)
    extra_monitor_model = models.CharField(max_length=50, default='NA', blank=True, null=True)
    #!EXTRAS
        

    def __str__(self):
        return self.iepl_id


class Allocation(models.Model):
    """Allocation Details"""
    service_tag = models.ForeignKey(Device, on_delete=models.CASCADE)
    allot_to = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return '{}_{}'.format(self.service_tag, self.allot_to)


class Report(models.Model):
    """Report Details such as Incorrect assignemnet,Free Item,Return To Store."""
    report_action_choices = (
        ('transfer', 'transfer'),
        ('incorrect', 'incorrect'),
        ('return_to_store', 'return_to_store'),
        ('free_item', 'free_item'),
    )
    allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        EmployeeMaster,
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    report_action = models.CharField(choices=report_action_choices, max_length=20)
    created_by = models.ForeignKey(
        User,
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(
        db_index=True,
        null=True,
        auto_now_add=True,
    )

    def __str__(self):
        return '{}_{}'.format(self.report_action, self.employee)


class Service(models.Model):
    """Create Service Report."""
    service_action_choices = (
        ('Release', 'Release'),
        ('Borrow', 'Borrow'),
    )
    service_status_choices = (
        ('Initiated', 'Initiated'),
        ('Completed', 'Completed'),
    )
    service_tag = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    service_action = models.CharField(choices=service_action_choices, max_length=50)
    service_status = models.CharField(choices=service_status_choices, max_length=50, default='Initiated')

    def __str__(self):
        return '{}_{}'.format(self.service_tag, self.employee)


class History_log(models.Model):
    """History Log Report."""
    service_tag = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='--')

    def __str__(self):
        return '{}_{}'.format(self.service_tag, self.employee)


class Logs(models.Model):
    """Transaction Log Report"""
    action_time = models.DateTimeField(
        db_index=True,
        default=timezone.now,
        editable=False,
    )
    """field change"""
    device = models.ForeignKey(
        Device,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    status_choices = (
        ('Free', 'Free'),
        ('Allocated', 'Allocated'),
        ('Decommissioned', 'Decomissioned'),
        ('Edited', 'Edited'),
        ('Added', 'Added'),
        ('Deleted', 'Deleted'),
        ('Transferred', 'Transferred'),
        ('Transfer Request Rejected', 'Transfer Request Rejected'),
        ('Returned To Store', 'Returned To Store')
    )
    status = models.CharField(
        max_length=100,
        db_index=True,
        choices=status_choices,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    allot_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True,
        related_name='allot_to_user'
    )
    details = models.CharField(
        max_length= 200,
        db_index = True,
        null=True,
        blank = True
    )

class DecomissionedItems(models.Model):
    """Used to save soft delete device data, on instance delete from device model, will copy the details of
     that instance to this model, Then remove the record from device model permanently"""
    iepl_id = models.CharField(max_length=10, unique=True, verbose_name='iepl_id')
    service_tag = models.CharField(max_length=100, blank=True, null=True)
    item_type = models.ForeignKey(Item_type, on_delete=models.CASCADE, blank=True, null=True)
    host_name = models.CharField(max_length=100, default='NA', blank=True, null=True)
    po_number = models.CharField(max_length=150, blank=True, null=True)
    po_date = models.DateTimeField(default=timezone.now, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, blank=True, null=True)
    model_no = models.CharField(max_length=150, blank=True, null=True)
    project = models.ForeignKey(ProjectMaster, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    desk_no = models.CharField(max_length=50, blank=True, null=True)
    asset_code = models.CharField(max_length=100, default='NA', blank=True, null=True)
    cpu = models.CharField(max_length=100, default='NA', blank=True, null=True)
    cpu_speed = models.FloatField(max_length=100, blank=True, null=True)
    monitor_model = models.CharField(max_length=100, default='NA', blank=True, null=True)
    os = models.CharField(max_length=100, default='NA', blank=True, null=True)
    ram = models.CharField(max_length=100, default='NA', blank=True, null=True)
    hdd = models.CharField(max_length=100, default='NA', blank=True, null=True)
    extra_monitor_model = models.CharField(max_length=50, default='NA', blank=True, null=True)
    status = models.BooleanField(
        default=False,
        db_index=True,
    )
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    created_by = models.ForeignKey(
        User,
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
