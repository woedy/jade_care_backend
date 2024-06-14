


var messageEndpoint = $('#chat_messages_form').attr('action');
var user_id_input = $('#user_id').attr('data-value');

function get_user_messages(full_name, room_id, photo) {
    //console.log(full_name)
    console.log(full_name)
    console.log(room_id)

    data = {
        user_id: 'idddddd',
        room_id: room_id,
    }

     $.ajax({
				type: 'POST',
				dataType: "json",
				url: messageEndpoint,
				timeout: 10000,
				data,
				success: function(data) {
				//console.log(data)
					if(data.result == "success"){
						console.log(data.result)
						console.log(data.messages)

						var room_messages = data.messages
						//console.log(room_messages)

						displayMessages(room_messages);
						$('#message_head_name').text(full_name);
						$('#message_head_image').attr('src', photo);
						$('.chat-messages').attr('id', room_id);



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

function displayMessages(room_messages) {

    console.log(room_messages);
    $('.chat-messages').empty();


    if(room_messages?.length != 0){
        room_messages.forEach(function (element, index, array){

						var message_user_id = room_messages[index].user.id
						var user_last_name = room_messages[index].user.last_name
						var user_first_name = room_messages[index].user.first_name
						var user_photo = room_messages[index].user.personal_info.photo
						var user_message = room_messages[index].message
						var timestamp = room_messages[index].timestamp
						var new_timestamp = new Date(timestamp);
						var new_time_tostring  = new_timestamp.toLocaleTimeString();

                        console.log("LastName: " + user_last_name);
                        console.log("FirstName: " + user_first_name);
                        console.log("MESSAGES: " + user_message);
                        console.log("MESSAGES: " + new_timestamp.toLocaleTimeString());

                        if(message_user_id != user_id_input) {
                           message = $('.chat-messages').append('<div class="chat-message-left pb-4"><div><img src="'+ user_photo  +'" class="rounded-circle mr-1" alt="Sharon Lessman" width="40" height="40"><div class="text-muted small text-nowrap mt-2">' + new_time_tostring + '</div></div><div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3"><div class="font-weight-bold mb-1">' + user_last_name + ' ' + user_first_name + '</div>' + user_message + '</div></div>')
                        }else if(message_user_id == user_id_input) {

                           message = $('.chat-messages').append('<div class="chat-message-right pb-4"><div><img src="'+ user_photo  +'" class="rounded-circle mr-1" alt="Sharon Lessman" width="40" height="40"><div class="text-muted small text-nowrap mt-2">' + new_time_tostring + '</div></div><div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3"><div class="font-weight-bold mb-1">' + user_last_name + ' ' + user_first_name + '</div>' + user_message + '</div></div>')
                        }



                        });
    }
    else  if(room_messages?.length == 0) {
        $('.chat-messages').append('<div class="chat-message-left pb-4"><div><div class="text-muted small text-nowrap mt-2"></div></div><div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3"><div class="font-weight-bold mb-1">No Messages</div>You have no conversation with the current user.</div></div>');
    }

    var d2 = $('.chat-messages');
    d2.scrollTop(d2.prop("scrollHeight"));



}





