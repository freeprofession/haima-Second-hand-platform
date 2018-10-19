//验证密码
function checkPassword() {
    // pwd_ = document.getElementById('pwd').value;
    var userpasswd = document.getElementById('pwd');
    var pattern = /^\w{6,16}$/;
    if (!pattern.test(userpasswd.value)) {
        document.getElementById('pwd_error').style.color = 'Red';
        document.getElementById('pwd_error').style.display = 'block';
        return false
    }
    else {
        document.getElementById('pwd_error').style.display = 'none';
        return true
    }
}

//确认密码
function ConfirmPassword() {
    var userpasswd = document.getElementById('pwd');
    var userConPassword = document.getElementById('cpwd');
    if ((userpasswd.value) !== (userConPassword.value) || userConPassword.value.length === 0) {
        document.getElementById('cpwd_error').style.color = 'Red';
        document.getElementById('cpwd_error').style.display = 'block';
        return false;
    }
    else {
        document.getElementById('cpwd_error').style.display = 'none';
        return true;
    }
}

//验证手机号
function checkPhone() {
    var phone = document.getElementById('phone');
    var pattern = /^1[34578]\d{9}$/; //验证手机号正则表达式
    if (!pattern.test(phone.value)) {
        document.getElementById('phone_error').style.color = 'Red';
        document.getElementById('phone_error').style.display = 'block';
        return false;
    }
    else {
        document.getElementById('phone_error').style.display = 'none';
        return true;
    }
}

function checkall() {
    flag1 = checkPassword()
    flag2 = ConfirmPassword()
    flag3 = checkPhone()
    return flag1 && flag2 && flag3


}


