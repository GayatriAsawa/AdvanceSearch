$(document).ready(function () {
    $('#free_item_fields').hide();
    $('#allocated_fields').hide();
    $('#hidden_fields').hide();
    $('#form_submit_button').hide();
    $("#monitor_make_text_id *").prop('disabled', true);
    $("#storage_text_id *").prop('disabled', true);
    $("#display_output_text_id *").prop('disabled', true);
    $('#controller').change(function(){

        if($(this).val() == "Free"){
            $('#free_item_fields').hide();
            $('#allocated_fields').show();
            $('#comment_description').html('Comment <span style="color: red">* </span> : (Changes Done in Needs Maintainence)')
        }
        else if($(this).val() == "Allocated"){
            if($('#id_project').val() != "")
            {
                $('#id_comment').attr('required','');
                $('#free_item_fields').show();
                $('#allocated_fields').show();
                $('#comment_description').html('Comment <span style="color: red">* </span> : (Changes Done in Needs Maintainence)')
                $('#id_project').prop('disabled', true);
                $('#id_employee').prop('disabled', true);
            } 
            else
            {
                $('#id_comment').attr('required','');
                $('#free_item_fields').show();
                $('#allocated_fields').show();
                $('#id_project').prop('disabled', false);
                $('#id_employee').prop('disabled', false);
                
            }
        }
        else{
            $('#free_item_fields').hide();
            $('#allocated_fields').hide();
            $('#hidden_fields').hide();
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
function validateMaintainenceForm(){
    if($('#controller').val() == "Allocated"){
        if($('#id_comment').val() == ""){
            alert("Please Enter A Comment");
        }
        else if($('#id_project').val() == ""){
            alert("Please Allocate the Project");
        }
        else if($('#id_employee').val() == ""){
            alert("Please Allocate the object from User");
        }
        else if($('#id_floor_number').val() == "" || $('#id_loc_number').val() == "" || $('#id_loc_type').val() == ""){
            alert("Please Enter All Location Fields");
        }
        else{
            $('#form_submit_button').click();
        }
    }

    else if($('#controller').val() == "Free"){

        if($('#id_floor_number').val() == "" || $('#id_loc_number').val() == "" || $('#id_loc_type').val() == "" ){
            alert("Please Enter All Location Fields");
        }
        else{
            $('#form_submit_button').click();
        }   
    }

    else{
        $('#form_submit_button').click();
    }
}