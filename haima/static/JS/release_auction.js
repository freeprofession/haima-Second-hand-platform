function  checktitle() {
    title=document.getElementById('goods_title');
    if(title.trim().length<=5) {
        document.getElementById('error_message').innerText='标题不能小于5个字'
        document.getElementById('error_messgage').style.display=='block';
        return false;
    }
    else {
        return true
    }
}
