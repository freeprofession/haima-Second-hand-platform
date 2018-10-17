function change_div(id) {
    if (id == 'dc1') {
        document.getElementById("dc2").style.display = 'none';
        document.getElementById("dc3").style.display = 'none';
        document.getElementById("dc1").style.display = 'block';

    }
    if (id == 'dc2') {
        document.getElementById("dc1").style.display = 'none';
        document.getElementById("dc3").style.display = 'none';
        document.getElementById("dc2").style.display = 'block';


    }
    if (id == 'dc3') {
        document.getElementById("dc1").style.display = 'none';
        document.getElementById("dc2").style.display = 'none';
        document.getElementById("dc3").style.display = 'block';
    }
}



