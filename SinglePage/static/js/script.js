/*
 On page load, display correct page & progress
*/
$(document).ready(function() {
    // executes when HTML-Document is loaded and DOM is ready
    for (let i = 0; i < cardCounter; i++) {
        $('#card' + i).hide();
    }
    $('#card' + (cardCounter)).show();
    if( cardCounter > 1){
         fillProgress();
    }
});

/*
 Display Continue btn only if check on first card
*/
document.getElementById('checkbox').onclick = function () {
    toggleSub(this, 'accept');
};

function toggleSub(box, id) {
    let el = document.getElementById(id);

    if (box.checked) {
        el.style.display = '';
    } else {
        el.style.display = 'none';
    }
}

/*
 Calculate and fill progressbar
*/
function fillProgress(){
    if(progressCounter < 100) {
        progressCounter += (100/maxValue);
        if(progressCounter > 100) {
            console.log(progressCounter);
            progressCounter = 100;
        }
        let val = Math.round(progressCounter);
        $('.progress-bar').css('width', val+'%').attr('aria-valuenow', val);
        $('.progress-text').text(val+"%");
    }
}

/*
Display cards one after another
*/
function displayCards() {
    if((cardCounter) < maxValue+1){
        $('#card' + cardCounter).hide();
        $('#card' + (cardCounter+1)).show();
        cardCounter += 1;
    }
    setSession();
    // Scroll to top of page
    $('html,body').scrollTop(0);
}

/*
 Get cookie for POST request
*/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrfToken = getCookie('csrftoken');

/*
 Save current page & counter
*/
function setSession() {
    let parameters = {};
    parameters.page = cardCounter;
    parameters.progress = progressCounter;

    let xhr = new XMLHttpRequest();
    xhr.open("POST", '/website/saveSession', true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(parameters));
}

/*
 Save personal information
*/
function setData(v) {
    let parameters = {};
    if (v === "agree"){
        parameters.type = "agree";
        parameters.agree = "true"
    }
    if (v === "personal"){
        let missing_answr = "false";
        document.getElementById('errorPersonalAge').innerHTML = "";
        document.getElementById('errorPersonalGender').innerHTML = "";

        parameters.type = "personal";
        parameters.age = document.getElementById("age").value;
        if (parameters.age == null || parameters.age === "") {
            document.getElementById('errorPersonalAge').innerHTML = "Please enter your age.";
            missing_answr = "true";
        }
        if (parameters.age < 1 || parameters.age > 100){
            document.getElementById('errorPersonalAge').innerHTML = "Please enter a valid age.";
            missing_answr = "true";
        }

        if (document.getElementById("female").checked === true){
            parameters.gender = "female";
        }
        else if (document.getElementById("male").checked === true){
           parameters.gender = "male";
        }
        else if (document.getElementById("other").checked === true){
             parameters.gender = "other";
        }
        else if (document.getElementById("private").checked === true){
             parameters.gender = "prefer not to say";
        }
        else{
            document.getElementById('errorPersonalGender').innerHTML = "Please select an answer.";
            missing_answr = "true";
        }

         if (missing_answr === "true"){
             document.getElementById('errorPersonal').innerHTML = "Some answers are missing. Please answer all questions before continuing.";
            $('html,body').scrollTop(0);
             return;
         }
         else if (missing_answr === "false"){
             displayCards(); fillProgress();
         }
    }
    if (v === "finish"){
        parameters.type = "finish";
        parameters.finish = "true"
    }

    document.getElementById('errorPersonal').innerHTML = "";

    let xhr = new XMLHttpRequest();
    xhr.open("POST", '/website/saveData', true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(parameters));
}

// Permanently display score in pos/neg framing condition
$(window).scroll(function(){
    var sticky = document.getElementsByClassName('sticky9');

    if (sticky.length > 0 && document.getElementById("card9").style.display !== "none"){
        console.log("here 9");
        console.log($(window).scrollTop());
        console.log($("#card9").offset().top );
        if ($(window).scrollTop() >= $("#card9").offset().top ) {
            $('.sticky9').addClass('fixed-header');
        }
        else {
            $('.sticky9').removeClass('fixed-header');

        }
    }
    if (sticky.length > 0 && document.getElementById("card10").style.display !== "none"){
        console.log("here n10");
        console.log($(window).scrollTop());
        console.log($("#card10").offset().top );
        if ($(window).scrollTop() >= $("#card10").offset().top ) {
            $('.sticky10').addClass('fixed-header');
        }
        else {
            $('.sticky10').removeClass('fixed-header');

        }
    }
});

// Delete answers from questionnaires and tasks for this user
function displayDelete() {
    // document.getElementById('deleteData').innerHTML = "Your data has been deleted!";
    // $('html,body').scrollTop(0);
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() { // listen for state changes
      if (xhr.readyState == 4 && xhr.status == 200) { // when completed we can move away
       window.location.href = 'https://prolific.co';
      }
    };
    xhr.open("POST", '/website/deleteData', true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
}

//Display modal if consent form not checked
$('#endSurvey').click(function () {
    if($("#check_debriefing").is(':checked')){
        window.location.href = 'https://prolific.co';
    }
    else{
         $("#deleteModal").modal();
    }
});


// $('#revokeData').click(function () {
//     // window.location.href = 'https://prolific.co';
//     console.log("redirect");
// });
