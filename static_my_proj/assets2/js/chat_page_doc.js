console.log("YOOOO")


var actionEndpoint = $('#chat_users_form').attr('action');

var user_id_input = $('#user_id').attr('data-value');



function get_chat_users(){

    data = {
        user_id: user_id_input
    }

    $.ajax({
				type: 'POST',
				dataType: "json",
				url: actionEndpoint,
				timeout: 10000,
				data,
				success: function(data) {
				//console.log(data)
					if(data.result == "success"){
						console.log(data.result)
					    var room_list = data.rooms
						//console.log(room_list)
						console.log(room_list)

                        room_list.forEach(function (element, index, array){
                        console.log("ROOM: " + room_list[index]);

                        var room_id = room_list[index].id


                        var user1_id = room_list[index].user1.id
                        var user1_last_name = room_list[index].user1.last_name
                        var user1_first_name = room_list[index].user1.first_name
                        var user1_full_name = "'" + user1_last_name + ' '+ user1_first_name + "'";
                        var user1photo = room_list[index].user1.personal_info.photo;
                        var new_user1photo = "'" + room_list[index].user1.personal_info.photo + "'";

                        var user2_id = room_list[index].user2.id
                        var user2_last_name = room_list[index].user2.last_name
                        var user2_first_name = room_list[index].user2.first_name
                        var user2_full_name = "'" + user2_last_name + ' '+ user2_first_name + "'";
                        var user2photo = room_list[index].user2.personal_info.photo;
                        var new_user2photo = "'" + room_list[index].user2.personal_info.photo + "'";

                        console.log(user1_id)
                        console.log(user2_id)

                        if(user1_id != user_id_input) {
                            console.log('HE IS CURRENT')


                            user_list = $('.chat_users').append('<a onclick="get_user_messages(' + user1_full_name + ',' + room_id + ',' + new_user1photo + ',' +')" href="#" id="user_' + user1_id + '" data-value="' + user1_id + '" class="list-group-item list-group-item-action border-0"><div class="badge bg-success float-right">0</div><div class="d-flex align-items-start"><img src="'+ user1photo  +'" class="rounded-circle mr-1" alt="Vanessa Tucker" width="40" height="40"><div class="flex-grow-1 ml-3">' + user1_last_name + ' ' + user1_first_name + '<div class="small"><span class="fas fa-circle chat-online"></span> Online</div></div></div></a>');

                        } else if (user2_id != user_id_input) {

                             user_list = $('.chat_users').append('<a onclick="get_user_messages(' + user2_full_name + ',' + room_id + ',' + new_user2photo + ',' +')"  href="#" id="user_' + user2_id + '" data-value="' + user2_id + '" class="list-group-item list-group-item-action border-0"><div class="badge bg-success float-right">0</div><div class="d-flex align-items-start"><img src="'+ user2photo  +'" class="rounded-circle mr-1" alt="Vanessa Tucker" width="40" height="40"><div class="flex-grow-1 ml-3">' + user2_last_name + ' ' + user2_first_name  + '<div class="small"><span class="fas fa-circle chat-online"></span> Online</div></div></div></a>')
                        }
                        });

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

get_chat_users();





