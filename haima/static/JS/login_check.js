$(function () {
    $("#login").click(function () {
        username = $('#username').val();
        password = $('#password').val();
        code = $('#login_code').val();
        response = $('#login_code').val();
        hashkey = $('#hash').val();
        $.post('/login_ajax/', {
            'username': username,
            'password': password,
            'code': code,
            'response': response,
            'hashkey': hashkey,
        }, function (data) {
            if (data.msg === 'login_ok') {
                location.href = '/haima/'
            } else if (data.msg === 'code_error') {
                $('#code_error').html('验证码错误');
            } else if (data.msg === "login_error") {
                $('#login_error').html('用户名或密码错误')
            }
        }, 'json')

    })

});
