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
