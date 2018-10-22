import pymysql
import redis

r = redis.Redis(host='47.100.200.132', port='6379')
con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='item', charset='utf8')
cursor = con.cursor(pymysql.cursors.DictCursor)
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import pymysql
import redis
import json
import time
import random
import re
import datetime
import captcha
from myapp import forms
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

r = redis.Redis(host="47.100.200.132", port=6379)
conn = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)


def homepage(request):
    username = request.session.get('username')
    if username:
        login_status = username
    else:
        login_status = '未登录'
    sql = "select * from goods_test limit 0,10"
    cursor.execute(sql)
    goods_list = cursor.fetchall()
    for goods in goods_list:
        goods['img_url'] = r.srandmember(goods['goods_id'], 1)[0].decode('utf-8')
    return render(request, 'homepage.html', locals())


def homepage_ajax(request):
    pass


# 登录
def login(request):
    username = request.session.get('username')
    if username:
        print(username)
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
    cur.execute("select * from t_user where user_name=%s", [username, ])  # 全表搜索，待建立索引
    user_login = cur.fetchone()
    user_id = user_login['user_id']
    if user_login is None:  # 判断用户名密码
        error = "login_error"
        return HttpResponse(json.dumps({"msg": error}))
    else:
        if login_code['status'] == 1:  # 判断验证码
            print(login_code['status'])
            if password == user_login['password']:  # 判断用户名密码
                error = "login_ok"
                request.session['username'] = username
                request.session['user_id'] = user_id
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

            if check_code:  # 手机验证码待定！
                check_code = check_code.decode('utf8')
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


# 用户中心
def user_center_info(request):
    username = request.session.get('username')
    if username:
        cur.execute("select * from t_user where user_name=%s", [username, ])
        user_info = cur.fetchall()
        for i in user_info:
            print(i)
        return render(request, 'user_center_info.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# 商品界面设置
def goods(request):
    username = request.session.get('username')  # 获取买家用户名
    user_id = request.session.get('user_id')  # 获取买家ID
    goods_id = request.GET.get('shangping_id')  # 获取商品ID
    cur.execute("select * from t_goods where goods_id=%s", [goods_id, ])  # 获取商品表内容
    goods_list = cur.fetchall()
    seller_id = goods_list['user_id']  # 获取卖家ID
    cur.execute("select * from t_user where user_id=%s", [seller_id, ])  # 获取卖家信息
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 记录当前时间
    print(username, user_id, goods_id, seller_id, now_time)
    if username:
        login_status = username
        count = goods_list['goods_browse_count']
        count += 1
        # 更新商品浏览次数
        cur.execute("update t_goods set goods_browse_count=%s where goods_id=%s", [count, goods_id])
        # 用户浏览记录
        cur.execute("insert into t_user_browse(browse_user_id,browse_date,browse_goods_id) value(%s,%s,%s) ",
                    [user_id, now_time, goods_id])
        conn.commit()
    else:
        login_status = '未登录'
    return render(request, "goods_info.html", locals())


def publish(request):
    return render(request, 'publish.html')


def auction(request):
    return render(request, 'auction-index.html')


def sale(request):
    return render(request, 'sale.html')


def buy(request):
    return render(request, 'buy.html')


def address(request):
    return render(request, 'address.html')
