// FORM VARIABLES

var appointmentFormEndpoint = $('#appointment_form').attr('action');

var appointment_type = null;
var doctor = null;
var appointment_date = null;
var appointment_time = null;
var reason = null;
var for_self = "True";
var other_data = null;
var appointment_medium = null;
var appointment_price = null;
var payment_type = null;
var payment_data = null;





// APPOINTMENT TYPE
function setAppointmentType(){
    var header = document.getElementById("ap_type");
    var btns = header.getElementsByClassName("app_type_btn");

    if(appointment_type == "New Problem"){
        $("#new_problem_btn").addClass("app_type_active");
        $("#covid_19_btn").removeClass("app_type_active");
        $("#problem_follow_up_btn").removeClass("app_type_active");
    }

    if(appointment_type == "Covid"){
        $("#new_problem_btn").removeClass("app_type_active");
        $("#covid_19_btn").addClass("app_type_active");
        $("#problem_follow_up_btn").removeClass("app_type_active");
    }

    if(appointment_type == "Problem Follow-up"){
        $("#new_problem_btn").removeClass("app_type_active");
        $("#covid_19_btn").removeClass("app_type_active");
        $("#problem_follow_up_btn").addClass("app_type_active");
    }

    console.log(appointment_type);

}

function setNewProblem(){
    var button = document.getElementById('new_problem').innerHTML;
    appointment_type = button;

    setAppointmentType();
}

function setCovid19(){
    var button = document.getElementById('covid_19').innerHTML;
    appointment_type = "Covid";
    setAppointmentType();
}

function setProblemFollowUp(){
    var button = document.getElementById('problem_follow_up').innerHTML;
    appointment_type = button;
    setAppointmentType();
}


function setDoctor(data){

    //console.log(data);
    var header = document.getElementById("doctor_head");
    var btns = header.getElementsByClassName("doctors");
    var doctor_id = $("#doctor-"+data).attr('id');

    $('.doctors').map(function(i,el) {
        if($(el).attr("id") != "doctor-" + data){
            $(el).removeClass("doc-active");
            $("#doctor-"+data).addClass(' doc-active');
            $(".doc-"+data).toggle();
            //$(".app_time_tab").toggle();
        }
    });

    doctor = data;

}

$(".app_time_tab").hide();


function setDate(data, date){
    appointment_date = date;

    var appointment_date_str = data;

    $('.app-dates').map(function(i,el) {

        $("#"+$(el).attr("id")).addClass('bg-primary text-white');

        if($(el).text() != appointment_date_str){

            $("#"+$(el).attr("id")).removeClass('bg-primary text-white');
            $("#"+$(el).attr("id")).addClass('collapsed');
            $("#"+$(el).attr("id")).attr("aria-expanded", "false");

        }
    });
}


function setTime(data, time){
    appointment_time = time;
    console.log(time);

    var appointment_time_str = data;

    $('.app-times').map(function(i,el) {

        $("#"+$(el).attr("id")).removeClass('btn-secondary');
        $("#"+$(el).attr("id")).addClass('btn-primary');

         if($(el).text() != appointment_time_str){

            $("#"+$(el).attr("id")).removeClass('btn-primary');
            $("#"+$(el).attr("id")).addClass('btn-secondary');
        }
    });
}


function setSelf(){
    for_self = 'True';
}


function setOther(){
    for_self = 'False';
}

function getOtherData(){

    other_data = {
        last_name: $("#other-lastname").val(),
        first_name: $("#other-firstname").val(),
        email: $("#other-email").val(),
        phone: $("#other-phone").val()

    };

}

function setMedium(name, price){
    appointment_medium = name;
    appointment_price = price;
    console.log(name);
    console.log(price);

    $('.app-mediums').map(function(i,el) {
        $("#"+$(el).attr("id")).addClass('app_type_active');

         if($(el).attr('data-value') != appointment_medium){

            $("#"+$(el).attr("id")).removeClass('app_type_active');

        }
    });

    setPrice();
}


function goToSummary() {

    getOtherData();

    $("#sum-app-type").text(appointment_type);
    $("#sum-app-doctor").text(doctor);
    $("#sum-app-date").text(appointment_date);
    $("#sum-app-time").text(appointment_time);
    $("#sum-app-reason").text($("#app-reason").val());

    $("#sum-app-forself").text(for_self);
    $("#sum-app-other-data-fullname").text(other_data['last_name'] + " " + other_data['first_name']);
    $("#sum-app-other-data-email").text(other_data['email']);
    $("#sum-app-other-data-phone").text(other_data['phone']);




}

function setPrice() {
    $(".appointment-fee").text("Ghc " +appointment_price +".00");

}



function setPaymentType(data){
    payment_type = data;


    $('.app-payments').map(function(i,el) {
        $("#"+$(el).attr("id")).addClass('app_type_active');

         if($(el).attr('data-value') != payment_type){

            $("#"+$(el).attr("id")).removeClass('app_type_active');

        }
    });
}



function getPaymentData(){

    payment_data = {
        last_name: $("#payment-lastname").val(),
        first_name: $("#payment-firstname").val(),
        email: $("#payment-email").val(),
        phone: $("#payment-phone").val()
    };

}




var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";

  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
    //document.getElementById("nextBtn").setAttribute('type', 'submit');
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }

  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}


function nextPrev(n) {
 goToSummary();

  var x = document.getElementsByClassName("tab");

  if (n == 1 && !validateForm()) return false;
  x[currentTab].style.display = "none";

  currentTab = currentTab + n;

  if (currentTab >= x.length) {

    //document.getElementById("regForm").submit();
   document.getElementById("nextBtn").setAttribute('type', 'submit');
   submitAppForm();
    return false;
  }

  showTab(currentTab);
}



function validateForm() {
  var valid = true;
  return valid; // return the valid status
}


function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}






function submitAppForm() {



    $("#appointment_form").submit(function(e) {

        //prevent Default functionality
        //e.preventDefault();
            console.log("SUBMIT HERE");

        getOtherData();
        getPaymentData();

        data = {
        appointment_type: appointment_type,
        doctor: doctor,
        appointment_date: appointment_date,
        appointment_time: appointment_time,
        reason: $("#app-reason").val(),
        for_self: for_self,
        other_data: other_data,
        appointment_medium: appointment_medium,
        appointment_price: appointment_price,
        payment_type: payment_type,
        payment_data: payment_data,
        };

        console.log(data);

        var posting = $.post(
            appointmentFormEndpoint,
            data,
        );

       // Put the results in a div
       posting.done(function( data ) {

       console.log(data);

        });


        });




}



