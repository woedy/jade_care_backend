var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab





function showTab(n) {
  // This function will display the specified tab of the form ...
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
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function sendAppointment(){
    $("#appointment_type").change(function (){
        console.log($(this).val());
        var appointment_type = $(this).val();

        $.ajax({
            url: '/appointments/make_appointment_ajax/',
            data: {
                'appointment_type' : appointment_type
            },
            dataType: 'json',
            success: function (data) {

            console.log(data);
            }
        });
    });

}

sendAppointment();


var appointment_type = "New Problem";

var data = {};

data['appointment_type'] = appointment_type;
data['doctor'] = doctor;
 console.log(data);

function setNewProblem(){
    var button = document.getElementById('new_problem').innerHTML;
    appointment_type = button;
    console.log(appointment_type);
}

function setCovid19(){
    var button = document.getElementById('covid_19').innerHTML;
    appointment_type = button;
    console.log(appointment_type);
}

function setProblemFollowUp(){
    var button = document.getElementById('problem_follow_up').innerHTML;
    appointment_type = button;
    console.log(appointment_type);
}



function setAppointmentType(){
    console.log(appointment_type);
    var header = document.getElementById("ap_type");
    var btns = header.getElementsByClassName("apFormButton");

    for (var i = 0; i < btns.length; i++) {
        btns[i].addEventListener("click", function() {
        var current = document.getElementsByClassName("ap-active");
        current[0].className = current[0].className.replace(" ap-active", "");
        this.className += " ap-active";
  });
}
}

setAppointmentType();

