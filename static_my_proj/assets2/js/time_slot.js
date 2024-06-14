$(".hide").hide();


$(document).ready(function() {
    $(".add-more").click(function(){
    var html = $(".copy").html();
    $(".after-add-more").after(html);
    });

    $("body").on("click",".remove",function(){
        $(this).parents(".control-group").remove();
    });
});

var appTimeFormEndpoint = $('#app_time_form').attr('action');

$(function() {
    //hang on event of form with id=myform
    $("#app_time_form").submit(function(e) {

        //prevent Default functionality
        //e.preventDefault();

        var serializedData = $(this).serialize();

        var myForm = document.getElementById('app_time_form');
         var formData = new FormData(myForm);
           console.log(formData.get('date'));
           console.log(formData.get('time[]'));



        console.log("doneeee");
        console.log(serializedData);


        var posting = $.post(
            appTimeFormEndpoint,
            serializedData,
        );

        });
});

















