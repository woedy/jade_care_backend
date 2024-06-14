var images = [];


/*
window.onload = function() {



  //Check File API support
  if (window.File && window.FileList && window.FileReader) {
    var filesInput = document.getElementById("files");
    filesInput.addEventListener("change", function(event) {
      var files = event.target.files; //FileList object
      var output = document.getElementById("images_container");
      for (var i = 0; i < files.length; i++) {
        var file = files[i];
        //Only pics
        if (!file.type.match('image'))
          continue;
        var picReader = new FileReader();
        images = [];

        picReader.addEventListener("load", function(event) {
          var picFile = event.target;
          images.push(picFile.result);

        });
        //Read the image
        picReader.readAsDataURL(file);

        getImages();
      }
    });
  } else {
    console.log("Your browser does not support File API");
  }
  //console.log(images);

}
*/


function preview_image()
{
 var total_file=document.getElementById("upload_file").files.length;
 for(var i=0;i<total_file;i++)
 {
  var img = "'" + URL.createObjectURL(event.target.files[i]) + "'";
    $("#images_container").append('<div id="'+ URL.createObjectURL(event.target.files[i])  +'" class="col-md-3 col-sm-3 col-4 col-lg-3 col-xl-2"><div onclick="delete_image('+ img +');" class="product-thumbnail"><img src="'+ URL.createObjectURL(event.target.files[i])  +'" class="img-thumbnail img-fluid" alt=""><span class="product-remove" title="remove"><i id="remove_image" class="bi bi-x-circle-fill"></i></span></div></div>');
 }
}


function delete_image(image_id)
{

    $("#"+ image_id).remove();


 //console.log("#" + image_id)


}



function getImages() {
    for (var i = 0; i < images.length; i++) {
        var image = images[i];
        $("#images_container").append('<div class="col-md-3 col-sm-3 col-4 col-lg-3 col-xl-2"><div class="product-thumbnail"><img src="'+ image  +'" class="img-thumbnail img-fluid" alt=""><span class="product-remove" title="remove"><i id="remove_image" class="bi bi-x-circle-fill"></i></span></div></div>');
    }

}







  $("#article_form").submit(function(e) {


        //e.preventDefault();
        console.log("SUBMIT HERE");




 });
