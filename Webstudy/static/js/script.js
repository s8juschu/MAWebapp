document.getElementById('checkbox').onclick = function () {
    console.log("here");
    toggleSub(this, 'accept');
};

function toggleSub(box, id) {
    var el = document.getElementById(id);

    if (box.checked) {
        el.style.display = 'block';
    } else {
        el.style.display = 'none';
    }
}
