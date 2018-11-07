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

// function allow() {
//     var state = document.getElementById("allow")
//     if (state.checked) {
//         document.getElementById('allow_').style.display = 'none';
//         return true
//     } else
//         document.getElementById('allow_').style.color = 'Red';
//         document.getElementById('allow_').style.display = 'block';
//        return false
//
// }
function phone_code() {
    var phone_code = document.getElementById('msg_code');
    if (phone_code.value.length === 0) {
        document.getElementById('phone_code_error').style.color = 'Red';
        document.getElementById('phone_code_error').innerText = '验证码不为空';
        return false
    }
    else {
        document.getElementById('phone_code_error').style.color = '#73858C';
        return true
    }

}

function picture_code() {
    var pic_code = document.getElementById('pic_code')
    if (pic_code.value.length === 0) {
        document.getElementById('pic_code_error').style.color = 'Red';
        return false
    } else {
        document.getElementById('pic_code_error').style.color = '#73858C';
        return true
    }

}

var code_ = false;

function get_code() {
    code_ = true;
}


function checkall() {
    flag1 = checkPassword()
    flag2 = ConfirmPassword()
    flag3 = checkPhone()
    // flag4=allow()
    flag5 = phone_code()
    flag6 = picture_code()
    if (code === false) {
        document.getElementById('phone_code_error').style.color = '#73858C';
        document.getElementById('phone_code_error').innerText = '请获取验证码';
    }
    var a = document.getElementById('allow')
    if (a.checked) {
        a = true
        document.getElementById('allow_').style.color = 'Red';
        document.getElementById('allow_').innerText = '';
    } else {
        a = false
        document.getElementById('allow_').style.color = 'Red';
        document.getElementById('allow_').innerText = '请勾选同意';

    }
    return flag1 && flag2 && flag3 && flag5 && flag6 && code_ && a


}


