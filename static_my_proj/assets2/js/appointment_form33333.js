// FORM VARIABLES

var appointmentFormEndpoint = $('#appointment_form').attr('action');

var appointment_type;
var doctor;
var appointment_date;
var appointment_time;
var reason;
var for_self;
var other_data;
var appointment_medium;
var appointment_price;
var payment_type;
var payment_data;





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
    var header = document.getElementById("doctor_head");
    var btns = header.getElementsByClassName("doctors");
    var doctor_id = $("#doctor-"+data).attr('id');

    $('.doctors').map(function(i,el) {
        if($(el).attr("id") != doctor_id){
            $(el).removeClass("doc-active");
            $("#doctor-"+data).addClass(' doc-active');
            $(".doc-"+data).toggle();
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




$(function() {
    //hang on event of form with id=myform
    $("#appointment_form").submit(function(e) {

        //prevent Default functionality
        //e.preventDefault();

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




        // Send the data using post

        //$.ajax({
        //    type: "POST",
        //        url: appointmentFormEndpoint,
        //        data,
        //        success: function(response){
        //        //if request if made successfully then the response represent the data
//
        //        console.log(response);
        //    }
        //});
        var posting = $.post(
            appointmentFormEndpoint,
            data,
        );

       // Put the results in a div
       posting.done(function( data ) {

       console.log(data);

        });

        });
});


var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab



function showTab(n) {
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
    document.getElementById("nextBtn").setAttribute('type', 'submit');
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  // ... and run a function that displays the correct step indicator:
  //fixStepIndicator(n)
}


function nextPrev(n) {
  var x = document.getElementsByClassName("tab");
  if (n == 1 && !validateForm()) return false;

  x[currentTab].style.display = "none";

  currentTab = currentTab + n;

  if (currentTab == x.length) {

    submitTheForm();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
  goToSummary();
}


function validateForm() {
  var valid = true;

  if (valid) {
    console.log('FINSSHHH')
  }
  return valid; // return the valid status
}


function submitTheForm(){
    console.log("SUBMITTTTEEEDDD");
}