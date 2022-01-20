// On page load, display correct page & progress
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

// Display Continue btn only if check on first card
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

//Fill progressbar
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

//Display cards one after another
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

// Save current page & counter
// Save answer
function setSession() {
    let parameters = {};
    parameters.page = cardCounter;
    parameters.progress = progressCounter;
    if ( 0 < cardCounter < maxValue){
        // parameters.answer = $('#textarea' + (cardCounter-1)).val();
    }

    let xhr = new XMLHttpRequest();
    xhr.open("POST", '/website/saveSession', true);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(parameters));
}

//Save values IMI
function saveIMI(type) {
    // let parameters = {};
    // parameters.type = type;
    // for (var i = 0; i < 5; i++) {
    //    console.log($('input[name=scale'+i+']:checked').val());
    // }
    //
    // var rep1 =
    // let xhr = new XMLHttpRequest();
    // xhr.open("POST", '/website/saveIMI', true);
    // xhr.setRequestHeader("X-CSRFToken", csrfToken);
    // xhr.setRequestHeader('Content-Type', 'application/json');
    // xhr.send(JSON.stringify(parameters));

}
//
// //Save values PXI
// function savePXI() {
//         for (var i = 0; i < 5; i++) {
//        console.log($('input[name=scale'+i+']:checked').val());
//     }
// }
