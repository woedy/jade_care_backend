// FORM VARIABLES
var appointment_type;
var doctor;
var appointment_date;
var appointment_time;



// APPOINTMENT TYPE
function setAppointmentType(){
    var header = document.getElementById("ap_type");
    var btns = header.getElementsByClassName("app_type_btn");

    if(appointment_type == "New Problem"){
        $("#new_problem_btn").addClass("app_type_active");
        $("#covid_19_btn").removeClass("app_type_active");
        $("#problem_follow_up_btn").removeClass("app_type_active");
    }

    if(appointment_type == "Covid-19"){
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
    appointment_type = button;
    setAppointmentType();
}

function setProblemFollowUp(){
    var button = document.getElementById('problem_follow_up').innerHTML;
    appointment_type = button;
    setAppointmentType();
}


// APPOINTMENT DOCTOR

function setDoctor(data){

    is_selected = false;

    var header = document.getElementById("doctor_head");
    var btns = header.getElementsByClassName("doctors");

   doctor = data;

   console.log(doctor);

   $("."+data).toggle();


}

$(".app_time_tab").hide();



function setDoctorInit(data){

    is_selected = false;

    var header = document.getElementById("doctor_head");
    var btns = header.getElementsByClassName("doctors");

    for(var i = 0; i < btns.length; i++){
        var current = document.getElementsByClassName("doctors");
        current[0].classList.add("doc_active");

    }

}






function setTime(data){
    var button = document.getElementById("time"+data).value;
    //appointment_time = button;
    if(){

    }
    $("#time"+data).removeClass("btn-secondary");
    $("#time"+data).addClass("btn-primary");

    console.log(data);

}