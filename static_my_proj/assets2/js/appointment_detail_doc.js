

$(document).ready(function(){
  $("#approve").click(function(){
   var approve = $("#approve").text();
   console.log(approve);
   send_appointment_action(approve)
  });

});



$(document).ready(function(){
  $("#decline").click(function(){
   var decline = $("#decline").text();
   console.log(decline);
   send_appointment_action(decline)
  });

});


$(document).ready(function(){
  $("#start").click(function(){
   var start = $("#start").text();
   console.log(start);
   send_appointment_action(start)
  });

});


$(document).ready(function(){
  $("#completed").click(function(){
   var completed = $("#completed").text();
   console.log(completed);
   send_appointment_action(completed)
  });

});


var actionEndpoint = $('#appointment_actions').attr('action');


function send_appointment_action(action){
    console.log(action)
    data = {
        action: action
    }

    $.ajax({
				type: 'POST',
				dataType: "json",
				url: actionEndpoint,
				data,
				timeout: 10000,
				success: function(data) {
					if(data.result == "success"){
						console.log(data.result)
						console.log(data.appointment_detail)
						$('.app_status').text(data.appointment_detail.status)
						$('.app_status').removeClass('bg-danger');
						$('.app_status').addClass('bg-success');

					}
					else if(data.result == "error"){
						alert(data.exception)
						console.log("error")
					}
				},
				error: function(data) {
					console.error("ERROR...", data)
				},
				complete: function(data){
				}
			});



}

