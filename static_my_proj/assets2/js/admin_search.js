

var actionEndpoint = $('#search_form').attr('action');

function searchFunction() {
  var x = document.getElementById("search");

  var q = $('#search').val();

  data = {
    q: q
  }


  $.ajax({
				type: 'POST',
				dataType: "json",
				url: actionEndpoint,
				data,
				timeout: 10000,
				success: function(data) {
					if(data.response == "Successful"){
						console.log(data.data)

					}
					else if(data.response == "Error"){
						//alert(data.exception)
						console.log("error")
					}
				},
				error: function(data) {
					console.error("ERROR...", data)
				},
				complete: function(data){
				}
			});

  console.log("YOOOOOOOOO")
  console.log(data)


}