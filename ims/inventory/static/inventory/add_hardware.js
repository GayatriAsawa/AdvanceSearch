$(document).ready(function(){
    $('#subsidiarycheck').hide();
    let subsidiaryError = true;   
    $("#id_item_name option:selected").text("--Select--");
    $("#id_item_name option:selected").hide();
    $("#id_item_name").children().each(function () {
        if($(this).val() != ""){
            detailsList = $(this).text().split(",");
            if(detailsList[1] == "Hardware"){
                $(this).addClass("Hardware");
            }
            else{
                $(this).addClass("Other");
            }
            $(this).text(detailsList[0]);
        }
    })
    $(".Other").each(function(){
        $(this).hide();
    })

    $('#subsidiary_id').keyup(function () {
        validateSubsidiary();
    });
    function validateSubsidiary() {
        if ($('#id_subsidiary').val() == "")
        {
            $('#subsidiarycheck').show();
            subsidiaryError = false;
            return false;
        } else {
            subsidiaryError = true;
            $('#subsidiarycheck').hide();
        }
    }

    $('#form_submit_button').click(function (){
        validateSubsidiary();
        if (subsidiaryError == true){
            return true;
        } else {
            return false;
        }
    });
})

