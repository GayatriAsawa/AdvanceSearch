$(document).ready(function () {
    $('#free_to_allocated_fields').hide();
    $('#hidden_fields').hide();
    $('#form_submit_button').hide();
    $("#monitor_make_text_id *").prop('disabled', true);
    $("#storage_text_id *").prop('disabled', true);
    $("#display_output_text_id *").prop('disabled', true);
    $('#controller').change(function(){
        if($(this).val() == "Allocated"){
            $('#free_to_allocated_fields').show();
            $('#comment_description').html("Comment :")
        }
        else if($(this).val() == "Decommissioned"){
            $('#free_to_allocated_fields').hide();
            $('#comment_description').html('Comment <span style="color: red">* </span> : (Reason for decommision)')
        }
        else if($(this).val() == "Needs Maintainence"){
            $('#free_to_allocated_fields').hide();
            $('#comment_description').html('Comment <span style="color: red">* </span>: (Maintainance Description)')
        }
        else{
            $('#free_to_allocated_fields').hide();
            $('#comment_description').html("Comment :")
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
    $('#id_employee').val("");
    $('#id_project').val("");
    $('#projectName').val("");
}
function validateFreeForm(){
    if($('#controller').val() == "Allocated"){
        if($('#id_employee').val() == ""){
            alert("Please Choose a User For Allocation !")
        }
        else if($('#id_project').val() == ""){
            alert("Please Choose A Project No")
        }
        else if($('#id_floor_number').val() == "" || $('#id_loc_type').val() == "" || $('#id_loc_number').val() == ""){
            alert("Please Enter All Location Fields");
        }
        else{
            $('#form_submit_button').click();
        }
    }
    else if($('#controller').val() == "Decommissioned"){
        if($('#id_floor_number').val() == "" || $('#id_loc_type').val() == "" || $('#id_loc_number').val() == ""){
            alert("Please Enter All Location Fields");
        }
        else if($('#id_comment').val() == ""){
            alert("Please Enter A Comment");
        }
        else{
            $('#form_submit_button').click();
        }
    }
    else if($('#controller').val() == "Needs Maintainence"){
        if($('#id_floor_number').val() == "" || $('#id_loc_type').val() == "" || $('#id_loc_number').val() == ""){
            alert("Please Enter All Location Fields");
        }
        else if($('#id_comment').val() == ""){
            alert("Please Enter A Comment");
        }
        else{
            $('#form_submit_button').click();
        }
    }
    else{
        $('#form_submit_button').click();
    }
}