$(document).ready(function () {
    $('#free_item_fields').hide();
    $('#needs_maintainence_fields').hide();
    $('#location_fields').hide();
    $('#hidden_fields').hide();
    $('#form_submit_button').hide();
    $("#monitor_make_text_id *").prop('disabled', true);
    $("#storage_text_id *").prop('disabled', true);
    $("#display_output_text_id *").prop('disabled', true);
    $('#controller').change(function(){
        if($(this).val() == "Free"){
            $('#free_item_fields').show();
            $('#needs_maintainence_fields').hide();
            $('#location_fields').show();
            $('#id_project').val("");
            $('#id_employee').val("");
            $('#projectName').val("");
            $('#id_project').prop('disabled', true);
            $('#id_employee').prop('disabled', true);
        }
        else if($(this).val() == "Needs Maintainence"){
            $('#id_comment').attr('required','');
            $('#free_item_fields').hide();
            $('#needs_maintainence_fields').show();
            $('#location_fields').show();
            $('#comment_description').html('Comment <span style="color: red">* </span>: (Maintainance Description)')
        }
        else{
            $('#free_item_fields').hide();
            $('#needs_maintainence_fields').hide();
            $('#hidden_fields').hide();
            $('#location_fields').hide();
        }   
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



function validateAllocatedForm(){
    if($('#controller').val() == "Needs Maintainence"){
        if($('#id_comment').val() == ""){
            alert("Please Enter A Comment");
        }
        else if($('#id_floor_number').val() == "" || $('#id_loc_number').val() == "" || $('#id_loc_type').val() == ""){
            alert("Please Enter All Location Fields");
        }
        else{
            $('#form_submit_button').click();
        }
    }
    else if($('#controller').val() == "Free"){
        if($('#id_project').val() != ""){
            alert("Please Deallocate the Project ");
        }
        else if($('#id_floor_number').val() == "" || $('#id_loc_number').val() == "" || $('#id_loc_type').val() == ""){
            alert("Please Enter All Location Fields");
        }
        else if($('#id_employee').val() !=""){
            alert("Please Deallocate the object from User");
        }
        else{
            $('#form_submit_button').click();
        }
    }
    else{
        $('#form_submit_button').click();
    }
}