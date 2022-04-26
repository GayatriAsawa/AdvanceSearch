$(document).ready(function () {
    $('#repair_to_decommissioned_fields').hide();
    $('#hidden_fields').hide();
    $('#form_submit_button').hide();
    $("#id_comment").prop('disabled', true);
    $("#monitor_make_text_id *").prop('disabled', true);
    $("#storage_text_id *").prop('disabled', true);
    $("#display_output_text_id *").prop('disabled', true);
    $('#controller').change(function(){
        if($(this).val() == "IQC"){
            $("#id_comment").prop('disabled', false);
            //$('#comment_description').text("Comment : (Vendor's work)")
            $('#comment_description').html('Comment <span style="color: red">* </span> : (Vendor\'s work)')
            $('#repair_to_decommissioned_fields').hide();
        }
        else if($(this).val() == "Decommissioned"){
            $("#id_comment").prop('disabled', false);
            $('#comment_description').html('Comment <span style="color: red">* </span> : (Reason for decommision)')
            $('#repair_to_decommissioned_fields').show();
        }
        else{
            $("#id_comment").prop('disabled', true);
            $('#comment_description').html('Comment <span style="color: red">* </span> : ')
            $('#repair_to_decommissioned_fields').hide();
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
    $('#id_floor_number').val("");
    $('#id_loc_type').val("");
    $('#id_loc_number').val("");
}
function validateRepairForm(){
    if($('#controller').val() == "IQC"){
        if($('#id_comment').val() == ""){
            alert("Please Enter A Comment");
        }
        else{
            $('#form_submit_button').click();
        }
    }
    else if($('#controller').val() == "Decommissioned"){
        if($('#id_comment').val() == ""){
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