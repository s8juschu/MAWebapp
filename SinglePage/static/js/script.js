/*
 On page load, display correct page & progress
*/
$(document).ready(function() {
    // display actual score on last page
    displayScore();

    // executes when HTML-Document is loaded and DOM is ready
    for (let i = 0; i < cardCounter; i++) {
        $('#card' + i).hide();
    }
    $('#card' + (cardCounter)).show();
    if( cardCounter > 1){
         fillProgress();
    }

    // Display decribe gender on page reload if checked
    if (cardCounter ===1 && $('#describe').is(":checked")){
        $('#genderText').show();
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

        if (document.getElementById("1824").checked === true){
            parameters.age = "18-24";
        }
        else if (document.getElementById("2531").checked === true){
           parameters.age = "25-31";
        }
        else if (document.getElementById("3238").checked === true){
             parameters.age = "32-38";
        }
        else if (document.getElementById("3945").checked === true){
             parameters.age = "39-45";
        }
        else if (document.getElementById("4652").checked === true){
           parameters.age = "46-52";
        }
        else if (document.getElementById("5359").checked === true){
             parameters.age = "53-59";
        }
        else if (document.getElementById("6065").checked === true){
             parameters.age = "60-65";
        }
        else if (document.getElementById("65").checked === true){
           parameters.age = ">65";
        }
        else{
            document.getElementById('errorPersonalAge').innerHTML = "Please select an answer.";
            missing_answr = "true";
        }

        if (document.getElementById("woman").checked === true){
            parameters.gender = "woman";
        }
        else if (document.getElementById("man").checked === true){
           parameters.gender = "man";
        }
        else if (document.getElementById("non-binary").checked === true){
             parameters.gender = "non-binary";
        }
        else if (document.getElementById("private").checked === true){
             parameters.gender = "prefer not to disclose"; describe
        }
        else if (document.getElementById("describe").checked === true){
             let description = document.getElementById("genderText").value;
             parameters.gender = "prefer to self-describe: " + description;
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


// Display box to self-describe gender if checked, else hide
$('input[type=radio][name=gender]').change(function() {
    if ($('#describe').is(":checked")){
        $('#genderText').show();
    }
    else{
        $('#genderText').hide();
    }
});

// Permanently display score in pos/neg framing condition
$(window).scroll(function(){
    var sticky = document.getElementsByClassName('sticky9');

    if (sticky.length > 0 && document.getElementById("card9").style.display !== "none"){
        if ($(window).scrollTop() >= $("#card9").offset().top ) {
            $('.sticky9').addClass('fixed-header');
        }
        else {
            $('.sticky9').removeClass('fixed-header');

        }
    }
    if (sticky.length > 0 && document.getElementById("card10").style.display !== "none"){
        if ($(window).scrollTop() >= $("#card10").offset().top ) {
            $('.sticky10').addClass('fixed-header');
        }
        else {
            $('.sticky10').removeClass('fixed-header');

        }
    }
});

function saveTextInput() {
    let parameters = {};
    parameters.text = document.getElementById('suspect_deception').value;

    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () { // listen for state changes
        if (this.readyState == 4 && this.status == 200) {
            window.location.href = 'https://prolific.co';
        }
    };
    xhr.open("POST", '/website/saveTextInput', true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(parameters));
}

// Delete answers from questionnaires and tasks for this user
function displayDelete() {
    // document.getElementById('deleteData').innerHTML = "Your data has been deleted!";
    // $('html,body').scrollTop(0);
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () { // listen for state changes
        if (xhr.readyState == 4 && xhr.status == 200) { // when completed we can move away
            saveTextInput();
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
        saveTextInput();
    }
    else{
         $("#deleteModal").modal();
    }
});

//Display actual score of user in first task round on end card
function displayScore() {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () { // listen for state changes
        if (this.readyState == 4 && this.status == 200) {
            const obj = JSON.parse(this.responseText);
            document.getElementById("actual_score_pre").innerHTML = obj.pre;
            document.getElementById("actual_score_main").innerHTML = obj.main;
        }
    };
    xhr.open("GET", '/website/getScore', true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader('Content-Type', 'text/plain');
    xhr.send();
}
