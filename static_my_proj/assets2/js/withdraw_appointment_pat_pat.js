$(document).ready(function(){
  $("#withdraw").click(function(){
   var withdraw = $("#withdraw").text();
   console.log(withdraw);
   send_appointment_action(withdraw)
  });

  $("#contact_doc").click(function(){
   var contact_doc = $("#contact_doc").text();
   console.log(contact_doc);
   send_appointment_action(contact_doc)


  });

  $("#view_convo").click(function(){
    var view_convo= $("#view_convo").text();
    console.log(view_convo);
    send_appointment_action(view_convo)

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


