var user_id_input = $('#user_id').attr('data-value');
var room_id_input = $('#room_id').attr('data-value');


var loc = window.location;
var wsStart = 'ws://';

  if(loc.protocol == 'https:') {
    wsStart = 'wss://';
   }

 var endPoint = wsStart + loc.host + "/appointments/appointment_text_message_page/";
 console.log(endPoint);


 webSocket = new WebSocket(endPoint);



 webSocket.addEventListener('open', (e) => {
        console.log('Connection Opened');

        webSocket.send(JSON.stringify({
			"command": "join",
			"room": room_id_input,
			"user_id": user_id_input,
			"page_number": 1

		}));
  });

webSocket.addEventListener('message', webSocketOnMessage);

webSocket.addEventListener('close', (e) => {
        console.log('Connection Closed');
        });

webSocket.addEventListener('error', (e) => {
    console.log('Connection Error');
});




function webSocketOnMessage(event) {
    var parseData = JSON.parse(event.data);
    var room_messages = parseData.messages.reverse();

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
                           message = $('.chat-messages').append('<div class="chat-message-left pb-4"><div><img src="'+ user_photo  +'" class="rounded-circle mr-1" alt="Sharon Lessman" width="40" height="40"><div class="text-muted small text-nowrap mt-2">' + new_time_tostring + '</div></div><div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3"><div class="font-weight-bold mb-1"><strong>' + user_last_name + ' ' + user_first_name + '</strong></div>' + user_message + '</div></div>');


                        }else if(message_user_id == user_id_input) {

                           message = $('.chat-messages').append('<div class="chat-message-right pb-4"><div><img src="'+ user_photo  +'" class="rounded-circle mr-1" alt="Sharon Lessman" width="40" height="40"><div class="text-muted small text-nowrap mt-2">' + new_time_tostring + '</div></div><div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3"><div class="font-weight-bold mb-1"><strong>' + user_last_name + ' ' + user_first_name + '</strong></div>' + user_message + '</div></div>');

                        }

                        var d = $('.chat-messages');
                        d.scrollTop(d.prop("scrollHeight"));

                        });

    }
    else  if(room_messages?.length == 0) {
        $('.chat-messages').append('<div class="chat-message-left pb-4"><div><div class="text-muted small text-nowrap mt-2"></div></div><div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3"><div class="font-weight-bold mb-1">No Messages</div>You have no conversation with the current user.</div></div>');

    }



}



  $("#chat_message").submit(function(e) {

        //prevent Default functionality
        e.preventDefault();
        console.log("SUBMIT HERE");
        console.log(room_id_input);


      webSocket.send(JSON.stringify({
			"command": "send",
			"message": $('#the_message').val(),
			"room": room_id_input,
			"user_id": user_id_input,
			"files": []

		}));
		$('#the_message').val("");


 });

