import pymysql
import redis
import base64

r = redis.Redis(host='47.100.200.132', port='6379')
con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='item', charset='utf8')
cursor = con.cursor(pymysql.cursors.DictCursor)
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pymysql
import redis
import json
import time
import random
import re
import captcha
from myapp import forms
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

r = redis.Redis(host="47.100.200.132", port=6379)
conn = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)


def get_token(func):
    def in_func(request):
        from qiniu import Auth
        access_key = 'ln1sRuRjLvxs_7jjVckQcauIN4dieFvtcWd8zjQF'
        secret_key = 'YogFj8XEOnZOfkapjAL2UuMmtujVEONBJRbowx-p'
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = 'haima'
        # 上传到七牛后保存的文件名
        key = None
        # 生成上传 Token，可以指定过期时间等
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        policy = {
            "scope": "haima",
            # 'callbackUrl': 'http://g1.xmgc360.com/callback/',
            # 'callbackBody': 'filename=$(fname)&filesize=$(fsize)&"key"=$(key)',
            # 'returnUrl': 'http://g1.xmgc360.com/callback/'
            # 'persistentOps':'imageView2/1/w/200/h/200'
        }
        # 3600为token过期时间，秒为单位。3600等于一小时
        token = q.upload_token(bucket_name, key, 3600, policy)
        print(token)
        return func(request, token)
    return in_func


def homepage(request):
    sql = "select * from goods_test limit 0,10"
    cursor.execute(sql)
    goods_list = cursor.fetchall()
    for goods in goods_list:
        goods['img_url'] = r.srandmember(goods['goods_id'], 1)[0].decode('utf-8')
    return render(request, 'homepage.html', {'goods_list': goods_list})


# 登录
def login(request):
    username = request.session.get('username')
    if username:
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        code = CaptchaStore.generate_key()
        return render(request, "login.html", locals())
    else:
        username = ''
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        code = CaptchaStore.generate_key()
        return render(request, "login.html", locals())
    #
    # return render(request, "login.html", locals())


# 图片验证码


# def ajax_captcha(request):
#     global login_code
#     if request.is_ajax():
#         result = CaptchaStore.objects.filter(response=request.GET.get('response'), hashkey=request.GET.get('hashkey'))
#         if result:
#             login_code = {'status': 1}
#         else:
#             login_code = {'status': 0}
#         return HttpResponse(json.dumps(login_code))


# 登录验证
def login_ajax(request):
    # 验证码判断
    login_code = {}
    if request.is_ajax():
        a = request.POST.get('response')
        print(a, request.POST.get('hashkey'))
        result = CaptchaStore.objects.filter(response=request.POST.get('response'), hashkey=request.POST.get('hashkey'))
        if result:
            print(result)
            login_code = {'status': 1}
            print(login_code)
        else:
            login_code = {'status': 0}
            print(login_code)
    # 获取表单信息
    username = request.POST.get("username")
    password = request.POST.get("password")
    cur.execute("select * from user where username=%s", [username, ])  # 全表搜索，待建立索引
    user_login = cur.fetchone()
    if user_login is None:  # 判断用户名密码
        error = "login_error"
        return HttpResponse(json.dumps({"msg": error}))
    else:
        if login_code['status'] == 1:  # 判断验证码
            print(login_code['status'])
            if password == user_login['password']:  # 判断用户名密码
                error = "login_ok"
                return HttpResponse(json.dumps({"msg": error}))
            else:
                error = "login_error"  # 用户名或密码错误
                return HttpResponse(json.dumps({"msg": error}))
        else:
            error = "code_error"  # 验证码错误
            return HttpResponse(json.dumps({"msg": error}))


# 注册
def register(request):
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    code = CaptchaStore.generate_key()
    return render(request, 'register.html', locals())


# 注册条件判断
def register_ajax(request):
    global user_error
    if request.method == "GET":
        # 获取用户名：
        username = request.GET.get("username")
        cur.execute("select * from user where username=%s", [username, ])  # 全表搜索，待建立索引
        user_list = cur.fetchall()
        if len(username) in range(6, 17):
            check_name = re.compile(r'^\w+$')
            check_ = check_name.match(username)
            if check_ is None:
                user_error = "用户名为6-16位的数字或英文"
                return HttpResponse(json.dumps({"error": user_error}))
            else:
                if user_list:  # 判断用户名是否存在
                    user_error = "用户名已存在"
                    return HttpResponse(json.dumps({"error": user_error}))
                else:
                    user_error = ""  # 用户名可用
                    return HttpResponse(json.dumps({"error": user_error}))
        else:
            user_error = "用户名为6-16位的数字或英文"
            return HttpResponse(json.dumps({"error": user_error}))

    else:
        login_code = {}
        if request.is_ajax():
            a = request.POST.get('response')
            print(a, request.POST.get('hashkey'))
            result = CaptchaStore.objects.filter(response=request.POST.get('response'),
                                                 hashkey=request.POST.get('hashkey'))
            if result:
                print(result)
                login_code = {'status': 1}
                print(login_code)
            else:
                login_code = {'status': 0}
                print(login_code)
        # 获取用户表单信息
        username = request.POST.get("username")
        password = request.POST.get("password")
        # email = request.POST.get("email")
        phone = request.POST.get("phone")
        # code = request.POST.get("code")
        check_code = r.get(phone)  # 获取手机验证码
        check_all = request.POST.get("check_all")
        print(username, password, phone, check_code, check_all, login_code)
        if login_code['status'] == 1:  # 图片验证码
            check_code = check_code.decode('utf8')
            if check_code:  # 手机验证码待定！
                if user_error == "" and check_all == 'true':
                    cur.execute("insert into user(username,password,phone) values(%s,%s,%s)",
                                [username, password, phone])
                    # print(username, email, phone, password)
                    r.delete(phone)
                    code_error = 'register_ok'  # 注册成功，跳转
                    request.session['username'] = username
                    return HttpResponse(json.dumps({"msg": code_error}))
                elif user_error == "用户名已存在":
                    code_error = 'user_exists'  # 用户名存在
                    return HttpResponse(json.dumps({"msg": code_error}))
                else:
                    code_error = 'check_all'  # 检查是否有错误
                    return HttpResponse(json.dumps({"msg": code_error}))
            else:
                code_error = 'phone_code_error'  # 手机验证码错误验证码
                return HttpResponse(json.dumps({"msg": code_error}))

        else:
            code_error = 'img_code_error'  # 图片验证码错误
            return HttpResponse(json.dumps({"msg": code_error}))
            # code_error = 'phone_code_error'  # 手机验证码错误验证码
            # return HttpResponse(json.dumps({"msg": code_error}))


# 验证码：
def code(request):
    phone = request.GET.get("phone")
    code_ = random.randint(100000, 999999)
    print(code, phone)
    r.set(phone, code_, 60)
    return HttpResponse(code)


# 注册成功页面跳转
def register_ok(request):
    return render(request, "register_ok.html")


# 商品分类展示
def goods_list(request):
    return render(request, 'goods_list.html')


# 发布商品
@get_token
def publish(request,token):
    return render(request, 'publish.html',{'token': token})


# 估价
def assess(request):
    return render(request, 'assess.html')


# 拍卖
def auction_index(request):
    return render(request, 'auction_index.html')

# 历史拍卖
def history_auction(request):
    return render(request,'histroy_auction.html')

# 我的拍卖
def my_auction(request):
    return render(request,'my_auction.html')

# 发布拍卖
def release_auction(request):
    return render(request,'release_auction.html')


# 用户中心
def user_center(request):
    return render(request, 'user_center.html')


# 我出售的
def my_sale(request):
    return render(request, 'my_sale.html')


# 我购买的
def my_buy(request):
    return render(request, 'my_buy.html')


# 我的地址
def address(request):
    return render(request, 'address.html')


@get_token
def test_qiniu(request, token):
    return render(request, '7cow.html', {'token': token})


def callback(request):
    if request.method == 'GET':
        key_json_base64 = request.GET.get('upload_ret')
        key_json= base64.b64decode(key_json_base64).decode('utf-8')
        print(key_json)
        key_dict = json.loads(key_json)
        key= key_dict['key']
        print(key)
        return HttpResponse('pgwecu7z4.bkt.clouddn.com/'+key+'-haima.shuiy')
    else:
        # json_result = json.loads(postBody)
        # print(json_result)
        return HttpResponse("POST")
