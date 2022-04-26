from typing import DefaultDict
from django.http.response import HttpResponse
from .modules import *

logger = logging.getLogger('logs')  # Instantiating logger.

@login_required(login_url=base.LOGIN_URL)
def add_device(request, id):
    """Add Device page for Admin and Super USer."""
    data = defaultdict()
    data['content_template'] = 'inventory/add_item.html'
    if id == 2:
        data['content_template'] = 'inventory/add_hardware.html'
    elif id == 3:
        data['content_template'] = 'inventory/add_admin.html'
    data['user'] = request.user
    data["device_form"] = DeviceForm()
    data["hardwareform"] = DeviceForm()
    data["adminform"] = DeviceForm()
    data['it'] = 0
    data['validError'] = 'First'
    countofentries = 0
    if request.POST:
        data['it'] = 1
        uniq_id = "iepl00001"
        if Device.objects.exists():
            id1 = Device.objects.latest('id')
            """Here auto increment iepl id by 1"""
            if (id1.pk+1)/10000 >= 1:
                uniq_id = "iepl" + str(id1.pk + 1)
            elif (id1.pk+1)/1000 >= 1:
                uniq_id = "iepl0" + str(id1.pk + 1)
            elif (id1.pk+1)/100 >= 1:
                uniq_id = "iepl00" + str(id1.pk + 1)
            elif (id1.pk+1)/10 >= 1:
                uniq_id = "iepl000" + str(id1.pk + 1)
            else:
                uniq_id = "iepl0000" + str(id1.pk + 1)
            countofentries = id1.pk + 1
            
        device_form = DeviceForm(request.POST)
        
        if device_form.is_valid():
            
            mulSelect = request.POST.getlist('multiple_select')
            mulSelectDisp = request.POST.getlist('multiple_select_disp')            
            ins = device_form.save(commit=False)
            if ins:
                # To add IT specific items
                if id == 1:
                    
                    storage_number = int(request.POST.get('total_chq'))
                    ins.storage = ""
                    if storage_number>1:
                        for i in range(0,storage_number-1):
                            ins.storage += str(request.POST.get('newtype_%i'%i)) +"-" + str(request.POST.get('newmem_%i'%i)) + "|"
                        ins.storage += str(request.POST.get('newtype_%i'%storage_number)) +"-" + str(request.POST.get('newmem_%i'%storage_number)) 
                    else:
                        ins.storage = str(request.POST.get('newtype_0')) +"-" + str(request.POST.get('newmem_0'))
                    
                    ins.monitor_make = ins.monitor_manufacturer + "|"
                    for i in range(0, len(mulSelect)-1):
                        ins.monitor_make += mulSelect[i] + "|"
                    ins.monitor_make += mulSelect[-1]

                    ins.display_output = ""
                    for i in range(0, len(mulSelectDisp)-1):                        
                        ins.display_output += mulSelectDisp[i] + "|"
                    ins.display_output += mulSelectDisp[-1]

                ins.iepl_id = uniq_id
                ins.location = str(ins.floor_number) + "-" + ins.loc_type + str(ins.loc_number)                
                ins.save()
                device_form.save()

                if(id == 1):
                    data["device_form"] = ins
                elif(id == 2):
                    data['content_template'] = 'inventory/add_hardware.html'
                    data["hardwareform"] = ins
                elif(id == 3):
                    data['content_template'] = 'inventory/add_admin.html'
                    data["adminform"] = ins
                data['validError'] = 'NoError'
                messages.success(request, 'Device added successfully..!!!')
                """Here set Transaction log Added with user id"""
                set_transaction_logs(request, ins.id, "Added", "Allocation Status: None->IQC")
                logger.debug(
                    'Device and Transaction log Added with user id - %s ' % request.user)
        else:
            if(id == 1):
                    data["device_form"] = device_form
            elif(id == 2):
                data["hardwareform"] = device_form
            elif(id == 3):
                data["adminform"] = device_form
            
            mulSelectDisp = request.POST.getlist('multiple_select_disp') 
            
            for field in device_form.errors:
                device_form[field].field.widget.attrs['class'] += " error"

            another_errors = {device_form.fields[field].label: error  for field, error in device_form.errors.items()}
            #Special Addition
            another_errors[""] = "Enter Display Output , Monitor Make , Storage Values Again"
            data['err'] = another_errors.items()
            logger.debug(
                'Device and Transaction log addition failed with user id - %s ' % request.user)
            data['validError'] = 'error'
            messages.error(request, another_errors)
    return render(request, "inventory/dashboard.html", data)


@login_required(login_url=base.LOGIN_URL)
def modify_item(request):
    """Modify item page for Admin and Super User"""
    data = defaultdict()
    data['content_template'] = 'inventory/manage_items.html'
    data['heading'] = 'Modify Items'
    data['hide_edit'] = False
    data["form_error"] = False
    if request.POST:  
        data['content_template'] = 'inventory/edit_item.html'           
        device = Device.objects.get(pk=(request.POST.get('curr_id')))
        device_form = DeviceForm(request.POST, instance=device)

        alloc_status = request.POST.get("allocation_status", "")
        if alloc_status == "Decommissioned":
            # if decomission_delete(request, device.id, False):
            device.delete()
        elif alloc_status == "Free":        
            """Here set Transaction log Free with user id"""
            set_transaction_logs(request, device.id, "Free")
        else:
            
            if device_form.is_valid():
                messages.success(request, 'Device edited successfully..!!!')
                device_form.save()
                if request.POST["employee"] != "" and alloc_status == "Allocated":
                    employee = User.objects.get(
                        pk=int(request.POST["employee"]))
                    ins = Allocation(
                        service_tag=device,
                        allot_to=employee
                    )
                    ins.save()
                    """Here set Transaction log Allocated to user with device id"""
                    set_transaction_logs(
                        request, device.id, "Allocated", "State doesn't found", employee.id)
                    """Here set Transaction log edited with user id"""
                logger.debug(
                    'Device and Transaction log modified with user id - %s ' % request.user)
                set_transaction_logs(request, device.id, "Edited","State doesn't found")
            else:
                data["device_form"] = device_form
                data["form_error"] = True
                data["project_name"] = device_form.cleaned_data.get('project').name
                for field in device_form.errors:
                    key = device_form.fields[field].label
                    device_form[field].field.widget.attrs['class'] += " error"+key
                    # key = device_form.fields[field].label

                data["items_list"] = Device.objects.all()
                data["show_form"] = True
                data['validError'] = 'error'
                messages.error(request, device_form.errors)
                logger.debug(
                    'Device and Transaction log modification failed error - %s , ' % device_form.errors)
                return render(request, "inventory/dashboard.html", data)
        return render(request, "inventory/dashboard.html", data)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        data["items_list"] = (Device.objects.all())
        data["device_form"] = DeviceForm()
        data["show_form"] = True
    return render(request, "inventory/dashboard.html", data)


@login_required(login_url=base.LOGIN_URL)
def delete_device(request, device_id):
    """Delete/Decomission device feature for Admin and SuperUser"""
    device = Device.objects.get(pk=device_id)
    device.delete()
    logger.debug('Device delete successful by user - %s ' % request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url=base.LOGIN_URL)
def device_details(request, device_id):
    """Device Detail/Information feature for all users"""
    data = defaultdict()
    data['content_template'] = 'inventory/item_details.html'
    data["ids"] = Device.objects.get(pk=device_id)
    data["allocation_items"] = Allocation.objects.filter(
        service_tag=data["ids"]).order_by("-pk")
    if data['allocation_items'].count() > 0:
        data['allocation_items'] = data['allocation_items'][0]
    else:
        data['allocation_items'] = dict()
    logger.debug('Device details visited for device-id - %s ' % device_id)
    return render(request, "inventory/dashboard.html", data)


@login_required(login_url=base.LOGIN_URL)
def search_devices(request):
    """ The function for 'Search Items' feature implementation."""
    data = defaultdict()
    data['content_template'] = 'inventory/manage_items.html'
    data['heading'] = 'Search Items'
    data['hide_edit'] = True
    data["items_list"] = Device.objects.all().order_by('created_on').reverse()
    data["device_form"] = DeviceForm()
    data["show_form"] = True
    logger.debug('Device search visited by user id - %s ' % request.user)
    return render(request, "inventory/dashboard.html", data)

@login_required(login_url=base.LOGIN_URL)    
def edit_item(request,id):
    temp = Device.objects.filter(id = id)
    temp1 = DeviceForm(instance=temp[0])
    data = DefaultDict()
    data = DefaultDict()
    data['curr_id']= id
    data['curr_id_iepl']= temp[0].iepl_id
    data['device_form'] = temp1
    data['content_template'] = 'inventory/edit_item.html'
    data['validError'] = 'First'
    data['state'] = temp[0].allocation_status
    return render(request, 'inventory/dashboard.html',data)

@login_required(login_url=base.LOGIN_URL)
def item_modification(request):
    if request.POST:
        id = request.POST.get('curr_id')
        device = Device.objects.get(pk=(request.POST.get('curr_id')))
        device_form = DeviceForm(request.POST, instance=device)

        #before transaction attributes
        init_transaction_comment = device.comment
        init_transaction_locfloor = device.floor_number
        init_transaction_loctype = device.loc_type
        init_transaction_locnumber = device.loc_number
        init_transaction_user = device.employee
        init_transaction_project = device.project
        init_transaction_storage = device.storage
        init_transaction_monitor_make = device.monitor_make
        init_transaction_display_output = device.display_output

        if device_form.is_valid():
            currentState = device.allocation_status
            targetState = request.POST.get('controller')

            # after transaction attributes
            changed_transaction_comment = device.comment
            changed_transaction_locfloor = device.floor_number
            changed_transaction_loctype = device.loc_type
            changed_transaction_locnumber = device.loc_number
            changed_transaction_user = device.employee
            changed_transaction_project = device.project

            device.location = str(changed_transaction_locfloor) +"-"+ str(changed_transaction_loctype) + str(changed_transaction_locnumber)
            
            if device.item_name.item_category== 'IT':
                storage_number = int(request.POST.get('total_chq'))
                device.storage = ""
                if storage_number>1:
                    for i in range(0,storage_number-1):
                        device.storage += str(request.POST.get('newtype_%i'%i)) +"-" + str(request.POST.get('newmem_%i'%i)) + "|"
                    device.storage += str(request.POST.get('newtype_%i'%storage_number)) +"-" + str(request.POST.get('newmem_%i'%storage_number)) 
                else:
                    if str(request.POST.get('newtype_0')) == "Storage Type":
                        device.storage = init_transaction_storage
                        #nothing to change
                    else:
                        device.storage = str(request.POST.get('newtype_0')) +"-" + str(request.POST.get('newmem_0'))
                
                mulSelect = request.POST.getlist('multiple_select')
                if len(mulSelect)>0: 
                    device.monitor_make = device.monitor_manufacturer + "|"
                    for i in range(0, len(mulSelect)-1):
                        device.monitor_make += mulSelect[i] + "|"
                    device.monitor_make += mulSelect[-1]
                else:
                    device.monitor_make = init_transaction_monitor_make

                mulSelectDisp = request.POST.getlist('multiple_select_disp')
                if len(mulSelectDisp)>0:
                    device.display_output = ""
                    for i in range(0, len(mulSelectDisp)-1):                        
                        device.display_output += mulSelectDisp[i] + "|"
                    device.display_output += mulSelectDisp[-1]
                else:
                    device.display_output = init_transaction_display_output

            if targetState != '-':
                #iqc_pass
                if currentState == "IQC" and targetState == "Free":
                    device.allocation_status = targetState
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState + "\nLocation: "+ str(init_transaction_locfloor) +"-"+ str(init_transaction_loctype) + "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)
                    set_transaction_logs(request, device.id, "Edited", transaction_details)

                #iqc_fail
                elif currentState == "IQC" and targetState == "Repair/Replace":
                    device.allocation_status = targetState
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState +  "\nComment: "+ str(init_transaction_comment) + "->" + str(changed_transaction_comment)
                    set_transaction_logs(request, device.id, "Edited", transaction_details)

                #vendor_work_done
                elif currentState == "Repair/Replace" and targetState == "IQC":
                    device.allocation_status = targetState
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState +  "\nComment: "+ init_transaction_comment + "->" + changed_transaction_comment
                    set_transaction_logs(request, device.id, "Edited", transaction_details)

                #vendor_unable_to_repair
                elif currentState == "Repair/Replace" and targetState == "Decommissioned":
                    device.allocation_status = targetState
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState + "\nLocation: "+ init_transaction_locfloor +"-"+ init_transaction_loctype + str(init_transaction_locnumber)+ "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)+  "\nComment: "+ init_transaction_comment + "->" + changed_transaction_comment
                    set_transaction_logs(request, device.id, "Edited", transaction_details)

                #allocate_to_user
                elif currentState == "Free" and targetState == "Allocated":
                    device.allocation_status = targetState
                    employee = User.objects.get(
                        pk=int(request.POST["employee"]))
                    ins = Allocation(
                        service_tag=device,
                        allot_to=employee
                    )
                    ins.save()
                    """Here set Transaction log Allocated to user with device id"""
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState + "\nUser: " + str(init_transaction_user) + "->" + str(changed_transaction_user)+ "\nProject: " + str(init_transaction_project) + "->" + str(changed_transaction_project) + "\nLocation: "+ init_transaction_locfloor +"-"+ init_transaction_loctype + str(init_transaction_locnumber)+ "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)+  "\nComment: None->" + changed_transaction_comment
                    set_transaction_logs(request, device.id, "Edited", transaction_details ,employee.id)

                #decommission_item
                elif currentState == "Free" and targetState == "Decommissioned":
                    device.allocation_status = targetState
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState + "\nLocation: "+ init_transaction_locfloor +"-"+ init_transaction_loctype + str(init_transaction_locnumber)+ "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)+  "\nComment: "+ init_transaction_comment + "->" + changed_transaction_comment
                    set_transaction_logs(request, device.id, "Edited", transaction_details)

                #raise_service_request
                elif currentState == "Free" and targetState == "Needs Maintainence":
                    device.allocation_status = targetState 
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState + "\nLocation: "+ init_transaction_locfloor +"-"+ init_transaction_loctype + str(init_transaction_locnumber)+ "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)+  "\nComment: "+ init_transaction_comment + "->" + changed_transaction_comment
                    set_transaction_logs(request, device.id, "Edited", transaction_details) 

                #free_item
                elif currentState == "Allocated" and targetState =="Free":
                    device.allocation_status = targetState
                    device.project = None
                    device.employee = None
                    allocated_device_obj = Allocation.objects.filter(service_tag = device)
                    allocated_device_obj.delete()
                    
                    changed_transaction_user = device.employee
                    changed_transaction_project = device.project
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState + "\nUser: " + str(init_transaction_user) + "->" + str(changed_transaction_user)+ "\nProject: " + str(init_transaction_project) + "->" + str(changed_transaction_project)+ "\nLocation: "+ init_transaction_locfloor +"-"+ init_transaction_loctype + str(init_transaction_locnumber)+ "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)
                    set_transaction_logs(request, device.id, "Edited", transaction_details)

                #raise_service_request
                elif currentState == "Allocated" and targetState == "Needs Maintainence":
                    device.allocation_status = targetState
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState + "\nLocation: "+ init_transaction_locfloor +"-"+ init_transaction_loctype + str(init_transaction_locnumber)+ "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)+  "\nComment: "+ init_transaction_comment + "->" + changed_transaction_comment
                    set_transaction_logs(request, device.id, "Edited", transaction_details)

                #solve_service_request
                elif currentState == "Needs Maintainence"  and targetState == "Allocated":
                    device.allocation_status = targetState
                    
                    check_allocation_obj = Allocation.objects.filter(service_tag = device)

                    if not check_allocation_obj.exists():
                        employee = User.objects.get(
                        pk=int(request.POST["employee"]))

                        allocated_device_obj = Allocation(
                            service_tag=device,
                            allot_to=employee
                        )
                        allocated_device_obj.save()
                        """Here set Transaction log Allocated to user with device id"""
                        transaction_details = "Allocation Status: " + currentState + "->" +targetState + "\nUser:"+ str(init_transaction_user) + "->" + str(changed_transaction_user) + "\nProject: " + str(init_transaction_project) + "->" + str(changed_transaction_project) + "\nLocation: "+ init_transaction_locfloor +"-"+ init_transaction_loctype + str(init_transaction_locnumber)+ "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)+  "\nComment: "+ init_transaction_comment + "->" + changed_transaction_comment  
                        set_transaction_logs(request, device.id, "Edited", transaction_details , employee.id)
                    else:
                        transaction_details = "Allocation Status: "+currentState + "->" +targetState + "\nLocation: "+ init_transaction_locfloor +"-"+ init_transaction_loctype + str(init_transaction_locnumber)+ "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)+  "\nComment: "+ init_transaction_comment + "->" + changed_transaction_comment 
                        set_transaction_logs(request, device.id, "Edited", transaction_details)

                    

                elif currentState == "Needs Maintainence" and targetState == "Free":
                    device.allocation_status = targetState
                    device.project = None
                    device.employee = None
                    allocated_device_obj = Allocation.objects.filter(service_tag = device)
                    allocated_device_obj.delete()
                    transaction_details = "Allocation Status: "+currentState + "->" +targetState + "\nLocation: "+ init_transaction_locfloor +"-"+ init_transaction_loctype + str(init_transaction_locnumber)+ "->" + changed_transaction_locfloor +"-"+ changed_transaction_loctype + str(changed_transaction_locnumber)+  "\nComment: "+ init_transaction_comment + "->" + changed_transaction_comment
                    set_transaction_logs(request, device.id, "Edited", transaction_details)

                   
                else:
                    print("Should Not Go In Here For Now")
            device_form.save()
            
        else:
            for field in device_form.errors:
                key = device_form.fields[field].label
                device_form[field].field.widget.attrs['class'] += " error"+key
            messages.error(request, device_form.errors)
            logger.debug(
                'Device and Transaction log modification failed error - %s , ' % device_form.errors)
            return redirect('/edit_item/'+id)
    return redirect('/modify_item')

def advance_search(request):
    data = defaultdict()
    data['content_template'] = 'inventory/advance_search.html'
    data['heading'] = 'Search Items'
    data['hide_edit'] = True
    data["items_list"] = Device.objects.all().order_by('created_on').reverse()
    data["device_form"] = DeviceForm()
    data["show_form"] = True
    logger.debug('Device search visited by user id - %s ' % request.user)
    return render(request, "inventory/dashboard.html", data)