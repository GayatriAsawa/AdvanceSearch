$(document).ready(function () {
    $('#iqc_pass_fields').hide();
    $('#iqc_fail_fields').hide();
    $('#hidden_fields').hide();
    $('#form_submit_button').hide();
    $("#monitor_make_text_id *").prop('disabled', true);
    $("#storage_text_id *").prop('disabled', true);
    $("#display_output_text_id *").prop('disabled', true);
    $('#controller').change(function(){
        if($(this).val() == "Free"){
            $('#iqc_pass_fields').show();
            $('#iqc_fail_fields').hide();
        }
        else if($(this).val() == "Repair/Replace"){
            $('#id_comment').attr('required','');
            $('#iqc_pass_fields').hide();
            $('#iqc_fail_fields').show();
        }
        else{
            $('#iqc_pass_fields').hide();
            $('#iqc_fail_fields').hide();
            $('#hidden_fields').hide();
        }
        resetEnteredValues();
    })
    
    //Logic for filtering item names
    var currentItemType =  $("#id_item_name option:selected").text().split(",")[1];
    $("#id_item_name").children().each(function () {
        if($(this).val() != ""){
            detailsList = $(this).text().split(",");
            if(detailsList[1] == currentItemType){
                $(this).addClass("Current");
            }
            else{
                $(this).addClass("Other");
            }
            $(this).text(detailsList[0]);
        }
        else{
            $(this).hide();
        }
    })
    $(".Other").each(function(){
        $(this).hide();
    })
});
function resetEnteredValues(){
    $('#id_gin_year').val("");
    $('#id_gin_initials').val("");
    $('#id_gin_srno').val("");
    $('#id_floor_number').val("");
    $('#id_loc_type').val("");
    $('#id_loc_number').val("");
    $('#id_host_name').val("");
    $('#id_local_admin').val("");
    //$('#id_comment').val("");
}
function validateIQCForm(){
    if($('#controller').val() == "Repair/Replace"){
        if($('#id_comment').val() == ""){
            alert("Please Enter A Comment");
        }
        else{
            $('#form_submit_button').click();
        }
    }
    else if($('#controller').val() == "Free"){
        if($('#id_gin_year').val() == "" || $('#id_gin_initials').val() == "" || $('#id_gin_srno').val() == ""){
            alert("Please Enter All GIN Number Fields");
        }
        else if($('#id_floor_number').val() == "" || $('#id_loc_type').val() == "" || $('#id_loc_number').val() == ""){
            alert("Please Enter All Location Fields");
        }
        else if($('#id_host_name').val() == ""){
            alert("Please Fill Out Host Name");
        }
        else{
            $('#form_submit_button').click();
        }
    }
    else{
        $('#form_submit_button').click();
    }
}