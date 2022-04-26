$(document).ready(function(){
    $("#id_item_name option:selected").text("--Select--");
    $("#id_item_name option:selected").hide();
    $("#id_item_name").children().each(function () {
        if($(this).val() != ""){
            detailsList = $(this).text().split(",");
            if(detailsList[1] == "IT"){
                $(this).addClass("IT");
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
})