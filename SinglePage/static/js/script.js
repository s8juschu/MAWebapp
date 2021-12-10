let maxValue = "5";
// let progressCounter = 0;

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

// Display Continue only if check on first card
document.getElementById('checkbox').onclick = function () {
    toggleSub(this, 'accept');
};

function toggleSub(box, id) {
    let el = document.getElementById(id);

    if (box.checked) {
        el.style.display = 'block';
    } else {
        el.style.display = 'none';
    }
}

// //Fill progressbar
function fillProgress(){
    console.log(progressCounter);
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

//Display cards one after another
function displayCards() {
    if((cardCounter) < maxValue+1){
        $('#card' + cardCounter).hide();
        $('#card' + (cardCounter+1)).show();
        cardCounter += 1;
    }
    setSession();
}

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

function setSession() {
    console.log(progressCounter);
    let parameters = {};
    parameters.page = cardCounter;
    parameters.progress = progressCounter;

    let xhr = new XMLHttpRequest();
    xhr.open("POST", '/website/saveSession', true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(parameters));
}
