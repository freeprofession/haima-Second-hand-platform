function checktitle() {
    var checktitle = document.getElementById("checktitle");
    if (pub_goods.title.value == "") {
        checktitle.style.display = "block";
        return true

    }
    else {
        checktitle.style.display = "none";
        return false
    }


}

function checkprice() {
    var checkprice = document.getElementById("checkprice");
    var reg = /^\d+(\.\d{0,2})?$/;
    if (pub_goods.price.value == "") {
        checkprice.innerHTML = "价格不能为空";
        checkprice.style.display = "block";
        return true;
    }
    if (reg.test(pub_goods.price.value)) {
        checkprice.style.display = "none";
        return false;
    } else {
        checkprice.innerHTML = "格式错误"
        checkprice.style.display = "block";
        return true;
    }

}

function checkform() {
    if (checktitle()){
        return false
    }
    if (checkprice()) {
        return false
    }
    return true
}

