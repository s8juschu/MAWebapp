/*
 On page load, display correct page & progress
 // executes when HTML-Document is loaded and DOM is ready
*/
$(document).ready(function() {
    // display actual score on last page
    displayScore();

    //save/load status of extra tasks in local storage
    if (localStorage.getItem("extraTaskCounter") === null) {
        localStorage.setItem("extraTaskCounter", "1");
    }
    let sessStor =  parseInt(localStorage.getItem("extraTaskCounter"), 10);
    $('#extraTask' + sessStor).show();
    if (sessStor === 1){
        $('#extraTask' + sessStor).show();
    }

    //Display correct card & progress
    for (let i = 0; i < cardCounter; i++) {
        $('#card' + i).hide();
    }
    $('#card' + (cardCounter)).show();
    if( cardCounter > 1){
         fillProgress();
    }

    // Display describe gender on page reload if checked
    if (cardCounter === 1 && $('#describe').is(":checked")){
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
     if ((cardCounter) < maxValue + 1) {
        $('#card' + cardCounter).hide();
        $('#card' + (cardCounter + 1)).show();
        cardCounter += 1;
    }
    setSession();
    // Scroll to top of page
    $('html,body').scrollTop(0);
}

/*
Display end card
*/
function displayLastCard(){
    $('#card' + cardCounter).hide();
    $('#card' + (maxValue + 1)).show();
    cardCounter = (maxValue + 1);

    fillProgress();

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
    xhr.onreadystatechange = function () { // listen for state changes
        if (this.readyState === 4) {
            if (this.status === 200) {
                if (!((cardCounter-1) === 0)){
                    fillProgress();
                }
            } else {
                if ((cardCounter) < maxValue + 1) {
                    $('#card' + cardCounter).hide();
                    $('#card' + (cardCounter - 1)).show();
                    cardCounter -= 1;
                }

                window.location.reload();
            }
        }
    };
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
             displayCards();
         }
    }
    if (v === "finish"){
        parameters.type = "finish";
        parameters.finish = "true"
    }

    document.getElementById('errorPersonal').innerHTML = "";

    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () { // listen for state changes
        if (v === "finish" && (this.readyState == 4 && this.status == 200)) {
            setTimeout(function(){ window.location.href = 'https://app.prolific.co/submissions/complete?cc=4FED7A67'; }, 8000);
            window.location.href = 'https://app.prolific.co/submissions/complete?cc=4FED7A67';
            // setData('finish');
        }
    };
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

// Display box to explain deception if checked, else hide
$('input[type=radio][name=deception]').change(function() {
    if ($('#deception_yes').is(":checked")){
        $('#div_text_deception').show();
    }
    else{
        $('#div_text_deception').hide();
    }
});


// Permanently display score in pos/neg framing condition
// $(window).scroll(function(){
//     var sticky = document.getElementsByClassName('sticky9');
//
//     if (sticky.length > 0 && document.getElementById("card9").style.display !== "none"){
//         if ($(window).scrollTop() >= $("#card9").offset().top ) {
//             $('.sticky9').addClass('fixed-header');
//         }
//         else {
//             $('.sticky9').removeClass('fixed-header');
//
//         }
//     }
//     if (sticky.length > 0 && document.getElementById("card10").style.display !== "none"){
//         if ($(window).scrollTop() >= $("#card10").offset().top ) {
//             $('.sticky10').addClass('fixed-header');
//         }
//         else {
//             $('.sticky10').removeClass('fixed-header');
//
//         }
//     }
// });

// Save if participant suspected deception and optional comments
function saveDeceptionInput() {

    let parameters = {};
    parameters.text = document.getElementById('text_deception').value;

    if($("#deception_yes").is(':checked')){
        parameters.suspect = "true";
    }
    else if($("#deception_no").is(':checked')){
         parameters.suspect = "false";
    }
    else {
        alert("Please answer if you suspected the deception");
        return;
    }

    // setData('finish');

    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () { // listen for state changes
        if (this.readyState == 4 && this.status == 200) {
            // setTimeout(function(){ window.location.href = 'https://prolific.co'; }, 8000);
            // window.location.href = 'https://prolific.co';
            setData('finish');
        }
    };
    xhr.open("POST", '/website/saveDeceptionInput', true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(parameters));
}

// Delete answers from questionnaires and tasks for this user
function displayDelete() {
    let text = document.getElementById('text_deception').value;
    if (!($("#deception_yes").is(':checked')) && !($("#deception_no").is(':checked'))){
        alert("Please answer if you suspected the deception");
        return;
    }

    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () { // listen for state changes
        if (xhr.readyState == 4 && xhr.status == 200) { // when completed we can move away
            saveDeceptionInput();
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
        saveDeceptionInput();
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
            let obj = JSON.parse(this.responseText);
            document.getElementById("actual_score_pre").innerHTML = obj.pre;
            document.getElementById("actual_score_main").innerHTML = obj.main;

            if(obj.hasOwnProperty('extra')){
                document.getElementById("actual_score_extra").innerHTML = "In the bonus round, you answered <b>"+ obj.extra+" out of";
                document.getElementById("actual_score_count").innerHTML = "<b>"+ obj.count + " tasks </b> correctly.";
            }

        }
    };
    xhr.open("GET", '/website/getScore', true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader('Content-Type', 'text/plain');
    xhr.send();
}

// Display one extra task after another
function displayNextTask() {
    let sessStor =  parseInt(localStorage.getItem("extraTaskCounter"), 10);
    if ((sessStor) < 8) {
        $('#extraTask' + sessStor).hide();
        $('#extraTask' + (sessStor + 1)).show();
        sessStor += 1;
        localStorage.setItem("extraTaskCounter", String(sessStor));
    }
    else {
        displayCards();
    }
}

// If badge modal closed, show next page
$('#badgem1Modal').on('hidden.bs.modal', function () {
    saveTask('m1');
});
$('#badgem2Modal').on('hidden.bs.modal', function () {
    saveTask('m2');
});
