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

$('input').on('click', function(){
  let valeur = 0;
  $('input:checked').each(function(){
       if ( $(this).attr('value') > valeur )
       {
           valeur =  $(this).attr('value');
       }
  });
  $('.progress-bar').css('width', valeur+'%').attr('aria-valuenow', valeur);
  $('.progress-text').text(valeur+"%");
});

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
let csrftoken = getCookie('csrftoken');

$('#accept').on('click', function () {
    console.log("next");
    let parameters = {};
    parameters.page = "1";

    let xhr = new XMLHttpRequest();
    xhr.open("POST", '/website/nextpage', true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(parameters));
});
