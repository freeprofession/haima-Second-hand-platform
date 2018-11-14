import pymysql
import time
from utils.pay import AliPay
from aip import AipImageSearch

APP_ID = '14640597'
API_KEY = '6pT1zsnXTY7Ywkx5OuOZjEFg'
SECRET_KEY = 'gIG4esr46GPbTTVOLGcbfDnYtiLxyISh'

client = AipImageSearch(APP_ID, API_KEY, SECRET_KEY)

st_time = time.localtime(time.time())
loc_time = '{}-{}-{}'.format(st_time.tm_year, st_time.tm_mon, st_time.tm_mday)
import base64

con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = con.cursor(pymysql.cursors.DictCursor)
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import redis
import json
import random
import re
import datetime
import jieba
import captcha
from myapp import forms
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myapp import phone_model
# from myapp import AI_assess
from myapp import goods_recommend


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


r = redis.Redis(host="47.100.200.132", port=6379, password='haima1234')
r1 = redis.Redis(host="47.100.200.132", port=6379, db=1, password='haima1234')
img = redis.Redis(host="47.100.200.132", port=6379, db=2, password='haima1234')
category = redis.Redis(host="47.100.200.132", port=6379, db=3, password='haima1234')
cut_words = redis.Redis(host="47.100.200.132", port=6379, db=4, password='haima1234')
auction_img = redis.Redis(host="47.100.200.132", port=6379, db=5, password='haima1234')
sms = redis.Redis(host="47.100.200.132", port=6379, db=5, password='haima1234')  # 注册验证码
set_eva = redis.Redis(host="47.100.200.132", port=6379, db=7, password='haima1234')  # 设置评论
get_eva = redis.Redis(host="47.100.200.132", port=6379, db=8, password='haima1234')  # 得到评论
user_recommend = redis.Redis(host="47.100.200.132", port=6379, db=9, password='haima1234')  # 用户推荐
goods_browse = redis.Redis(host="47.100.200.132", port=6379, db=10, password='haima1234')  # 浏览记录
message_push = redis.Redis(host="47.100.200.132", port=6379, db=11, password='haima1234')  # 消息推送


def get_token(func):
    def in_func(request):
        from qiniu import Auth
        access_key = 'ln1sRuRjLvxs_7jjVckQcauIN4dieFvtcWd8zjQF'
        secret_key = 'YogFj8XEOnZOfkapjAL2UuMmtujVEONBJRbowx-p'
        q = Auth(access_key, secret_key)
        bucket_name = 'haima'
        key = None
        policy = {
            "scope": "haima",
            # "returnBody":
            # 'callbackUrl': 'http://g1.xmgc360.com/callback/',
            # 'callbackBody': 'filename=$(fname)&filesize=$(fsize)&"key"=$(key)',
            # 'returnUrl': 'http://g1.xmgc360.com/callback/'
            # 'persistentOps':'imageView2/1/w/200/h/200'
        }
        token = q.upload_token(bucket_name, key, 3600, policy)
        return func(request, token)

    return in_func


def send_sms(request):
    from urllib import request as rq
    phone = request.POST.get('phone')
    identify = random.randint(100000, 999999)
    print(phone)
    textmod = {"sid": "5e7761804d551f3d6184322133855f37",
               "token": "3e877f5f0eaee4b6eb75597db115d720",
               "appid": "60de937cff7d4a458ab4a0404468abd3",
               "templateid": "393404",
               "param": identify,
               "mobile": phone,
               "uid": phone}
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
    req = rq.Request(url='https://open.ucpaas.com/ol/sms/sendsms', data=textmod, headers=header_dict)
    res = rq.urlopen(req)
    res = res.read().decode('utf-8')
    print(res)
    sms.set(phone, identify, 180)
    return HttpResponse(json.dumps(res))


def mysql_required(function):
    def mysql_restart(request):
        con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
        cur = con.cursor(pymysql.cursors.DictCursor)
        return function(request)

    return mysql_restart


# 登录状态检查，装饰器
def login_required(function):
    @mysql_required
    def check_login_status(request):
        user = request.session.get('user')
        user_id = request.session.get('user_id')
        if user_id:
            return function(request)
        elif user:
            return function(request)
        else:
            return HttpResponseRedirect('/login/')

    return check_login_status


# 权限装饰器
def root_request(function):
    @mysql_required
    @login_required
    def check_request(request):
        user_id = request.session.get('user_id')
        customer = request.GET.get('customer')
        goods_id = request.GET.get('goods_id')
        print("权限：", user_id, customer, goods_id, "______________________________________")
        if customer == "buy":
            cur.execute("select * from t_order_success where order_goods_id=%s and buy_user_id=%s", [goods_id, user_id])
            buy_check = cur.fetchone()
            if buy_check:
                print(buy_check)
                return function(request)
            else:
                return HttpResponseRedirect('/haima/')
        elif customer == "sell":
            cur.execute("select * from t_order_success where order_goods_id=%s and release_user_id=%s",
                        [goods_id, user_id])
            sell_check = cur.fetchone()
            # print(sell_check)
            if sell_check:
                return function(request)
            else:
                return HttpResponseRedirect('/haima/')
        else:
            return HttpResponseRedirect('/haima/')

    return check_request


def message_push_(function):
    def message_push_1(request):
        user_id = request.session.get('user_id')
        message_check1 = message_push.lrange(user_id, 0, 1)
        if message_check1:
            message_push.delete(user_id)
        return function(request)

    return message_push_1


@mysql_required
def homepage(request):
    a = 0
    request.session["wo"] = a
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        login_status = username
        cur.execute("select user_address from t_user where user_id = %s", [user_id])
        user_address = cur.fetchone()
        if user_address['user_address']:
            cur.execute(
                "select * from t_goods where goods_address = %s order by rand() limit 5",
                [user_address['user_address'], ])
            same_city_list = cur.fetchall()
            if not same_city_list:
                same_city_msg = 1
        else:
            same_city_msg = 2
        cur.execute("select user_imgurl from t_user where user_id = %s", [user_id, ])
        user_imgurl = cur.fetchone()
        if user_imgurl['user_imgurl'] == '':
            cur.execute("update t_user set user_imgurl = %s where user_id = %s",
                        ['../static/Images/default_hp.jpg', user_id])
            con.commit()
            cur.execute("select user_imgurl from t_user where user_id = %s", [user_id, ])
            user_imgurl = cur.fetchone()
    else:
        login_status = "未登录"
        user_imgurl = {}
        user_imgurl['user_imgurl'] = '../static/Images/default_hp.jpg'
    cur.execute(
        "select goods_id,goods_title,goods_price,goods_imgurl from t_goods where goods_category_id = %s and goods_state = %s limit 10",
        ['1', '0'])
    phone_list = cur.fetchall()
    cur.execute(
        "select goods_id,goods_title,goods_price,goods_imgurl from t_goods where goods_category_id = %s and goods_state = %s limit 10",
        ['2', '0'])
    computer_list = cur.fetchall()
    cur.execute(
        "select goods_id,goods_title,goods_price,goods_imgurl from t_goods where goods_category_id = %s and goods_state = %s limit 10",
        ['3', '0'])
    camera_list = cur.fetchall()
    # 收藏--------------------------
    # cur.execute("select * from t_user_collection where collection_user_id=%s", [user_id, ])
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s order by collection_record_id desc limit 0,5',
        [user_id, ])
    collection_list = cur.fetchall()
    cur.execute("select * from t_goods order by goods_id desc limit 5")
    newest_list = cur.fetchall()
    return render(request, 'homepage.html', locals())


def homepage_ajax(request):
    pass
    return render(request, 'homepage.html', {'goods_list': goods_list})


# 登录
def login(request):
    url = request.META.get('HTTP_REFERER', '/')
    # print(url, "返回地址")
    request.session["url"] = url
    href = request.GET.get('href')
    request.session['href'] = href
    username = request.session.get('username')
    if username:
        # print(username)
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
@mysql_required
def login_ajax(request):
    # 验证码判断
    login_code = {}
    if request.is_ajax():
        a = request.POST.get('response')
        # print(a, request.POST.get('hashkey'))
        result = CaptchaStore.objects.filter(response=request.POST.get('response'), hashkey=request.POST.get('hashkey'))
        if result:
            # print(result)
            login_code = {'status': 1}
            # print(login_code)
        else:
            login_code = {'status': 0}
            # print(login_code)
    # 获取表单信息
    username = request.POST.get("username")
    password = request.POST.get("password")
    cur.execute("select * from t_user where user_name=%s", [username, ])  # 全表搜索，待建立索引
    user_login = cur.fetchone()
    # print(user_login)
    if user_login is None:  # 判断用户名密码
        error = "login_error"
        return HttpResponse(json.dumps({"msg": error}))
    else:
        if login_code['status'] == 1:  # 判断验证码
            # print(login_code['status'])
            if password == user_login['user_password']:
                user_id = user_login['user_id']  # 判断用户名密码
                request.session['username'] = username
                request.session['user_id'] = user_id
                # href = request.session.get('href') #废弃跳转思路
                return_url = request.session["url"]
                # print(href)
                error = "login_ok"
                if return_url:
                    if return_url == "http://127.0.0.1:8000/register_ok/":
                        return_url = "/haima/"
                    elif return_url == "http://127.0.0.1:8000/register/":
                        return_url = "/haima/"
                    else:
                        pass
                else:
                    return_url = "/haima/"
                print(return_url, "enddddd")
                return HttpResponse(json.dumps({"msg": error, "href": return_url}))
            else:

                error = "login_error"  # 用户名或密码错误
                return HttpResponse(json.dumps({"msg": error}))
        else:
            error = "code_error"  # 验证码错误
            return HttpResponse(json.dumps({"msg": error}))


@mysql_required
def forget_password(request):
    username = request.POST.get("username")
    phone = request.POST.get("phone")
    cur.execute("select user_phone from t_user where user_name=%s", [username, ])
    check_phone = cur.fetchone()
    if check_phone:
        # print(check_phone)
        if check_phone["user_phone"] == phone:
            # print(phone, check_phone["user_phone"], type(phone), type(check_phone["user_phone"]))
            msg = "success"
            return HttpResponse(json.dumps({"msg": msg}))
        else:
            msg = "phone_error"
            # print(555)
            return HttpResponse(json.dumps({"msg": msg}))
    else:
        msg = "user_error"
        return HttpResponse(json.dumps({"msg": msg}))


@mysql_required
def forget_password_two(request):
    phone_code = request.POST.get("phone_code1")
    new_password = request.POST.get("new_password")
    phone = request.POST.get("phone")
    username = request.POST.get("username")
    # print(phone_code, new_password, phone)
    code = ""
    cur.execute("select user_phone from t_user where user_name=%s", [username, ])
    check_phone = cur.fetchone()
    if check_phone:
        if check_phone["user_phone"] == phone:
            try:
                code = sms.get(phone)
                code = code.decode("utf-8")
                if len(new_password) in range(6, 16):
                    if code == phone_code:
                        msg = "success"
                        # print(msg)
                        cur.execute("update t_user set user_password=%s where user_name=%s", [new_password, username])
                        con.commit()
                        return HttpResponse(json.dumps({"msg": msg}))
                    else:
                        msg = "code_error"
                        return HttpResponse(json.dumps({"msg": msg}))
                else:
                    msg = "password_error"
                    return HttpResponse(json.dumps({"msg": msg}))
            except:
                msg = "phone_error"
                return HttpResponse(json.dumps({"msg": msg}))
        else:
            msg = "phone_error"
            return HttpResponse(json.dumps({"msg": msg}))
    else:
        msg = "phone_error"
        return HttpResponse(json.dumps({"msg": msg}))


# 注册
def register(request):
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    code = CaptchaStore.generate_key()
    return render(request, 'register.html', locals())


# 注册条件判断
@mysql_required
def register_ajax(request):
    global user_error
    if request.method == "GET":
        # 获取用户名：
        username = request.GET.get("username")
        cur.execute("select * from t_user where user_name=%s", [username, ])  # 全表搜索，待建立索引
        user_list = cur.fetchall()
        if len(username) in range(6, 17):
            check_name = re.compile("[\u4e00-\u9fa5_a-zA-Z0-9]+$")
            check_ = check_name.match(username)
            if check_ is None:
                user_error = "用户名为6-16位的数字或英文,或汉子"
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
            # print(a, request.POST.get('hashkey'))
            result = CaptchaStore.objects.filter(response=request.POST.get('response'),
                                                 hashkey=request.POST.get('hashkey'))
            if result:
                # print(result)
                login_code = {'status': 1}
                # print(login_code)
            else:
                login_code = {'status': 0}
                # print(login_code)
        # 获取用户表单信息
        username = request.POST.get("username")
        password = request.POST.get("password")
        # email = request.POST.get("email")
        phone = request.POST.get("phone")
        code = request.POST.get("code")
        check_all = request.POST.get("check_all")
        print(phone)
        # print(username, password, phone, check_code, check_all, login_code)
        if login_code['status'] == 1:  # 图片验证码
            check_code = sms.get(phone)  # 获取手机验证码
            check_code = check_code.decode("utf-8")
            if check_code == code:  # 手机验证判断！
                if user_error == "" and check_all == 'true':
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
                    user_imgurl = '../static/Images/default_hp.jpg'
                    cur.execute(
                        "insert into t_user(user_name,user_password,user_phone,user_startdate,user_imgurl) values(%s,%s,%s,%s,%s)",
                        [username, password, phone, now_time, user_imgurl])
                    # print(username, email, phone, password)
                    con.commit()
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
    # print(code, phone)
    r.set(phone, code_, 60)
    return HttpResponse(code)


# 注册成功页面跳转
@mysql_required
def register_ok(request):
    return render(request, "register_ok.html")


# 搜索跳转到商品列表-------------------------------------------
@mysql_required
def goods_list(request):
    value_list = []
    start_list = []
    goods_lst = []
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        login_status = username

    if request.method == 'GET':
        question = request.GET.get('q')
        category = request.GET.get('c')
        if question:
            if question == '全新闲置':
                prompt = '以下商品为本平台最新上架商品，只显示最新的60条哟！'
                cur.execute("select * from t_goods order by goods_id desc limit 60")
                goods_lst = cur.fetchall()
            elif question == '同城交易':
                if request.session.get('user_id'):
                    user_id = request.session.get('user_id')
                    cur.execute("select user_address from t_user where user_id = %s", [user_id])
                    user_address_dict = cur.fetchone()
                    user_address = user_address_dict['user_address']
                    if user_address:
                        cur.execute("select * from t_goods where goods_address = %s", [user_address, ])
                        goods_lst = cur.fetchall()
                        if goods_lst:
                            prompt = '以下商品为' + user_address + '地区同城的商品，如需要查询其他地区请在用户中心中修改居住地'
                        else:
                            prompt = '抱歉没有找到您所在的' + user_address + '的商品'
                    else:
                        print(user_address)
                        prompt = '亲还没有设置居住地看不到同城商品哟！请在用户中心设置'
                else:
                    return redirect('/user_center/')
            else:
                question_word = jieba.cut(question)
                question_word = list(question_word)
                if len(question_word) != 1:
                    question_word.insert(0, question)
                for key in question_word:
                    if cut_words.smembers(key):
                        bvalue_list = list(cut_words.smembers(key))
                        for value in bvalue_list:
                            value = int(value.decode('utf-8'))
                            value_list.append(value)
                value_list = sorted(set(value_list), key=value_list.index)
                for goods_id in value_list:
                    sql = "select goods_id,goods_title,goods_imgurl,goods_price from t_goods where goods_id = %d and goods_state = 0" % goods_id
                    cur.execute(sql)
                    goods = cur.fetchone()
                    if goods:
                        goods_lst.append(goods)
                prompt = '已选条件： 所有与' + '"' + question + '"' + '相关的宝贝'
        if category == '1':
            cur.execute("select goods_id,goods_title,goods_imgurl,goods_price from t_goods where goods_category_id=%s",
                        [category, ])
            goods_lst = cur.fetchall()
            prompt = '已选类型：手机'
        if category == '2':
            cur.execute("select goods_id,goods_title,goods_imgurl,goods_price from t_goods where goods_category_id=%s",
                        [category, ])
            goods_lst = cur.fetchall()
            prompt = '已选类型：电脑'
        if category == '3':
            cur.execute("select goods_id,goods_title,goods_imgurl,goods_price from t_goods where goods_category_id=%s",
                        [category, ])
            goods_lst = cur.fetchall()
            prompt = '已选类型：相机'
        if category == '4':
            cur.execute("select goods_id,goods_title,goods_imgurl,goods_price from t_goods where goods_category_id=%s",
                        [category, ])
            goods_lst = cur.fetchall()
            prompt = '已选类型：电玩随身听'
        if category == '5':
            cur.execute(
                "select goods_id,goods_title,goods_imgurl,goods_price from t_goods where goods_category_id=%s",
                [category, ])
            goods_lst = cur.fetchall()
            prompt = '已选类型：其他'
        # 价格筛选
        if request.GET.get("price_low") and request.GET.get("price_high"):
            price_low = int(request.GET.get("price_low"))
            price_high = int(request.GET.get("price_high"))
            for goods in goods_lst:
                if price_low <= goods['goods_price'] <= price_high:
                    start_list.append(goods)
            goods_lst = start_list
        if request.GET.get("price_low") and request.GET.get("price_high") == "":
            price_low = int(request.GET.get("price_low"))
            for goods in goods_lst:
                if price_low <= goods['goods_price']:
                    start_list.append(goods)
            goods_lst = start_list
        if request.GET.get("price_high") and request.GET.get("price_low") == "":
            price_high = int(request.GET.get("price_high"))
            for goods in goods_lst:
                if goods['goods_price'] <= price_high:
                    start_list.append(goods)
            goods_lst = start_list

        sort_method = request.GET.get('sort_method')
        if sort_method == '1':
            goods_lst.sort(key=lambda x: x['goods_price'])
        if sort_method == '2':
            goods_lst.sort(key=lambda x: x['goods_price'], reverse=True)

        # 分页
        paginator = Paginator(goods_lst, 24)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'goods_list.html', locals())


# 用户中心——————————————————————
@mysql_required
@login_required
def user_center(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
        # 用户信息------------------
        cur.execute("select * from t_user where user_name=%s", [username, ])
        user_info = cur.fetchall()
        # 浏览记录--------------------------------
        cur.execute(
            'select * from t_goods right join t_user_browse on browse_goods_id=goods_id where browse_user_id=%s',
            [user_id, ])
        # cur.execute("select * from t_user_browse where browse_user_id=%s", [user_id, ])
        browse_list = cur.fetchall()
        paginator1 = Paginator(browse_list, 10)
        page1 = request.GET.get('page1')
        try:
            contacts1 = paginator1.page(page1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts1 = paginator1.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts1 = paginator1.page(paginator1.num_pages)
        # 这里需要返回他的购买和出售数量，从order_success 订单成功表去查
        cur.execute("select * from t_order_success where buy_user_id=%s", [user_id])
        dict1 = cur.fetchall()
        buy_count = len(dict1)
        cur.execute("select * from t_order_success where release_user_id=%s", [user_id])
        dict2 = cur.fetchall()
        sell_count = len(dict2)
        buy_conut = 0
        if dict1:
            buy_conut = len(dict1)
        # print(user_info, browse_list, 77777777777777777777)

        return render(request, 'user_center.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# 用户信誉-----------------------------------
@login_required
@mysql_required
def user_credit(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    user_credit_id = request.GET.get('user_credit_id')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    # 判断是否登陆-------------------------------
    if user_id:
        # 判断是否为本人进入
        # print(user_id, user_credit_id)
        if str(user_credit_id) == str(user_id):
            return redirect("/user_center/")
        else:
            # -用户信息
            # 发布商品--------------------------------------------------------------
            cur.execute("select * from t_user where user_id=%s ", [user_credit_id, ])
            user_info = cur.fetchall()
            # 计算天数------------------
            day_ = str(user_info[0]["user_startdate"])
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            d1 = datetime.datetime.strptime(day_, "%Y-%m-%d")
            d2 = datetime.datetime.strptime(now_time, "%Y-%m-%d")
            d3 = str(d2 - d1)
            if d3.split(" ")[0] == "0:00:00":
                day_count = 0
            else:
                day_count = d3.split(" ")[0]
            # -累计卖出-----------------
            # -收到的评价-------------------
            # -正在发布的商品----------------
            cur.execute("select * from t_goods where user_id=%s and goods_state=%s order by release_date desc",
                        [user_credit_id, 0])
            goods_list = cur.fetchall()
            goods = {}

            # lst = []
            # for item in goods_list:
            #     date = item.get('release_date')
            #     if item["release_date"] == date:
            #         lst.append(item)
            #     goods[date] = lst
            # goods_count = len(goods_list)
            for item in goods_list:
                date = item.get('release_date')
                goods[date] = ""

            for j in goods:
                lst = []
                count = 0
                for item in goods_list:
                    if j == item['release_date']:
                        count += 1
                        lst.append(item)
                # count_ = {"count": count}
                # lst.insert(0, count_)
                for i in lst:
                    i["count"] = str(count) + " 件商品"
                    break
                goods[j] = lst

            # print(goods)
            # cur.execute(
            #     'select * from t_order_success right join t_evaluation on order_id=evaluation_order_id where buy_user_id=%s ',
            #     [user_id, ])
            # buy_list = cur.fetchall()
            # cur.execute(
            #     'select * from t_order_success inner join t_evaluation on order_id= evaluation_order_id inner join t_goods on order_goods_id=goods_id '
            #     'where to_rid=%s order by second_message_id desc',
            #     [user_id, ])
            # # 卖家收到的评价---------------------------
            # cur.execute(
            #     'select * from t_order_success right join t_evaluation on order_id=evaluation_order_id where sell_user_id=%s ',
            #     [user_id, ])
            # sell_list = cur.fetchall()
            # 评价------------------------------------------------
            # 买家收到的评价-----------
            cur.execute(
                "select order_id from t_order_success where buy_user_id=%s and sell_eva_state=%s or release_user_id=%s and buy_eva_state=%s",
                [user_credit_id, 1, user_credit_id, 1])
            order_id = cur.fetchall()
            eva_list = []
            # print(user_id)
            count_order = len(order_id)
            for id in order_id:
                one = {}
                key = str(user_credit_id) + str(id["order_id"])
                a = get_eva.hgetall(key)
                # print(key, a)
                if a:
                    for i in a:
                        c = a[i].decode("utf-8")
                        i = i.decode("utf-8")
                        one[i] = c
                    eva_list.append(one)
                else:
                    eva_list.append("none")
            # print("评价内容", eva_list)
            count_eva = len(eva_list)
            return render(request, "user_credit.html", locals())
    else:
        return redirect('/login/')


# _____________________________________________________________-

# ******************************************************商品界面设置,返回商品详情***************************************
@mysql_required
def goods_detail(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    username = request.session.get('username')  # 获取买家用户名
    user_id = request.session.get('user_id')  # 获取买家ID
    goods_id = request.GET.get('goods')
    message_second_id = request.GET.get('message_second_id')
    if message_second_id:
        pass
    else:
        message_second_id = "q2"
    print(message_second_id, "锚标记！！")
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    # 商品收藏------------------------------------------
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s order by collection_record_id desc limit 0,4',
        [user_id, ])
    collection_list = cur.fetchall()
    # --------------------------------------------------
    # print(goods_id)  # 获取商品ID
    cur.execute("select * from t_goods where goods_id=%s", [goods_id, ])  # 获取商品表内容
    goods_list = cur.fetchall()  # 商品表内容
    print(goods_list)
    # print(username, user_id, goods_id, goods_list)
    seller_id = goods_list[0]['user_id']  # 获取卖家ID
    goods_state = goods_list[0]['goods_state']  # 商品状态
    # 获取商品图片
    img_list = []
    for item in img.lrange(goods_id, 0, 4):
        item = item.decode("utf-8")
        img_list.append(item)
    # print("商品图片地址", img_list)

    # 判断是否为发布人进去页面---------------------
    if user_id == seller_id:
        cur.execute("SELECT count(*) FROM t_user_collection WHERE collection_goods_id = %s;", [goods_id, ])
        collection_count = str(cur.fetchone()['count(*)']) + "人收藏"
        seller_in = "seller_in"
    else:
        seller_in = "no_seller"
        collection_count = ""
    # =-----卖家信息————————————————
    cur.execute("select * from t_user where user_id=%s", [seller_id, ])  # 获取卖家信息
    seller_info = cur.fetchall()
    cur.execute("select count(*) from t_order_success where release_user_id=%s", [seller_id])
    count_sell = cur.fetchone()["count(*)"]
    print(count_sell)
    # cur.execute("select count(*) from test where id=1")成交记录
    # ------------------------------------
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 记录当前时间
    # print(username, user_id, goods_id, seller_id, now_time)
    goods_desc = goods_list[0]['goods_desc']  # 商品详细介绍
    cur.execute('select * from t_user right join t_message on user_id = message_user_id')
    message_list = cur.fetchall()  # 留言
    # ++++++++++++++++++++++++商品留言处理++++++++++++++++++++++++++++++
    cur.execute("select * from t_second_message right join t_user on child_user_id=user_id where  second_goods_id=%s",
                [goods_id, ])
    b = cur.fetchall()
    # print('weeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', b, 'weeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    cur.execute('select * from t_message right join t_user on message_user_id=user_id where message_goods_id=%s ',
                [goods_id, ])
    a = cur.fetchall()
    c_comment_dict = {}
    for d in b:
        id = d.get('second_message_id')
        c_comment_dict[id] = d
    p_comment_dict = {}
    # print(c_comment_dict)
    for d in a:
        id = d.get('message_id')
        p_comment_dict[id] = d
    # lst = {}
    # print(4444444444444444, p_comment_dict)
    for i in p_comment_dict:
        lst = []
        for j in c_comment_dict:
            if c_comment_dict[j]:
                # print(c_comment_dict[j]['parent_message_id'], i, 4444444444444444444444444444444444, type(i))
                if p_comment_dict[i]['message_user_id'] == c_comment_dict[j]['parent_user_id'] and i == \
                        int(c_comment_dict[j]['parent_message_id']):
                    lst.append(c_comment_dict[j])
                    c_comment_dict[j] = ''
        p_comment_dict[i]['child_message'] = lst
    # 按钮列表
    # print("评论", p_comment_dict)
    button_list = []
    for i in p_comment_dict:
        button_list.append(int(i))
    # print(p_comment_dict)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    if username:  # 登录后才记录，浏览记录
        key = goods_id
        goods_browse.lpush(key, user_id)
        key = goods_id
        cur.execute("select user_imgurl from t_user where user_id=%s", [user_id])
        user_imgurl = cur.fetchone()["user_imgurl"]
        # print("图片", user_imgurl)
        login_status = username
        cur.execute("select * from t_user_browse where browse_user_id=%s and browse_goods_id=%s", [user_id, goods_id])
        browse = cur.fetchone()
        # print(browse, "检查")
        if browse is None:
            count = goods_list[0]['goods_browse_count']
            count += 1
            # 更新商品浏览次数
            cur.execute("update t_goods set goods_browse_count=%s where goods_id=%s", [count, goods_id])
            # print(count, goods_id, "商品浏览记录")
        # 用户浏览记录
        if seller_id != user_id:
            cur.execute("select * from t_user_browse where browse_user_id=%s and browse_goods_id=%s",
                        [user_id, goods_id])
            user_browse = cur.fetchone()
            if user_browse:
                cur.execute("update t_user_browse set browse_date=%s where browse_goods_id=%s and browse_user_id=%s",
                            [now_time, goods_id, user_id])
            else:
                cur.execute("insert into t_user_browse(browse_user_id,browse_date,browse_goods_id) value(%s,%s,%s) ",
                            [user_id, now_time, goods_id])
        con.commit()
    else:
        login_status = '未登录'
        user_imgurl = '../static/Images/default_hp.jpg'
    href = 1
    cur.close()
    return render(request, "detail.html", locals())


# 测试用---------------------------------
def text_message(request):
    cur.execute("select * from t_second_message right join t_user on child_user_id=user_id where  second_goods_id=%s",
                ['2', ])
    b = cur.fetchall()
    cur.execute('select * from t_message right join t_user on message_user_id=user_id where message_goods_id=%s ',
                ['2', ])
    a = cur.fetchall()
    # print(a)
    # print(b)
    c_comment_dict = {}
    for d in b:
        id = d.get('second_message_id')
        c_comment_dict[id] = d
    p_comment_dict = {}

    for d in a:
        id = d.get('message_user_id')
        p_comment_dict[id] = d
    # lst = {}
    for i in p_comment_dict:
        lst = []
        for j in c_comment_dict:
            if p_comment_dict[i]['message_user_id'] == c_comment_dict[j]['parent_user_id']:
                lst.append(c_comment_dict[j])
        p_comment_dict[i]['child_message'] = lst

    return render(request, "test2.html", locals())


def test_ajax(request):
    username = request.session.get('username')
    # print(username, 4444)
    child_id = request.POST.get('child_id')
    cur.execute("select * from t_user where user_id=%s", [child_id, ])
    child_user = cur.fetchone()
    # print(child_user['user_name'], 45555)
    message = request.POST.get('message')
    if username:
        # print(message)
        # cur.execute()   #加入数据库
        # 评论拼接
        tt = """            
                    <div style="margin-left: 100px">
                        <img src="{0}" alt="" height="50" width="50">
                        {1}
                        <p>{2}<input type="text" id="message"><input type="button" value="回复"
                                                                                         id="btn_message"></p>
                        <p><input type="text" id="c_message" value="" hidden></p>
                  
                </div>
            """
        tt = tt.format(child_user['user_imgurl'], child_user['user_name'], message)

        return HttpResponse(json.dumps({"msg": tt}))
    else:
        href = request.session.get('username')
        r_error = 'need_login'
        href = '/login/?href=/test/%23abc'  # get方法#号
        return HttpResponse(json.dumps({"msg": r_error, "href": href}))


# 回复处理，留言板
@mysql_required
@login_required
def review_ajax(request):
    # 判断登陆状态----------------
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ------接受值———————————
    child_review = request.POST.get('child_review')
    rp_user_id = request.POST.get('reply_id')
    message_id = request.POST.get('message_id')
    # parent_id = request.POST.get("parent_id")
    # goods_id = request.POST.get("goods_id")
    print(" # ------接受值———————————")
    print(child_review, rp_user_id, message_id, username, user_id)
    cur.execute("select * from t_message where message_id=%s", [message_id, ])
    message_id_list = cur.fetchone()
    print(message_id_list)
    message_id = message_id_list["message_id"]
    parent_id = message_id_list["message_user_id"]
    goods_id = message_id_list["message_goods_id"]
    if user_id:
        login_state = username
        # ------获取用户信息———————————
        cur.execute("select * from t_user where user_id=%s", [user_id, ])
        child_user = cur.fetchone()
        # 提取要回复人的名字
        # child_name_ = child_review
        rule1 = r'回复(.*?):'
        child_name = re.findall(rule1, child_review)
        print(child_name, "要回复人")
        print(rp_user_id, child_review, "回复内容，ID")
        # 判断@名字是否合法：
        cur.execute("select * from t_message where message_id=%s", [message_id, ])
        reply_id__ = cur.fetchone()
        cur.execute("select * from t_second_message where second_message_id=%s", [rp_user_id, ])
        check_child_name_ = cur.fetchone()
        if check_child_name_:
            reply_id1 = check_child_name_["child_user_id"]
            cur.execute("select * from t_user where user_id=%s", [reply_id1, ])
            check_child_name_2 = cur.fetchone()
            # check_child_name = check_child_name_['user_name']
            if child_name and check_child_name_2 and check_child_name_2:
                print("判断用户名", child_name[0], check_child_name_2['user_name'])
                if check_child_name_2['user_name'] == child_name[0]:
                    rule2 = r':(.*)'
                    print('ture')
                    send_review = "@" + child_name[0] + ':  ' + \
                                  re.findall(rule2, child_review)[0]
                    reply_id = reply_id1
                else:
                    send_review = child_review
                    reply_id = reply_id__["message_user_id"]
            else:
                send_review = child_review
                # cur.execute("select * from t_message where message_id=%s", [message_id, ])
                # reply_id__ = cur.fetchone()
                reply_id = reply_id__["message_user_id"]
        else:
            reply_id = reply_id__["message_user_id"]
            send_review = child_review

        # 储存数据
        user_id_ = str(user_id)
        print(send_review, goods_id, now_time, user_id, rp_user_id)
        # print(type, type(send_review), type(goods_id), type(now_time), type(user_id_), type(rp_user_id))
        cur.execute(
            "insert into t_second_message(parent_user_id,second_desc,second_goods_id,second_date,child_user_id,to_rid,parent_message_id) value(%s,%s,%s,%s,%s,%s,%s)",
            [parent_id, send_review, goods_id, now_time, user_id_, reply_id, message_id])
        second_message_id = cur.lastrowid
        con.commit()
        # cur.execute("select * from t_second_message where second_message_id=%s", [second_message_id, ])
        # second_message_lst = cur.fetchone()
        rr = """<dl>
                                    <dd style="margin-left: 75px;height: 50px;">
                                        <input type="text" id="child_user_id" value="{0}" hidden>
                                        <a  href="/user_center/"><img src="{1}" alt="" height="40" width="40"></a>
                                        <div style="margin-left: 45px;position: relative;top: -50px;"><a
                                                href="/user_center/" style="color: #2d64b3"
                                                class="c_name_{2}">{3}</a>:
                                            <a  href="/user_center/" style="color: #a3a3a3"><span style="color: #333333;font-size: 14px">{4}</span></a>
                                            <div><a  href="/user_center/"><span style="color: #a3a3a3">{5}</span></a>
                                                <input id="review" class="c_review_{6}"
                                                       type="button" value="回复"
                                                       onclick="c_review({7})" hidden>
                                            </div>
                                        </div>
                                    </dd>
                                   </dl>
                               """
        rr = rr.format(child_user["user_id"], child_user["user_imgurl"], second_message_id, username, send_review,
                       now_time,
                       second_message_id, second_message_id)
        return HttpResponse(json.dumps({"msg": rr}))
    else:
        login_state = "未登录"
        r_error = 'need_login'
        href = '/login/?href=/goods_detail/?goods=' + str(goods_id)  # get方法#号
        return HttpResponse(json.dumps({"msg": r_error, "href": href}))


@mysql_required
def lea_message(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if username:
        Published = request.POST.get("Published")
        goods_id = request.POST.get("goods_id")
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("商品留言", user_id, Published, goods_id, now_time)
        cur.execute(
            "insert into t_message(message_user_id,message_desc,message_goods_id,message_date) values(%s,%s,%s,%s)",
            [user_id, Published, goods_id, now_time])
        con.commit()
        url = "success"
        value = "goods_message"
        cur.execute("select user_id from t_goods where goods_id=%s", [goods_id, ])
        check_name_ = cur.fetchone()
        if check_name_["user_id"] == user_id:
            pass
        else:
            message_push.lpush(check_name_["user_id"], value)
        return HttpResponse(json.dumps({"href": url}))

    else:
        p_error = 'need_login'
        url = '/login'
        return HttpResponse(json.dumps({"msg": p_error, "href": url}))


# 商品收藏页面++++++++++++++++++++++++++++++++++++++++
@mysql_required
def collection(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    goods_id = request.POST.get("goods_id")
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("select * from t_user_collection where collection_user_id=%s and collection_goods_id=%s",
                [user_id, str(goods_id)])
    collection_check_ = cur.fetchone()
    print("商品收藏", collection_check_)
    if username:
        if collection_check_:
            msg = "您已收藏过改商品"
        else:
            msg = "收藏成功"
            cur.execute(
                "insert into t_user_collection(collection_date,collection_goods_id,collection_user_id) values(%s,%s,%s)",
                [now_time, goods_id, user_id])
            con.commit()
        return HttpResponse(json.dumps({"msg": msg}))
    else:
        msg = "need_login"
        href = '/login'
        return HttpResponse(json.dumps({"msg": msg, "href": href}))


# 商品上架，下架
@mysql_required
def lower_goods(request):
    goods_id = request.POST.get("goods_id")
    print(goods_id, 888888888888888888888)
    state = request.POST.get("state")
    if state == "lower":
        cur.execute("update t_goods set goods_state=%s where goods_id=%s", ['2', goods_id])
        msg = "下架成功"
        # msg = "下架失败"
        con.commit()
        href = '/goods_detail/?goods=' + str(goods_id)
    else:
        cur.execute("update t_goods set goods_state=%s where goods_id=%s", ['0', goods_id])
        msg = "上架成功"
        con.commit()
        href = '/goods_detail/?goods=' + str(goods_id)
        print(href)

    return HttpResponse(json.dumps({"msg": msg, "href": href}))


def goods_detail_ajax(request):
    pass


# 发布商品
# def publish(request):
#     user_name = request.session.get('username')
#     if request.method == 'POST':
#         price = int(request.POST.get('price_hid').replace('¥', ''))
#     return render(request, 'publish.html', locals())

@login_required
@mysql_required
def goods_republish(request):
    user_name = request.session.get('username')
    goods_id = request.GET.get("goods_id")
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username

    if goods_id:
        cur.execute("select * from t_goods where goods_id=%s", [goods_id, ])
        goods_list = cur.fetchone()

        img_list1 = []
        for item in img.lrange(goods_id, 0, 4):
            img_list1.append(item.decode("utf-8"))
        print("图片", img_list1)
        a = 0
        c = ""
        for i in img_list1:
            rr = """<div id="js-uploadList_fuck{0}" class="img-box">
    <div class="img-border"><span class="js-upload_delete icon-delete_fill red" data-index="{1}"></span>
        <img src="{2}">
    </div>
</div>"""
            b = rr.format(a, a, i)
            a += 1
            c += b
        print(c)
        return render(request, "publish.html", locals())
    else:
        return render(request, "publish.html", locals())


@mysql_required
@login_required
def pub_success(request):
    goods_id = request.POST.get('goods_id')
    user_id = request.session.get('user_id')
    if goods_id:
        title = request.POST.get('title')
        category = request.POST.get('type')
        price = float(request.POST.get('price'))
        postage = request.POST.get('postage')
        desc = request.POST.get('desc')
        appearance = request.POST.get('appearance')
        filelist = json.loads(request.POST.get('filelist'))
        print(title, category, price, postage, desc, appearance)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if filelist:
            img.delete(goods_id)
            for file in filelist:
                img.rpush(goods_id, "http://files.g1.xmgc360.com/" + file)
            goods_img = img.lindex(goods_id, 0)
            goods_img = goods_img.decode("utf-8")
            cur.execute(
                "update t_goods set goods_title=%s,goods_category_id=%s,goods_price=%s,goods_postage=%s,goods_desc=%s,goods_appearance=%s,release_date=%s,goods_imgurl=%s where goods_id=%s",
                [title, category, price, postage, desc, appearance, now_time, goods_img, goods_id])
        else:
            cur.execute(
                "update t_goods set goods_title=%s,goods_category_id=%s,goods_price=%s,goods_postage=%s,goods_desc=%s,goods_appearance=%s,release_date=%s where goods_id=%s",
                [title, category, price, postage, desc, appearance, goods_id, now_time])
        con.commit()
        href = '/publish_ok/?goods_id=' + str(goods_id)
        return HttpResponseRedirect(href)
    else:
        title = request.POST.get('title')
        category = request.POST.get('type')
        price = float(request.POST.get('price'))
        postage = request.POST.get('postage')
        desc = request.POST.get('desc')
        appearance = request.POST.get('appearance')
        filelist = json.loads(request.POST.get('filelist'))
        cur.execute("select user_address from t_user where user_id =%s", [user_id, ])
        user_address = cur.fetchone()
        if user_address:
            address = user_address["user_address"]
        else:
            address = '江苏苏州 吴江区'
        appearance = '4'
        if desc:
            pass
        else:
            desc = '该卖家比较懒，还没有商品描述'
        for i in filelist:
            print(i)
        url = "http://files.g1.xmgc360.com/" + filelist[0]
        sql = "INSERT INTO t_goods(`user_id`,`release_date`,`goods_title`,`goods_desc`,`goods_price`,`goods_category_id`,`goods_imgurl`,`goods_address`,`goods_appearance`) \
                                                                           VALUES ('%s','%s','%s','%s','%f','%s','%s','%s','%s')" % \
              (
                  str(user_id), loc_time, title, desc, price, category, url, address, appearance)
        cur.execute(sql)
        last_id = cur.lastrowid
        options = {}
        options["brief"] = "{\"id\":\"" + str(last_id) + "\", \"url\":\"" + url + "\"}"
        print(options["brief"])
        print(client.productAddUrl(url, options))
        for file in filelist:
            img.rpush(last_id, "http://files.g1.xmgc360.com/" + file)
        con.commit()
        print(title, category, price, postage, filelist)
        href = '/publish_ok/?goods_id=' + str(last_id)
        return HttpResponseRedirect(href)


def publish_ok(request):
    goods_id = request.GET.get("goods_id")
    print(goods_id, 646544644445)
    if goods_id:
        href = "/goods_detail/?goods=" + str(goods_id)
    else:
        href = "/haima/"
    return render(request, "publish_ok.html", locals())


# 估价
def assess(request):
    user_name = request.session.get('username')
    return render(request, 'assess.html', locals())


# 估价ajax
def assess_ajax(request):
    assess_list = []
    brand = request.POST.get('brand')
    model = request.POST.get('model')
    brand, model = phone_model.Phone_model(brand, model)
    assess_list.append(brand)
    assess_list.append(model)
    configuration = request.POST.get('configuration')
    IS, volume = configuration.split('+')
    IS = int(re.findall(r"\d+\.?\d*", IS)[0])
    volume = int(re.findall(r"\d+\.?\d*", volume)[0])
    assess_list.append(IS)
    assess_list.append(volume)
    color = int(request.POST.get('color'))
    assess_list.append(color)
    GT = int(request.POST.get('GT'))
    assess_list.append(GT)
    face = int(request.POST.get('face'))
    assess_list.append(face)
    maintain = int(request.POST.get('maintain'))
    assess_list.append(maintain)
    UT = int(request.POST.get('UT'))
    assess_list.append(UT)
    price = AI_assess.assess_price(assess_list)[0]
    # print(assess_list)
    # print(price)
    if price < 0:
        price = -price
    price = '¥' + str(int(price))
    time.sleep(1)
    return HttpResponse(json.dumps({"price": price}))


# 拍卖首页
def auction_index(request):
    id = request.session.get('user_id')
    print(id)
    list1 = []
    if id:
        goods_list = []
        cur.execute('select user_name from t_user where user_id=%s', [id])
        username = cur.fetchone()
        cur.execute("select auction_goods_id from t_auction_goods")
        goods_dict = cur.fetchall()
        # 先将需要在首页展示的拍卖商品的id全部拿出来存进一个列表里
        for i in goods_dict:
            goods_list.append(i["auction_goods_id"])
        # 对这个需要展示的商品id进行遍历，将他需要展示的数据全部一条一条的拿出来
        for goods_id in goods_list:
            dict1 = {}
            cur.execute("select * from t_auction_goods where auction_goods_id=%s ", [goods_id])
            goods_messge = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_messge
            dict1["attribute"] = goods_auction_message
            list1.append(dict1)

        return render(request, "auction_index.html", locals())
    else:
        return HttpResponseRedirect('/login/')


# ********************************************************************普通商品购买***************************************
def goods_confirm_buy(request):
    error = ""
    price = request.POST.get("price")
    user_id = request.session.get("user_id")
    pay_password = request.POST.get("pay_password")
    goods_id = request.POST.get("goods_id")
    cur.execute("select user_pay_password,user_money from t_user where user_id=%s", [user_id])
    user_message = cur.fetchone()
    user_pay_password = user_message["user_pay_password"]
    user_money = user_message["user_money"]
    print(price, user_money)
    if user_pay_password:
        if len(pay_password) < 6:
            error = "pay_password_length_error"
            return HttpResponse(json.dumps({"msg": error}))
        elif int(pay_password) != int(user_pay_password):
            error = "pay_password_error"
            return HttpResponse(json.dumps({"msg": error}))
        elif float(user_money) < float(price):
            error = "money_less_error"
            return HttpResponse(json.dumps({"msg": error}))
        else:
            # 购买完成，更新数据库和生成订单扣款等
            try:
                # 先扣除购买者的钱
                user_money = float(user_money) - float(price)
                cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, user_id])
                print("扣钱成功")
                # 生成商品订单
                cur.execute("select user_id from t_goods where goods_id=%s", [goods_id])
                release_user_id = cur.fetchone()["user_id"]
                date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                cur.execute(
                    "insert into t_order(release_user_id,buy_user_id,order_date,order_goods_id) values (%s,%s,%s,%s)",
                    [str(release_user_id), str(user_id), date, str(goods_id)])
                print("生成订单成功")
                cur.execute("update t_goods set goods_state=%s where goods_id=%s", ["1", goods_id])
                print("更新商品状态成功")
                con.commit()
                error = "pay_ok"
                return HttpResponse(json.dumps({"msg": error}))

            except Exception as e:
                print(e)
    else:
        error = "no_pay_password"
        return HttpResponse(json.dumps({"msg": error}))


# 用户输入支付密码扣款完成

def buy_goods_ok(request):
    return render(request, "buy_goods_ok.html")


# 我出售的
@login_required
@mysql_required
def my_sale(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    # 发布中的商品------------------------------
    cur.execute(
        'select * from t_goods  where user_id=%s and goods_state=%s order by release_date desc',
        [user_id, 0])
    p_sale_list = cur.fetchall()
    paginator1 = Paginator(p_sale_list, 3)
    page1 = request.GET.get('page1')
    try:
        contacts1 = paginator1.page(page1)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts1 = paginator1.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts1 = paginator1.page(paginator1.num_pages)
    # 交易中的商品---------------------------------
    cur.execute(
        'select * from t_order right join t_goods on order_goods_id=goods_id where release_user_id=%s ',
        [user_id, ])
    transaction_list = cur.fetchall()
    print(transaction_list)
    paginator2 = Paginator(transaction_list, 2)
    page2 = request.GET.get('page2')
    try:
        contacts2 = paginator2.page(page2)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts2 = paginator2.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts2 = paginator2.page(paginator2.num_pages)

    return render(request, 'my_sale.html', locals())

#
# def refund_ajax(request):
#     user_id = request.session.get('user_id')
#     order_id = request.POST.get("order_id")
#     reason = request.POST.get("reason")
#     refund_user_id = request.POST.get("refund_user_id")
#     print("退款", order_id, reason, refund_user_id)
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     desc = "你收到一条订单为" + str(order_id) + "的退款消息！"
#     cur.execute("update t_order set refund_state=%s,refund_reason=%s where order_id=%s", [1, reason, order_id])
#     cur.execute(
#         "insert into t_system_message (push_message_id,get_message_id,system_desc,system_date) value(%s,%s,%s,%s)",
#         [user_id, refund_user_id, desc, now_time])
#     con.commit()
#     message_push.lpush(refund_user_id, "system")
#     msg = "success"
#     return HttpResponse(json.dumps({"msg": msg}))


def order_mark(request):
    order_id = request.POST.get("order_id")
    user_id = request.session.get('user_id')
    order_mark = request.POST.get("order_mark")
    if order_mark:
        print("提交物流信息", order_id, order_mark)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            cur.execute("update t_order set state=%s,order_mark=%s where order_id=%s", [1, order_mark, order_id])
            con.commit()
            msg = "success"
            cur.execute("select buy_user_id from t_order where order_id=%s", [order_id, ])
            user_id_ = cur.fetchone()
            user_id1 = user_id_["buy_user_id"]
            value = "system"
            message_push.lpush(user_id1, value)
            desc = "你购买的订单号为" + str(order_id) + "买家已经发货"
            cur.execute(
                "insert into t_system_message (push_message_id,get_message_id,system_desc,system_date) value(%s,%s,%s,%s)",
                [user_id, user_id1, desc, now_time])
        except:
            msg = "fail"
    else:
        msg="fail"
    return HttpResponse(json.dumps({"msg": msg}))


# my_sale 户中心商品下架——ajax: 待修改
def user_lower_goods(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    goods_id = request.POST.get("goods_id")
    user_id = request.session.get('user_id')
    page_count_c = request.POST.get("page_count_c")
    print(page_count_c, "传过来的页数")
    print(goods_id)
    if page_count_c != 'None' and page_count_c != 0:
        page_count = int(page_count_c)
    else:
        page_count = 1
    # 下架商品-------------------
    cur.execute("update t_goods set goods_state=%s where goods_id=%s", ['2', goods_id])
    con.commit()
    # ---页面拼接---------------------------
    cur.execute("select * from t_goods where user_id=%s and goods_state=%s order by release_date desc",
                [user_id, 0])
    goods_list = cur.fetchall()
    print(len(goods_list) % 3, "秋雨", len(goods_list))
    if len(goods_list) % 3 == '0':
        msg = "flash"
        href = "/my_sale/?page1=" + str(page_count - 1)
        print(href)
        return HttpResponse(json.dumps({"msg": msg, "href": href}))
    else:
        try:
            print(3 * page_count, "页数+++++")
            goods_list_ = goods_list[3 * page_count - 1]
            goods_id_ = goods_list_["goods_id"]
            release_date = goods_list_["release_date"]
            goods_imgurl = goods_list_["goods_imgurl"]
            goods_title = goods_list_['goods_title']
            goods_browse_count = goods_list_["goods_browse_count"]
            goods_price = goods_list_["goods_price"]
            dd = """  <ul class="order_list_th w978 clearfix" id="goods_{0}">
                            <input type="text" value="{1}" hidden id="goods_id_{2}">
                            <li class="col01" id="date">{3}</li>
                        </ul>
    
                        <table class="order_list_table w980" id="goods1_{4}">
                            <tbody>
                            <tr>
                                <td width="55%">
                                    <ul class="order_goods_list clearfix">
                                        <li class="col01"><a href="/goods_detail/?goods={5}"><img
                                                src="{6}"></a></li>
                                        <li class="col02"><a
                                                href="/goods_detail/?goods={7}"
                                                style="color: dodgerblue">{8}</a><em
                                                style="color: red">{9}元</em>
                                        </li>
                                        <li class="col04">{10}人浏览</li>
                                    </ul>
                                </td>
                                <td width="15%"><input type="button" class="lower1_btn lower_{11} oper_btn"
                                           onclick="lower({12})" value="下架"></td>
                                <td width="15%"><a href="" class="oper_btn">修改</a></td>
                            </tr>
                            </tbody>
                        </table>"""
            rr = dd.format(goods_id_, goods_id_, goods_id_, release_date, goods_id_, goods_id_, goods_imgurl,
                           goods_id_,
                           goods_title, goods_price,
                           goods_browse_count, goods_id, goods_id_)
            msg = "append"
            html = rr
        except:
            msg = "append"
            html = ""
        return HttpResponse(json.dumps({"msg": msg, "html": html}))
        # except:
        #     msg = "flash"
        #     href = "/my_sale/"
        #     return HttpResponse(json.dumps({"msg": msg, "href": href}))
        # msg = "error"
        # href = "/my_sale/"
        # return HttpResponse(json.dumps({"msg": msg, "href": href}))


# 我的出售，上下架页面
@login_required
@mysql_required
def my_sale_lower(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    if request.is_ajax():
        goods_id = request.POST.get("goods_id")
        try:
            cur.execute("update t_goods set goods_state=%s where goods_id=%s", ['0', goods_id])
            msg = "上架成功"
            con.commit()
            msg = "success"
        except:
            msg = "fail"
        href = "/my_sale_lower/"
        return HttpResponse(json.dumps({"msg": msg, "href": href}))
    else:
        cur.execute(
            'select * from t_goods  where user_id=%s and goods_state=%s order by goods_id desc',
            [user_id, 2])
        p_sale_list = cur.fetchall()
        if len(p_sale_list) > 5:
            paginator1 = Paginator(p_sale_list, 5)
            page1 = request.GET.get('page1')
            try:
                contacts1 = paginator1.page(page1)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts1 = paginator1.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                contacts1 = paginator1.page(paginator1.num_pages)
        else:
            contacts1 = p_sale_list
        return render(request, "my_sale_lower.html", locals())


# 出售完成页面
@login_required
def my_sale_complete(request):
    if request.is_ajax():
        print(111111)
    else:
        user_id = request.session.get('user_id')
        username = request.session.get('username')
        username = request.session.get('username')
        if username:
            message_check1 = message_push.lrange(user_id, 0, 1)
            message_list_push = []
            message_list_push1 = message_push.lrange(user_id, 0, 3)
            for item in message_list_push1:
                message_list_push.append(item.decode("utf-8"))
            print(message_list_push)
            if message_check1:
                message_check = "../static/Images/new02.gif"
            else:
                message_check = "../static/Images/message.png"
            print(message_check, "消息推送")
            login_status = username
        cur.execute(
            'select * from t_order_success right join t_goods on order_goods_id=goods_id where release_user_id=%s ',
            [user_id, ])
        order_list = cur.fetchall()

        print(order_list)
        paginator1 = Paginator(order_list, 4)
        page1 = request.GET.get('page1')
        try:
            contacts1 = paginator1.page(page1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts1 = paginator1.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts1 = paginator1.page(paginator1.num_pages)

    return render(request, "my_sale_complete.html", locals())


@mysql_required
@login_required
def my_buy(request):
    username = request.session.get('username')
    user_id = request.session.get("user_id")
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    else:
        login_status = "未登录"
    cur.execute("select * from t_order right join t_goods on order_goods_id=goods_id where buy_user_id=%s", [user_id])
    order_list = cur.fetchall()
    print(order_list)
    return render(request, 'my_buy.html', locals())


@mysql_required
@login_required
def tinxinfahuo(request):
    user_id = request.session.get("user_id")
    order_id = request.POST.get("order_id")
    cur.execute("select * from t_order where order_id=%s", [order_id, ])
    order_list = cur.fetchone()
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    desc = "收到单号为" + str(order_id) + "的发货请求"
    cur.execute(
        "insert into t_system_message (push_message_id,get_message_id,system_desc,system_date) value(%s,%s,%s,%s)",
        [user_id, order_list["release_user_id"], desc, now_time])
    msg = "success"
    con.commit()
    message_push.lpush(order_list["release_user_id"], "system")
    return HttpResponse(json.dumps({"msg": msg}))


@mysql_required
@login_required
def my_buy_complete(request):
    username = request.session.get('username')
    user_id = request.session.get("user_id")
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    else:
        login_status = "未登录"
    cur.execute("select * from t_order_success right join t_goods on order_goods_id=goods_id where buy_user_id=%s",
                [user_id, ])
    order_success_list = cur.fetchall()
    return render(request, "my_buy_complete.html", locals())


# 我的收藏
@login_required
@mysql_required
def my_collection(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    username = request.session.get('username')  # 获取买家用户名
    user_id = request.session.get('user_id')  # 获取买家ID
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    if request.is_ajax():
        page_ = request.POST.get("page_")
        goods_id = request.POST.get("goods_id")
        if page_ != 'None':
            page_count = int(page_)
        else:
            page_count = 1
        cur.execute("delete from t_user_collection where collection_user_id=%s and collection_goods_id=%s",
                    [user_id, goods_id])
        con.commit()
        cur.execute(
            'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s order by collection_record_id',
            [user_id, ])
        collection_list = cur.fetchall()
        if page_ != 'None':
            page_count = int(page_)
        else:
            page_count = 1
        if len(collection_list) % 5 == 0:
            href = "/my_collection/?page=" + str(page_count - 1)
            msg = "flash"
            print("收藏页面链接跳转", href)
            return HttpResponse(json.dumps({"msg": msg, "href": href}))
        else:
            try:
                goods_list = collection_list[5 * page_count - 1]
                rr = """ <li id="goods_{0}">
                                    <a href="/goods_detail/?goods={1}"><img src="{2}"
                                                                                             style="position: relative;z-index: 1"></a>
                                    <h4><a href="/goods_detail/?goods={3}">{4}</a></h4>
                                    <div class="operate">
                                        <span class="prize">{5}</span>
                                        <p class="unit fl">{6}</p>
                                        <button class="del_col fl" title="删除收藏" onclick="delete_({7})"><img
                                                src="../static/Images/delete_goods.jpg"
                                                style="width: 15px;height: 15px;margin: 0"
                                                alt="">
                                        </button>
                                    </div>
                                </li>"""
                state = 0
                if goods_list["goods_state"] == '0':
                    state = goods_list["goods_price"]
                elif goods_list["goods_state"] == "1":
                    state = "已出售"
                elif goods_list["goods_state"] == "2":
                    state = "已下架"
                a_append = rr.format(goods_list["goods_id"], goods_list["goods_id"], goods_list["goods_imgurl"],
                                     goods_list["goods_id"], goods_list["goods_title"], state,
                                     goods_list["collection_date"],
                                     goods_list["goods_id"])
                print(a_append)
                msg = "success"
            except:
                msg = "success"
                a_append = ""
            return HttpResponse(json.dumps({"msg": msg, "html": a_append}))

    else:
        goods_id = request.GET.get('goods')
        # 商品收藏------------------------------------------
        cur.execute(
            'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s order by collection_record_id',
            [user_id, ])
        collection_list = cur.fetchall()
        paginator = Paginator(collection_list, 5)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        # -----------------------------------
        r_goods_list = []
        recommend_goods = user_recommend.lrange(user_id, 0, -1)
        for r_goods_id in recommend_goods:
            r_goods_id = r_goods_id.decode('utf-8')
            cur.execute("select goods_id,goods_imgurl,goods_title,goods_price from t_goods where goods_id = %s",
                        [r_goods_id, ])
            r_goods = cur.fetchone()
            r_goods_list.append(r_goods)
        return render(request, 'my_collection.html', locals())


# 评价
@root_request
@mysql_required
def evaluate(request):
    username = request.session.get('username')  # 获取买家用户名
    user_id = request.session.get('user_id')  # 获取买家ID
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    goods_id = request.GET.get('goods_id')
    customer = request.GET.get("customer")
    print("evaluate", "------", username, user_id, goods_id)
    # 商品收藏------------------------------------------
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s order by collection_record_id desc limit 0,4',
        [user_id, ])
    collection_list = cur.fetchall()
    # --------------------------------------------------
    print(goods_id)  # 获取商品ID
    cur.execute("select * from t_goods where goods_id=%s", [goods_id, ])  # 获取商品表内容
    goods_list = cur.fetchall()  # 商品表内容
    print(username, user_id, goods_id, goods_list)
    seller_id = goods_list[0]['user_id']  # 获取卖家ID
    goods_state = goods_list[0]['goods_state']  # 商品状态
    goods_desc = goods_list[0]["goods_desc"]
    # 获取商品图片
    img_list = []
    for item in img.lrange(goods_id, 0, 4):
        item = item.decode("utf-8")
        img_list.append(item)
    print("商品图片地址", img_list)
    # =-----卖家信息————————————————
    cur.execute("select * from t_user where user_id=%s", [seller_id, ])  # 获取卖家信息
    seller_info = cur.fetchall()
    cur.execute("select count(*) from t_order_success where release_user_id=%s", [seller_id])
    count_sell = cur.fetchone()["count(*)"]
    # 判断买卖家
    if customer == "buy":
        # --本商品是否已经评价-------------------
        cur.execute("select * from t_order_success where order_goods_id=%s", [goods_id, ])  # 获取商品表内容
        buy_list = cur.fetchone()
        print(buy_list, "44444444444444444")
        order_id = buy_list["order_id"]
        eva_state = buy_list["buy_eva_state"]
        if eva_state != 0:
            cur.execute("select * from t_evaluation where evaluation_order_id=%s", [order_id, ])
            buy_desc_list = cur.fetchall()
            print(buy_desc_list, 5555555555555555555555)
    else:
        print(customer)
        cur.execute("select * from t_order_success where order_goods_id=%s", [goods_id, ])  # 获取商品表内容
        sell_list = cur.fetchone()
        print(sell_list)
        eva_state = sell_list["sell_eva_state"]
        order_id = sell_list["order_id"]
        print("订单：", order_id, "状态", type(eva_state))
        if eva_state != 0:
            cur.execute("select * from t_evaluation where evaluation_order_id=%s", [order_id, ])
            sell_desc_list = cur.fetchall()
            print(55555555, customer, eva_state, order_id, sell_desc_list)

    return render(request, 'evaluate.html', locals())


@mysql_required
def evaluate_ajax(request):
    user_id = request.session.get('user_id')
    evaluate_text = request.POST.get('evaluate_text')
    customer = request.POST.get('customer')
    order_id = request.POST.get('order_id')
    sudu = int(request.POST.get('sudu'))
    qingkuang = int(request.POST.get('qingkuang'))
    taidu = int(request.POST.get('taidu'))
    eva_state = int(request.POST.get('pingjia'))
    if eva_state == 0:
        user_credit1 = 2 * (sudu + qingkuang + taidu) / 3
    elif eva_state == 1:
        user_credit1 = (sudu + qingkuang + taidu) / 3
    else:
        sudu = 10 - sudu
        taidu = 10 - taidu
        qingkuang = 10 - qingkuang
        user_credit1 = -(sudu + qingkuang + taidu) / 3

    print(sudu, qingkuang, taidu, eva_state, 666666666666666666666666)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(evaluate_text, eva_state, customer, type(order_id))
    if customer == "buy":
        cur.execute(
            "update t_evaluation set buyer_evaluation_date = %s,buyer_desc=%s,buy_state=%s where evaluation_order_id = %s",
            [now_time, evaluate_text, eva_state, order_id])
        cur.execute("update t_order_success set buy_eva_state=%s where order_id=%s", [1, order_id])
        # __________________redis保存被回复人记录(别人查看记录)-----------------------------------------------------------------------
        cur.execute("select * from t_order_success where order_id=%s", [int(order_id), ])
        order_list = cur.fetchone()
        cur.execute("update t_user set user_credit=user_credit+%s where user_id=%s",
                    [user_credit1, order_list["release_user_id"]])
        key = str(order_list["release_user_id"]) + str(order_id)
        print("购买人，", key)
        # 评价人的信息！-------------
        cur.execute("select * from t_user where user_id=%s", [user_id, ])
        get_user_list = cur.fetchone()
        # 商品信息！----------------------------------------------------
        cur.execute("select * from t_goods where goods_id=%s", [order_list["order_goods_id"], ])
        goods_lst = cur.fetchone()
        get_eva.hset(key, "username", get_user_list["user_name"])
        get_eva.hset(key, "user_imgurl", get_user_list["user_imgurl"])
        get_eva.hset(key, "user_id", get_user_list["user_id"])
        get_eva.hset(key, "user_address", get_user_list["user_address"])
        get_eva.hset(key, "desc", evaluate_text)
        get_eva.hset(key, "date", now_time)
        get_eva.hset(key, "goods_id", goods_lst["goods_id"])
        get_eva.hset(key, "goods_name", goods_lst["goods_title"])
        get_eva.hset(key, "goods_price", goods_lst["goods_price"])
        get_eva.hset(key, "eva_state", eva_state)
        get_eva.hset(key, "customer", "买家")
        # __________________redis保存回复人记录-----------------------------------------------------------------------
        # 评价用户的信息！-------------
        key_ = str(order_list["buy_user_id"]) + str(order_id)
        cur.execute("select * from t_user where user_id=%s", [order_list["release_user_id"], ])
        set_user_list = cur.fetchone()
        set_eva.hset(key_, "username", set_user_list["user_name"])
        set_eva.hset(key_, "user_imgurl", set_user_list["user_imgurl"])
        set_eva.hset(key_, "user_id", set_user_list["user_id"])
        set_eva.hset(key, "user_address", set_user_list["user_address"])
        set_eva.hset(key_, "desc", evaluate_text)
        set_eva.hset(key_, "date", now_time)
        set_eva.hset(key_, "goods_id", goods_lst["goods_id"])
        set_eva.hset(key_, "goods_name", goods_lst["goods_title"])
        set_eva.hset(key_, "goods_price", goods_lst["goods_price"])
        set_eva.hset(key_, "eva_state", eva_state)
        set_eva.hset(key_, "customer", "卖家")
        message_push.lpush(order_list["release_user_id"], "evaluation")
    else:
        print("卖卖卖")
        cur.execute(
            "update t_evaluation set seller_evaluation_date = %s,seller_desc=%s,sell_state=%s where evaluation_order_id = %s",
            [now_time, evaluate_text, eva_state, order_id])
        cur.execute("update t_order_success set sell_eva_state=%s where order_id=%s", [1, order_id])
        # __________________redis保存被回复人记录(别人查看记录)-----------------------------------------------------------------------
        cur.execute("select * from t_order_success where order_id=%s", [int(order_id), ])
        order_list = cur.fetchone()
        cur.execute("update t_user set user_credit=user_credit+%s where user_id=%s",
                    [user_credit1, order_list["buy_user_id"]])
        key = str(order_list["buy_user_id"]) + str(order_id)
        # 被评价用户的信息！-------------
        cur.execute("select * from t_user where user_id=%s", [user_id, ])
        get_user_list = cur.fetchone()
        # 商品信息！----------------------------------------------------
        cur.execute("select * from t_goods where goods_id=%s", [order_list["order_goods_id"], ])
        goods_lst = cur.fetchone()
        get_eva.hset(key, "username", get_user_list["user_name"])
        get_eva.hset(key, "user_imgurl", get_user_list["user_imgurl"])
        get_eva.hset(key, "user_id", get_user_list["user_id"])
        get_eva.hset(key, "user_address", get_user_list["user_address"])
        get_eva.hset(key, "desc", evaluate_text)
        get_eva.hset(key, "date", now_time)
        get_eva.hset(key, "goods_id", goods_lst["goods_id"])
        get_eva.hset(key, "goods_name", goods_lst["goods_title"])
        get_eva.hset(key, "goods_price", goods_lst["goods_price"])
        get_eva.hset(key, "eva_state", eva_state)
        get_eva.hset(key, "customer", "卖家")
        # __________________redis保存回复人记录-----------------------------------------------------------------------
        # 评价用户的信息！-------------
        key_ = str(order_list["release_user_id"]) + str(order_id)
        cur.execute("select * from t_user where user_id=%s", [order_list["buy_user_id"], ])
        set_user_list = cur.fetchone()
        set_eva.hset(key_, "username", set_user_list["user_name"])
        set_eva.hset(key_, "user_imgurl", set_user_list["user_imgurl"])
        set_eva.hset(key_, "user_id", set_user_list["user_id"])
        set_eva.hset(key_, "user_address", set_user_list["user_address"])
        set_eva.hset(key_, "desc", evaluate_text)
        set_eva.hset(key_, "date", now_time)
        set_eva.hset(key_, "goods_id", goods_lst["goods_id"])
        set_eva.hset(key_, "goods_name", goods_lst["goods_title"])
        set_eva.hset(key_, "goods_price", goods_lst["goods_price"])
        set_eva.hset(key_, "eva_state", eva_state)
        set_eva.hset(key_, "customer", "买家")
        message_push.lpush(order_list["buy_user_id"], "evaluation")
    con.commit()
    msg = "success"
    return HttpResponse(json.dumps({"msg": msg}))


# 我收到的评价
@mysql_required
@message_push_
def my_evaluate_get(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    cur.execute(
        "select order_id from t_order_success where buy_user_id=%s and sell_eva_state=%s or release_user_id=%s and buy_eva_state=%s",
        [user_id, 1, user_id, 1])
    order_id = cur.fetchall()
    eva_list = []
    # print(user_id)
    count_order = len(order_id)
    for id in order_id:
        one = {}
        key = str(user_id) + str(id["order_id"])
        a = get_eva.hgetall(key)
        # print(key, a)
        if a:
            for i in a:
                c = a[i].decode("utf-8")
                i = i.decode("utf-8")
                one[i] = c
            eva_list.append(one)
        else:
            eva_list.append("none")
    print(eva_list)

    return render(request, 'my_evaluate_get.html', locals())


# 给他人的评价
@mysql_required
def my_evaluate_give(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    cur.execute(
        "select order_id from t_order_success where buy_user_id=%s and sell_eva_state=%s or release_user_id=%s and buy_eva_state=%s",
        [user_id, 1, user_id, 1])
    order_id = cur.fetchall()
    eva_list = []
    # print(user_id)
    count_order = len(order_id)
    for id in order_id:
        one = {}
        key = str(user_id) + str(id["order_id"])
        print(key)
        a = set_eva.hgetall(key)
        # print(key, a)
        if a:
            for i in a:
                c = a[i].decode("utf-8")
                i = i.decode("utf-8")
                one[i] = c
            eva_list.append(one)
        else:
            eva_list.append("none")
    print(eva_list)

    return render(request, 'my_evaluate_give.html', locals())


# 系统消息
@login_required
@mysql_required
@message_push_
def system_message(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    login_status = username
    cur.execute("select * from t_system_message where get_message_id=%s order by system_message_id desc", [user_id, ])
    message_list = cur.fetchall()
    paginator = Paginator(message_list, 5)
    page = request.GET.get('page')
    print("系统消息", message_list)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'system_message.html', locals())


# 收到的回复
@login_required
@mysql_required
@message_push_
def leave_message(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    cur.execute(
        'select * from t_second_message inner join t_user on child_user_id=user_id inner join t_goods on second_goods_id=goods_id '
        'where to_rid=%s order by second_message_id desc',
        [user_id, ])
    review_list = cur.fetchall()
    paginator = Paginator(review_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'leave_message.html', locals())


# 我的回复
@login_required
@mysql_required
def leave_message_two(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    cur.execute(
        'select * from t_second_message inner join t_user on to_rid=user_id inner join t_goods on second_goods_id=goods_id '
        'where child_user_id=%s order by second_message_id desc',
        [user_id, ])
    my_review_list = cur.fetchall()
    paginator = Paginator(my_review_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'leave_message_two.html', locals())


@login_required
@mysql_required
@message_push_
def leave_message_three(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    cur.execute(
        "select * from t_goods right join t_message on goods_id=message_goods_id inner join t_user on message_user_id=t_user.user_id where t_goods.user_id=%s ",
        [user_id, ])
    my_review_list = cur.fetchall()
    print(my_review_list)
    paginator = Paginator(my_review_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'leave_message_three.html', locals())


# 修改信息
@mysql_required
@login_required
def modify_information(request):
    user_id = request.session.get('user_id')
    if request.method == 'GET':
        cur.execute("select * from t_user where user_id = '%s'" % user_id)
        result = cur.fetchall()[0]
        user = json.dumps(result, cls=CJsonEncoder)
        user = json.loads(user)
        username = request.session.get('username')
        if username:
            message_check1 = message_push.lrange(user_id, 0, 1)
            message_list_push = []
            message_list_push1 = message_push.lrange(user_id, 0, 3)
            for item in message_list_push1:
                message_list_push.append(item.decode("utf-8"))
            print(message_list_push)
            if message_check1:
                message_check = "../static/Images/new02.gif"
            else:
                message_check = "../static/Images/message.png"
            print(message_check, "消息推送")
            login_status = username
        return render(request, 'modify_information.html', locals())
    else:
        shen = request.POST.get('cmbProvince')
        shi = request.POST.get('cmbCity')
        xian = request.POST.get('cmbArea')
        img = request.POST.get('img')
        date = request.POST.get('date')
        sex = request.POST.get('sex')
        password = request.POST.get('pay_password')

        if shen == '请选择省份':
            area = ''
        else:
            area = shen + ' ' + shi + ' ' + xian
        cur.execute(
            "UPDATE t_user SET `user_pay_password` = '%s',`user_imgurl` = '%s',`user_sex`='%s',`user_birthday`='%s',`user_address`='%s' where user_id = '%s'" % (

                password, img, sex, date, area, user_id))
        con.commit()
        return redirect('/modify_information/')


def modify_password(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    if username:
        message_check1 = message_push.lrange(user_id, 0, 1)
        message_list_push = []
        message_list_push1 = message_push.lrange(user_id, 0, 3)
        for item in message_list_push1:
            message_list_push.append(item.decode("utf-8"))
        print(message_list_push)
        if message_check1:
            message_check = "../static/Images/new02.gif"
        else:
            message_check = "../static/Images/message.png"
        print(message_check, "消息推送")
        login_status = username
    return render(request, 'modify_password.html', locals())


@mysql_required
@login_required
def modify_password_ajax(request):
    user_phone = request.POST.get('user_phone')
    phone_yzm = request.POST.get('phone_yzm')
    user_id = request.session.get('user_id')
    user_password = request.POST.get('user_password')
    repwd = request.POST.get('repwd')
    print(repwd)
    cur.execute("select user_phone from t_user where user_id = %s", [user_id, ])
    users_phone = cur.fetchone()
    if user_phone:
        if user_phone != users_phone['user_phone']:
            msg = "phone_error"
            return HttpResponse(json.dumps({'msg': msg}))
        else:
            msg = '111'
            if sms.get(user_phone):
                true_phone_yzm = sms.get(user_phone)
                true_phone_yzm = true_phone_yzm.decode('utf-8')
                if phone_yzm != true_phone_yzm:
                    msg = "phone_yzm_error"
                    return HttpResponse(json.dumps({'msg': msg}))
            return HttpResponse(json.dumps({'msg': msg}))
    if user_password == '':
        msg = 'user_password_none'
        return HttpResponse(json.dumps({'msg': msg}))
    else:
        if user_password != repwd:
            msg = 'repsd_error'
            return HttpResponse(json.dumps({'msg': msg}))
        if user_password == repwd:
            cur.execute("update t_user set user_password = %s where user_id =%s", [user_password, user_id])
            con.commit()
            msg = '222'
            return HttpResponse(json.dumps({'msg': msg}))


# 上传图片所需要的token
def gettokendata(request):
    index = request.POST.get('index')
    if index == None:
        index = '1'
    from qiniu import Auth
    access_key = 'ln1sRuRjLvxs_7jjVckQcauIN4dieFvtcWd8zjQF'
    secret_key = 'YogFj8XEOnZOfkapjAL2UuMmtujVEONBJRbowx-p'
    q = Auth(access_key, secret_key)
    bucket_name = 'haima'
    key = None
    policy = {
        "scope": "haima",
        "returnBody": '{"key": $(key), "index": "' + index + '"}',
    }
    token = q.upload_token(bucket_name, key, 3600, policy)
    return HttpResponse(token)


# ***********************************************普通商品确认收货*************************************************
@mysql_required
@login_required
def confirm_goods(request):
    goods_id = request.POST.get("goods_id")
    cur.execute("select * from t_order where order_goods_id=%s", [goods_id])
    goods_message = cur.fetchone()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    user_id = request.session.get('user_id')
    # 把信息加到订单成功表：然后删除原来订单表里的数据
    try:
        cur.execute("insert into t_order_success (release_user_id,buy_user_id,order_date,order_goods_id) values (%s,%s,%s,%s\
                      )",
                    [str(goods_message["release_user_id"]), str(goods_message["buy_user_id"]), date, str(goods_id)])
        goods_order_id = cur.lastrowid
        cur.execute("select order_id from t_order where order_goods_id=%s", [goods_id])
        cur.execute("delete from t_order where order_goods_id=%s", [str(goods_id)])
        # 用户确认收货以后需要把卖家的钱增加
        cur.execute("select goods_price from t_goods where goods_id=%s", [goods_id])
        goods_price = cur.fetchone()["goods_price"]
        cur.execute("select user_money from t_user where user_id=%s", [goods_message["release_user_id"]])
        user_money = cur.fetchone()["user_money"]
        user_money = user_money + goods_price
        cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, goods_message["release_user_id"]])
        cur.execute("insert into t_evaluation (evaluation_order_id,buy_id,sell_id) values (%s,%s,%s)",
                    [goods_order_id, user_id, goods_message["release_user_id"]])
        con.commit()
        print("ok")
    except Exception as e:
        con.rollback()
        print(e)

    return HttpResponse(json.dumps({"msg": "123"}))


def get_ali_object():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2016092000555548"  # APPID （沙箱应用）

    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
    # notify_url = "http://47.94.172.250:8804/page2/"
    notify_url = "http://127.0.0.1:8000/page2/"
    # 支付完成后，跳转的地址。
    return_url = "http://127.0.0.1:8000/page2/"
    merchant_private_key_path = "keys/app_private_2048.txt"  # 应用私钥
    alipay_public_key_path = "keys/alipay_public_2048.txt"  # 支付宝公钥
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay


# 前端跳转的支付页面
@login_required
def page1(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    # 根据当前用户的配置，生成URL，并跳转。
    user_id = request.session.get("user_id")
    money = request.POST.get('price')
    title = request.POST.get('title')
    phone = request.POST.get('phone')
    name = request.POST.get('name')
    address = request.POST.get('address') + request.POST.get("user_address")
    alipay = get_ali_object()
    goods_id = request.POST.get('goods_id')
    cur.execute("select goods_state from t_goods where goods_id=%s", [goods_id])
    state = cur.fetchone()["goods_state"]
    print(type(state))
    request.session['goods_id'] = goods_id

    if state == '1':
        return HttpResponse("error")
    else:
        request.session['user_buy_phone'] = phone
        request.session['name'] = name
        request.session['address'] = address
        # 生成支付的url
        query_params = alipay.direct_pay(
            subject=title,  # 商品简单描述
            out_trade_no="x2" + str(time.time()),  # 用户购买的商品订单号（每次不一样） 20180301073422891
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
        cur.close()
        return HttpResponse(pay_url)


@mysql_required
def page2(request):
    alipay = get_ali_object()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        # post_dict有10key： 9 ，1
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('------------------开始------------------')
        print('POST验证', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']

        # 修改订单状态
        # models.Order.objects.filter(trade_no=out_trade_no).update(status=2)
        print('------------------结束------------------')
        # 修改订单状态：获取订单号
        return HttpResponse('POST返回')

    else:
        user_id = request.session.get("user_id")
        goods_id = request.session.get("goods_id")
        phone = request.session.get("user_buy_phone")
        name = request.session.get("name")
        address = request.session.get("address")
        cur.execute("select order_id from t_order where order_goods_id=%s", [goods_id])
        x = cur.fetchone()
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================开始==================')
        print('GET验证', status)
        print('==================结束==================')
        print("支付成功")
        try:
            if x:
                return HttpResponse("购买已经完成")
                # 生成商品订单
            else:
                cur.execute("select user_id from t_goods where goods_id=%s", [goods_id])
                release_user_id = cur.fetchone()["user_id"]
                date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                cur.execute(
                    "insert into t_order(release_user_id,buy_user_id,order_date,order_goods_id,buy_phone,buy_name,buy_address) values (%s,%s,%s,%s,%s,%s,%s)",
                    [str(release_user_id), str(user_id), date, str(goods_id), str(phone), str(name), str(address)])
                print("生成订单成功")
                cur.execute("update t_goods set goods_state=%s where goods_id=%s", ["1", goods_id])
                print("更新商品状态成功")
                con.commit()
                message_push.lpush(release_user_id, "my_sale")


        except Exception as e:
            print(e)
        return redirect("/user_center/")


def admin_session(func):
    def in_func(request):
        user = request.session.get('user')
        if user:
            return func(request, user)
        else:
            return redirect('/admin_login/')

    return in_func


def admin_login(request):
    if request.method == "GET":
        return render(request, 'admin_login.html')
    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        cur.execute("select * from t_admin where user=%s and pwd=%s", [user, pwd])
        result = cur.fetchall()
        if result:
            request.session['user'] = user
            return HttpResponse('login')
        else:
            return HttpResponse('')


@admin_session
def admin(request, user):
    cur.execute('SELECT COUNT(*) FROM t_user')
    num_user = cur.fetchall()[0]['COUNT(*)']
    cur.execute('SELECT COUNT(*) FROM t_goods WHERE goods_state = 0')
    num_goods = cur.fetchall()[0]['COUNT(*)']
    return render(request, 'admin.html', {'user': user, 'num_user': num_user, 'num_goods': num_goods})


@admin_session
def admin_goods(request, user):
    return render(request, 'admin_goods.html', {'user': user})


@admin_session
def admin_search_goods(request, user):
    start = request.POST.get('start')
    end = request.POST.get('end')
    key = request.POST.get('key')
    if not end:
        end = loc_time
    sql = "select goods_id,goods_title,user_name,goods_category_id,goods_state,release_date,goods_address from t_goods inner join t_user on t_goods.user_id=t_user.user_id where release_date BETWEEN '%s' AND '%s'" % (
        start, end)
    goods_type = request.POST.get('goods_type')
    goods_state = request.POST.get('goods_state')
    if goods_type in ['1', '2', '3', '4', '5']:
        sql += " and goods_category_id = '%s'" % (goods_type)
    if goods_state in ['0', '1', '2']:
        sql += " and goods_state= '%s'" % (goods_state)
    if key:
        key = '%' + key + '%'
        sql += " and concat(goods_title,goods_address,user_name,goods_id) like '%s'" % (key)
    cur.execute(sql)
    goodslist = cur.fetchall()
    paginator = Paginator(goodslist, 35)
    page = request.POST.get('page')
    try:
        contacts = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
        page = 1
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    num_pages = paginator.num_pages
    if num_pages <= 5:
        pagelist = [i + 1 for i in range(num_pages)]
    else:
        if page <= 3:
            pagelist = [i + 1 for i in range(5)]
        elif page >= num_pages - 2:
            pagelist = [i + 1 for i in range(num_pages - 5, num_pages)]
        else:
            pagelist = [i + 1 for i in range(page - 2, page + 3)]
    datalist = {'page': page, 'num_pages': num_pages, 'data': contacts.object_list, 'pagelist': pagelist}
    return HttpResponse(json.dumps(datalist, cls=CJsonEncoder), content_type="application/json")


@admin_session
def admin_search_user(request, user):
    start = request.POST.get('start')
    end = request.POST.get('end')
    key = request.POST.get('key')
    user_state = request.POST.get('user_state')
    if not end:
        end = loc_time
    sql = "select user_id,user_name,user_password,user_address,user_phone,user_startdate,user_money,user_state from t_user where user_startdate BETWEEN '%s' AND '%s'" % (
        start, end)
    user_state = request.POST.get('user_state')
    if user_state in ['0', '1']:
        sql += " and user_state= '%s'" % (user_state)
    if key:
        key = '%' + key + '%'
        sql += " and concat(user_name,user_phone,user_address) like '%s'" % (key)
    cur.execute(sql)
    userlist = cur.fetchall()
    paginator = Paginator(userlist, 35)
    page = request.POST.get('page')
    try:
        contacts = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
        page = 1
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    num_pages = paginator.num_pages
    if num_pages <= 5:
        pagelist = [i + 1 for i in range(num_pages)]
    else:
        if page <= 3:
            pagelist = [i + 1 for i in range(5)]
        elif page >= num_pages - 2:
            pagelist = [i + 1 for i in range(num_pages - 5, num_pages)]
        else:
            pagelist = [i + 1 for i in range(page - 2, page + 3)]
    datalist = {'page': page, 'num_pages': num_pages, 'data': contacts.object_list, 'pagelist': pagelist}
    return HttpResponse(json.dumps(datalist, cls=CJsonEncoder), content_type="application/json")


@admin_session
def admin_update(request, user):
    checkID = request.POST.get('checkID')
    goods_id = request.POST.get('goods_id')
    user_id = request.POST.get('user_id')
    action = request.POST.get('action')
    if checkID:
        checkID = '(' + checkID[1:-1] + ')'
        sql = "update t_goods set goods_state = '" + action + "' where goods_id in " + checkID
        print(sql)
        result = cur.execute(sql)
    else:
        if goods_id:
            if action == 'del':
                result = cur.execute("delete from t_goods where goods_id = %s", [goods_id, ])
            else:
                result = cur.execute("update t_goods set goods_state = %s where goods_id = %s", [action, goods_id, ])
        else:
            if action == 'del':
                result = cur.execute("delete from t_user where user_id = %s", [user_id, ])
            else:
                result = cur.execute("update t_user set user_state = %s where user_id = %s", [action, user_id, ])
    con.commit()
    if result:
        return HttpResponse("success")
    else:
        return HttpResponse('')


@admin_session
def admin_user(request, user):
    cur.execute(
        "select user_id,user_name,user_password,user_address,user_phone,user_startdate,user_money,user_state from t_user")
    userlist = cur.fetchall()
    return render(request, 'admin_user.html', {'user': user, 'userlist': userlist})


@admin_session
def admin_order(request, user):
    cur.execute(
        "select * from (t_goods inner join t_user on t_goods.user_id=t_user.user_id)inner join t_order on t_goods.goods_id = t_order.order_goods_id")
    orderlist = cur.fetchall()
    print(orderlist)
    return render(request, 'admin_order.html', {'user': user, 'orderlist': orderlist})


@admin_session
def exit(request, user):
    del request.session['user']
    return redirect('/admin_login/')


@login_required
def place_order(request):
    user_id = request.session.get("user_id")
    goods_id = request.GET.get("goods_id")
    cur.execute("select * from t_goods where goods_id=%s", [goods_id])
    goods_message = cur.fetchone()
    return render(request, 'place_order.html', locals())


def by_scort(t):
    return t[1]


def search_image(request):
    goods_id_list = []
    goods_list = []
    url = request.POST.get("url")
    if url:
        result = client.productSearchUrl(url)
        print(url)
        if result['result']:
            print(result)
            for goods in result['result']:
                score = goods['score']
                if score > 0.5:
                    brief = json.loads(goods['brief'])
                    id = brief['id']
                    print(id)
                    goods_id_list.append((id, score))
        goods_id_list = sorted(goods_id_list, key=by_scort, reverse=True)
        for goods_id in goods_id_list:
            cur.execute("select goods_id,goods_imgurl,goods_title,goods_price from t_goods where goods_id = %s",
                        [goods_id[0], ])
            goods = cur.fetchone()
            goods_list.append(goods)
        return render(request, 'search_image.html', locals())
    else:
        return redirect('/haima/')
