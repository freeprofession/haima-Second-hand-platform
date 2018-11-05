import pymysql
import time

st_time = time.localtime(time.time())
loc_time = '{}-{}-{}'.format(st_time.tm_year, st_time.tm_mon, st_time.tm_mday)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import base64

# r = redis.Redis(host='47.100.200.132', port='6379')
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
from myapp import AI_assess

r = redis.Redis(host="47.100.200.132", port=6379)
r1 = redis.Redis(host="47.100.200.132", port=6379, db=1)
<<<<<<< HEAD
=======
<<<<<<< HEAD
img = redis.Redis(host="47.100.200.132", port=6379, db=2)  # 商品图片
category = redis.Redis(host="47.100.200.132", port=6379, db=3)  # 商品分类
cut_words = redis.Redis(host="47.100.200.132", port=6379, db=4)  # 分词搜索
sms = redis.Redis(host="47.100.200.132", port=6379, db=5)  # 注册验证码
=======
>>>>>>> 5bd55ac73206ca4960e0b4ed17efbadfd14be180
img = redis.Redis(host="47.100.200.132", port=6379, db=2)
category = redis.Redis(host="47.100.200.132", port=6379, db=3)
cut_words = redis.Redis(host="47.100.200.132", port=6379, db=4)
auction_img= redis.Redis(host="47.100.200.132", port=6379, db=5)
<<<<<<< HEAD
sms = redis.Redis(host="47.100.200.132", port=6379, db=5)  # 注册验证码
=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295
>>>>>>> 5bd55ac73206ca4960e0b4ed17efbadfd14be180


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
<<<<<<< HEAD

=======
<<<<<<< HEAD
=======
img = redis.Redis(host="47.100.200.132", port=6379, db=2)  # 商品图片
category = redis.Redis(host="47.100.200.132", port=6379, db=3)  # 商品分类
cut_words = redis.Redis(host="47.100.200.132", port=6379, db=4)  # 分词搜索
sms = redis.Redis(host="47.100.200.132", port=6379, db=5)  # 注册验证码
>>>>>>> 5bd55ac73206ca4960e0b4ed17efbadfd14be180

>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295

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
<<<<<<< HEAD

=======
>>>>>>> 5bd55ac73206ca4960e0b4ed17efbadfd14be180


# 登录状态检查，装饰器
def login_required(function):
    def check_login_status(request):
        user_id = request.session.get('user_id')
        if user_id:
            return function(request)
        else:
            return HttpResponseRedirect('/login/')

    return check_login_status


def homepage(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    if username:
        login_status = username
        cur.execute(
            "select * from t_goods where goods_address = (select user_address from t_user where user_id = %s) order by rand() limit 5",
            [user_id, ])
        same_city_list = cur.fetchall()
        cur.execute("select user_imgurl from t_user where user_id = %s", [user_id, ])
        user_imgurl = cur.fetchone()
        if user_imgurl['user_imgurl'] == None:
            cur.execute("update t_user set user_imgurl = %s where user_id = %s",
                        ['../static/Images/default_hp.jpg', user_id])
            con.commit()
            cur.execute("select user_imgurl from t_user where user_id = %s", [user_id, ])
            user_imgurl = cur.fetchone()
    else:
        login_status = "未登录"
        user_imgurl = {}
        user_imgurl['user_imgurl'] = '../static/Images/default_hp.jpg'
    sql = "select * from t_goods limit 0,10"
    cur.execute(sql)
    goods_list = cur.fetchall()
    # 收藏--------------------------
    # cur.execute("select * from t_user_collection where collection_user_id=%s", [user_id, ])
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s ',
        [user_id, ])
    collection_list = cur.fetchall()
    cur.execute("select * from t_goods order by goods_id desc limit 5")
    newest_list = cur.fetchall()
    return render(request, 'homepage.html', locals())


def homepage_ajax(request):
    pass
    # print(goods_list)
    return render(request, 'homepage.html', {'goods_list': goods_list})


# 登录
def login(request):
    url = request.META.get('HTTP_REFERER', '/')
    print(url, "返回地址")
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
            print(login_code['status'])
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
        cur.execute("select * from t_user where user_name=%s", [username, ])  # 全表搜索，待建立索引
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
        # code = request.POST.get("code")
        check_code = r.get(phone)  # 获取手机验证码
        check_all = request.POST.get("check_all")
        # print(username, password, phone, check_code, check_all, login_code)
        if login_code['status'] == 1:  # 图片验证码

            if check_code:  # 手机验证码待定！
                check_code = check_code.decode('utf8')
                if user_error == "" and check_all == 'true':
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
                    cur.execute(
                        "insert into t_user(user_name,user_password,user_phone,user_startdate) values(%s,%s,%s,%s)",
                        [username, password, phone, now_time])
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
def register_ok(request):
    return render(request, "register_ok.html")


# 搜索跳转到商品列表-------------------------------------------
def goods_list(request):
    value_list = []
    start_list = []
    goods_lst = []
    if request.method == 'GET':
        question = request.GET.get('q')
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
                    prompt = '以下商品为' + user_address + '地区同城的商品，如需要查询其他地区请在用户中心中修改居住地'
                else:
                    prompt = '亲还没有设置居住地看不到同城商品哟！请在用户中心设置'
            else:
                return redirect('/user_center/')
        else:
            question_word = jieba.cut(question)
            question_word = list(question_word)
            if len(question_word) != 1:
                question_word.insert(0, question)
            count = 0
            for key in question_word:
                if cut_words.smembers(key):
                    count += 1
                    bvalue_list = list(cut_words.smembers(key))
                    for value in bvalue_list:
                        value = int(value.decode('utf-8'))
                        if value not in value_list:
                            value_list.append(value)
                    for goods_id in value_list:
                        sql = "select * from t_goods where goods_id = %d" % goods_id
                        cur.execute(sql)
                        goods = cur.fetchone()
                        goods_lst.append(goods)
            prompt = '已选条件： 所有与' + question + '相关的宝贝'
            if count == 0:
                return render(request, 'register_ok.html')

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
        paginator = Paginator(goods_lst, 18)
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
@login_required
def user_center(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    if username:
        # 用户信息------------------
        cur.execute("select * from t_user where user_name=%s", [username, ])
        user_info = cur.fetchall()
        # 浏览记录--------------------------------
        cur.execute(
            'select * from t_goods right join t_user_browse on browse_goods_id=goods_id where browse_user_id=%s',
            [user_id, ])
        # cur.execute("select * from t_user_browse where browse_user_id=%s", [user_id, ])
        browse_list = cur.fetchall()

        #这里需要返回他的购买和出售数量，从order_success 订单成功表去查
        cur.execute("select * from t_order_success where buy_user_id=%s",[user_id])
        dict1=cur.fetchall()
        buy_conut=0
        if dict1:
            buy_conut=len(dict1)
        print(user_info, browse_list, 77777777777777777777)
<<<<<<< HEAD
=======
<<<<<<< HEAD

=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295
>>>>>>> 5bd55ac73206ca4960e0b4ed17efbadfd14be180
        return render(request, 'user_center.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# 用户信誉-----------------------------------
@login_required
def user_credit(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    user_credit_id = request.GET.get('user_credit_id')
    # 判断是否登陆-------------------------------
    if user_id:
        # 判断是否为本人进入
        print(user_id, user_credit_id)
        if str(user_credit_id) == str(user_id):
            return redirect("/user_center/")
        else:
            # -用户信息
            cur.execute("select * from t_user where user_id=%s ", [user_credit_id, ])
            user_info = cur.fetchall()
            # 计算天数------------------
            day_ = user_info[0]["user_startdate"]
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
            cur.execute("select * from t_goods where user_id=%s and goods_state=%s", [user_credit_id, 0])
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

            print(goods)
            return render(request, "user_credit.html", locals())
    else:
        return redirect('/login/')


# _____________________________________________________________-

# 商品界面设置
def goods_detail(request):
    username = request.session.get('username')  # 获取买家用户名
    user_id = request.session.get('user_id')  # 获取买家ID
    goods_id = request.GET.get('goods')
    # 商品收藏------------------------------------------
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s ',
        [user_id, ])
    collection_list = cur.fetchall()
    # --------------------------------------------------
    print(goods_id)  # 获取商品ID
    cur.execute("select * from t_goods where goods_id=%s", [goods_id, ])  # 获取商品表内容
    goods_list = cur.fetchall()  # 商品表内容
    print(username, user_id, goods_id, goods_list)
    seller_id = goods_list[0]['user_id']  # 获取卖家ID
    goods_state = goods_list[0]['goods_state']  # 商品状态
    # 获取商品图片
    img_list = []
    for item in img.lrange(goods_id, 0, 4):
        item = item.decode("utf-8")
        img_list.append(item)
    print("商品图片地址", img_list)

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
    button_list = []
    for i in p_comment_dict:
        button_list.append(int(i))
    # print(p_comment_dict)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    if username:  # 登录后才记录，浏览记录
        cur.execute("select user_imgurl from t_user where user_id=%s", [user_id])
        user_imgurl = cur.fetchone()["user_imgurl"]
        print("图片", user_imgurl)

        login_status = username
        cur.execute("select * from t_user_browse where browse_user_id=%s and browse_goods_id=%s", [user_id, goods_id])
        browse = cur.fetchone()
        # print(browse, "检查")
        if browse is None:
            count = goods_list[0]['goods_browse_count']
            count += 1
            # 更新商品浏览次数
            cur.execute("update t_goods set goods_browse_count=%s where goods_id=%s", [count, goods_id])
            print(count, goods_id, "商品浏览记录")
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
    return render(request, "detail.html", locals())


# 测试用---------------------------------
def text_message(request):
    cur.execute("select * from t_second_message right join t_user on child_user_id=user_id where  second_goods_id=%s",
                [1, ])
    b = cur.fetchall()
    cur.execute('select * from t_message right join t_user on message_user_id=user_id where message_goods_id=%s ',
                [1, ])
    a = cur.fetchall()
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
    print(username, 4444)
    child_id = request.POST.get('child_id')
    cur.execute("select * from t_user where user_id=%s", [child_id, ])
    child_user = cur.fetchone()
    print(child_user['user_name'], 45555)
    message = request.POST.get('message')
    if username:
        print(message)
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
                                        <img src="{1}" alt="" height="40" width="40">
                                        <div style="margin-left: 45px;position: relative;top: -50px;"><a
                                                href="" style="color: #2d64b3"
                                                class="c_name_{2}">{3}</a>:
                                            <span style="color: #333333;font-size: 14px">{4}</span>
                                            <div><span style="color: #a3a3a3">{5}</span>
                                                <a name="abc">1</a>
                                                <input id="review" class="c_review_{6}"
                                                       type="button" value="回复"
                                                       onclick="c_review({7})">
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


def lea_message(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if username:
        Published = request.POST.get("Published")
        goods_id = request.POST.get("goods_id")
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(
            "insert into t_message(message_user_id,message_desc,message_goods_id,message_date) values(%s,%s,%s,%s)",
            [user_id, Published, goods_id, now_time])
        con.commit()
        url = '/goods_detail/?goods=' + str(goods_id)
        return HttpResponse(json.dumps({"href": url}))

    else:
        p_error = 'need_login'
        url = '/login'
        return HttpResponse(json.dumps({"msg": p_error, "href": url}))


# 商品收藏页面++++++++++++++++++++++++++++++++++++++++
def collection(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    goods_id = request.POST.get("goods_id")
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("select * from t_user_collection where collection_user_id=%s and collection_goods_id=%s",
                [user_id, str(goods_id)])
    collection_check_ = cur.fetchone()
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
def lower_goods(request):
    goods_id = request.POST.get("goods_id")
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

    return HttpResponse(json.dumps({"msg": msg, "href": href}))


def goods_detail_ajax(request):
    pass


# 发布商品
def publish(request):
    if request.method == 'POST':
        price = int(request.POST.get('price_hid').replace('¥', ''))
    return render(request, 'publish.html', locals())


def pub_success(request):
    title = request.POST.get('title')
    category = request.POST.get('type')
    price = float(request.POST.get('price'))
    postage = request.POST.get('postage')
    desc = request.POST.get('desc')
    filelist = json.loads(request.POST.get('filelist'))
    address = '江苏苏州 吴江区'
    appearance = '4'
    if desc:
        pass
    else:
        desc = '该卖家比较懒，还没有商品描述'
    for i in filelist:
        print(i)
    sql = "INSERT INTO t_goods(`user_id`,`release_date`,`goods_title`,`goods_desc`,`goods_price`,`goods_category_id`,`goods_imgurl`,`goods_address`,`goods_appearance`) \
                                                                   VALUES ('%s','%s','%s','%s','%f','%s','%s','%s','%s')" % \
          (
              1, loc_time, title, desc, price, category, "http://pgwecu7z4.bkt.clouddn.com/" + filelist[0], address,
              appearance)
    cur.execute(sql)
    con.commit()
    print(title, category, price, postage, filelist)
    return HttpResponse("FROM")


# 估价
def assess(request):
    return render(request, 'assess.html')


# 估计ajax
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
    print(assess_list)
    price = AI_assess.assess_price(assess_list)[0]
    price = '¥' + str(int(price))
    print(price)
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


# 历史拍卖
def history_auction(request):
    id = request.session.get('user_id')
    print(id)
    if id:
        cur.execute('select user_name from t_user where user_id=%s', \
                    [id])
        username = cur.fetchone()

        return render(request, 'histroy_auction.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# ********************************************我的拍卖********************************************************
# 默认是进入用户的发布历史界面
def my_auction(request):
    id = request.session.get('user_id')
    print(id)
    if id:
        cur.execute('select user_name from t_user where user_id=%s', [id])
        username = cur.fetchone()
        list1 = []
        user_id = request.session.get("user_id")
        print(user_id)
        cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s",
                    [user_id])
        message = cur.fetchall()
        id_list = []
        for i in message:
            id_list.append(i["release_auction_goods_id"])
        for goods_id in id_list:
            dict1 = {}
            cur.execute("select * from t_auction_goods where auction_goods_id=%s ", [goods_id])
            goods_messge = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_messge
            dict1["attribute"] = goods_auction_message
            print(goods_auction_message["auction_goods_floorprice"])
            list1.append(dict1)
        print("查询成功")
        return render(request, 'my_auction_one.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# ******************************************发布拍卖*****************************************
# 进入发布拍卖页面把他的名字显示出来


def release_auction(request):
    id = request.session.get('user_id')
    if id:
        cur.execute('select user_name from t_user where user_id=%s', [id])
        username = cur.fetchone()
        return render(request, 'release_auction.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# *****************************************发布拍卖提交处理***********************************************************
# 用户点击发布拍卖的时候的逻辑判断和数据库操作
def publish_auction(request):
    global error
    user_id = request.session.get('user_id')
    cur.execute("select user_money from t_user where user_id=%s",[user_id])
    user_money=cur.fetchone()["user_money"]

    if request.method == 'POST':

        title = request.POST.get('title')
        desc = request.POST.get('desc')
        floorprice = request.POST.get('floorprice')
        floorpremium = request.POST.get("floorpremium")
        end_date = request.POST.get("end_date")
        start_date = request.POST.get("start_date")
        category = request.POST.get("category")
        postage = request.POST.get("postage")
        imgurl_list=json.loads(request.POST.get("img_address"))
        print(imgurl_list)
        imgurl="http://pgwecu7z4.bkt.clouddn.com/"+imgurl_list[0]
        print(imgurl_list)

        list1 = []
        date_now = datetime.datetime.now().strftime('%Y-%m-%d')
        if title and desc and floorpremium and floorprice and end_date and start_date and category and postage:
            if len(title) >= 6 and floorpremium < floorprice and str(floorprice).isdigit() == True and str(
                    floorpremium).isdigit() == True \
                    and start_date == date_now and user_money>=30:
                error = "ok"
                #扣除保证金
                user_money=user_money-30
                cur.execute("insert into t_auction_goods(auction_goods_title,auction_goods_desc,auction_goods_imgurl,\
                            auction_goods_user_id,auction_goods_category_id) values(%s,%s,%s,%s,%s)",
                            [title, desc, imgurl, \
                             str(user_id), str(postage)])

                goods_id = cur.lastrowid
                # 把其余的图片传到redis
                for i in imgurl_list:
                    i="http://pgwecu7z4.bkt.clouddn.com/"+i
                    print(i)
                    auction_img.rpush(goods_id,i)
                cur.execute(
                    "insert into t_release_auction(release_auction_date,release_auction_goods_id,release_auction_user_id) values (%s,%s,%s)" \
                    , [date_now, str(goods_id), str(user_id)])
                cur.execute("insert into t_auction_goods_record(auction_goods_title,auction_goods_desc,auction_goods_imgurl,\
                                                auction_goods_user_id,auction_goods_category_id) values(%s,%s,%s,%s,%s)",
                            [title, desc, imgurl, \
                             str(user_id), str(postage)])
                cur.execute("insert into t_auction_attribute (start_date,end_date,auction_goods_floorprice,auction_goods_floorpremium,\
                            auction_goods_price,auction_goods_id) values (%s,%s,%s,%s,%s,%s)",
                            [start_date, end_date, floorprice, floorpremium, floorprice, str(goods_id)])
                cur.execute("update t_user set user_money=%s where user_id=%s",[user_money,user_id])
                con.commit()
                return HttpResponse(json.dumps({"msg": error}))
            elif len(title) < 6:
                error = 'title.length_error'
                return HttpResponse(json.dumps({"msg": error}))
            elif start_date != date_now:
                error = 'time_error'
                return HttpResponse(json.dumps({"msg": error}))
            elif str(floorprice).isdigit() == False or str(floorpremium).isdigit() == False:
                error = 'price_error'
                return HttpResponse(json.dumps({"msg": error}))
            elif int(floorpremium) >= int(floorprice):
                error = 'floorpremium_error'
                return HttpResponse(json.dumps({"msg": error}))
            elif user_money<30:
                error="margin_error"
                return HttpResponse(json.dumps({"msg": error}))
        else:
            error = 'less_error'
            return HttpResponse(json.dumps({"msg": error}))


# 发布拍卖成功
def release_auction_ok(request):
    return render(request, 'release_auction_ok.html')


# *******************************返回用户的发布记录**************************************

def my_release_record(request):
    return_title = request.GET.get("id")  # 根据传回来的id 来判断返回的值
    print(type(return_title))
    print(return_title)
    if return_title == "one":
        list1 = []
        user_id = request.session.get("user_id")


# 发布拍卖成功
def release_auction_ok(request):
    return render(request, 'release_auction_ok.html')


# **********************************************************返回用户的我的拍卖中心的我的发布界面**************************************
# 这里主要是显示他的发布记录,和发布商品现在的状态
def my_auction_one(request):
    user_id = request.session.get("user_id")
    list10 = []
    list11=[]
    list12=[]
    list13=[]
    list14=[]
    list15=[]
    list16=[]
    print(user_id)
    #从发布记录表里找到商品id
    cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s",[user_id])
    message = cur.fetchall()
    id_list = []
    for i in message:
        id_list.append(i["release_auction_goods_id"])
    print(id_list)
    for goods_id in id_list:
        dict1 = {}
        cur.execute("select auction_goods_state from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
        x = cur.fetchone()
        print(x)
        state=x["auction_goods_state"]

        #返回发布记录的时候就要判断他发布的商品是否5已经下架，2竞拍成功，4购买成功，3付款成功，1流拍
        if int(state)==0:#0代表的是正常拍卖的
            # print("正常拍卖")

            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["state"]="正在拍卖"
            #返回当前竞拍者的姓名
            cur.execute(
                "select auction_record_id from t_auction_record where auction_goods_id=%s",
                [goods_id])
            record_dict = cur.fetchall()
            if record_dict:
                if record_dict:
                    record_list = []
                    for i in record_dict:
                        record_list.append(i["auction_record_id"])
                    record_maxid = max(record_list)
                    cur.execute("select auction_goods_buyuser_id from t_auction_record where auction_record_id=%s",[record_maxid])
                    buy_user_id=cur.fetchone()
                    cur.execute("select user_name from t_user where user_id=%s", [buy_user_id["auction_goods_buyuser_id"]])
                    user_name = cur.fetchone()["user_name"]
                    if user_name:
                        dict1["user_name"] = user_name
                    else:
                        dict1["user_name"] = "无"
            list10.append(dict1)

        if int(state)==1:#1流拍
            # print("流拍")
            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["state"]="商品已经流拍"
            dict1["user_name"] = "无"
            list11.append(dict1)

        if int(state)==2:#2被竞拍成功
            # print("被竞拍成功")
            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["state"]="商品已经被竞拍成功等待买家付款"
            cur.execute("select auction_order_buy_user_id from t_auction_order where auction_order_goods_id=%s",[goods_id])
            buy_user_id=cur.fetchone()
            cur.execute("select user_name from t_user where user_id=%s",[buy_user_id["auction_order_buy_user_id"]])
            user_name=cur.fetchone()["user_name"]
            dict1["user_name"]=user_name
            list12.append(dict1)

        if int(state)==3:#商品付款成功
            print("ok")
            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            cur.execute("select auction_order_id from t_auction_order where auction_order_goods_id=%s",[goods_id])
            order_id=cur.fetchone()["auction_order_id"]
            cur.execute("select * from t_auction_order where auction_order_id=%s", [order_id])
            order_messge = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["state"] = "商品已经付款"
            cur.execute("select auction_order_buy_user_id from t_auction_order where auction_order_goods_id=%s",
                        [goods_id])
            buy_user_id = cur.fetchone()
            cur.execute("select user_name from t_user where user_id=%s", [buy_user_id["auction_order_buy_user_id"]])
            user_name = cur.fetchone()["user_name"]
            dict1["order"]=order_messge
            dict1["user_name"] = user_name
            cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s",[order_id])
            the_goods_state=cur.fetchone()["the_goods_state"]
            if the_goods_state:
                dict1["the_goods_state"]=the_goods_state
                list14.append(dict1)
            else:
                list13.append(dict1)

        if int(state)==4:#商品收货成功
            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["state"] = "商品已经收货"

            list15.append(dict1)

        if int(state)==5:#商品被用户自己下架
            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["state"] = "商品已经下架"
            list16.append(dict1)
    print(list13)
    return render(request, 'my_auction_one.html', locals())


# **********************************************************返回用户的我的拍卖中心我拍卖的界面**************************************
# 这个显示的他正在拍卖中的商品
def my_auction_two(request):
    user_id = request.session.get("user_id")
    list2 = []
    cur.execute("select auction_goods_id from t_auction_goods where auction_goods_user_id=%s", [user_id])
    goods_id_dict = cur.fetchall()
    goods_id_list = []
    goods_list = []
    attribute_list = []
    buy_name_list = []
    # 这里是找到这个人所有正在拍卖的商品
    for i in goods_id_dict:
        goods_id_list.append(i["auction_goods_id"])
    # 找到商品的拍卖属性和基本属性,同时找到商品竞拍者的名字
    for i in goods_id_list:
        cur.execute("select * from t_auction_goods where auction_goods_id=%s", [i])
        goods = cur.fetchone()
        goods_list.append(goods)
        cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [i])
        attribute = cur.fetchone()
        attribute_list.append(attribute)
        cur.execute("select auction_goods_buyuser_id from t_auction_attribute where auction_goods_id=%s", [i])
        buy_user_id = cur.fetchone()["auction_goods_buyuser_id"]
        if buy_user_id and buy_user_id > 0:
            cur.execute("select user_name from t_user where user_id=%s", [buy_user_id])
            buy_name = cur.fetchone()
            buy_name_list.append(buy_name)

        else:
            dict2 = {"user_name": "无"}
            buy_name_list.append(dict2)


    for i in range(len(goods_id_list)):
        dict1 = {}
        dict1["goods"] = goods_list[i]
        dict1["attribute"] = attribute_list[i]
        dict1["buyname"] = buy_name_list[i]
        list2.append(dict1)
    print(list2)
    return render(request, 'my_auction_two.html', locals())
#*****************************************************返回用户的我的拍卖中心我拍卖的界面**************************************
def my_auction_three(request):
    return render(request, 'my_auction_two.html', locals())



# **********************************************************返回用户的我的拍卖中心我的竞拍的界面**************************************
def my_auction_four(request):
    user_id = request.session.get("user_id")
    # 先找到该用户的所有竞拍记录
    cur.execute("select auction_record_id  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    record_id_dict = cur.fetchall()
<<<<<<< HEAD

=======
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])

    goods_record_list = cur.fetchall()
    goods_list = []
    goods_info_list = []
    goods_buyuser_name_list = []
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> af608055631636185d945b5386d63afb1f4ac379

=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295
>>>>>>> 5bd55ac73206ca4960e0b4ed17efbadfd14be180
    #找到用户的订单
    cur.execute("select *  from t_auction_order where auction_order_buy_user_id=%s",[user_id])
    order_dict=cur.fetchall()
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    list6=[]
<<<<<<< HEAD


=======
    # 这里是通过竞拍记录id找到商品id

    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])

    goods_list = []
<<<<<<< HEAD

<<<<<<< HEAD
=======


<<<<<<< HEAD
=======
=======
>>>>>>> f4d504ed34f968dcb3ffc7488120befed846cd42
>>>>>>> 4f7aaa064f8a013a8999f8ad2b7f132d97de98cf
>>>>>>> af608055631636185d945b5386d63afb1f4ac379
=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295
>>>>>>> 5bd55ac73206ca4960e0b4ed17efbadfd14be180
    for i in record_id_dict:
        dict1={}
        #这里拿到拍卖记录表的状态
        cur.execute("select auction_goods_state from t_auction_record where auction_record_id=%s",[i["auction_record_id"]])
        x=cur.fetchone()
        state=x["auction_goods_state"]
        if state==0:#竞拍失败的记录
            dict1 = {}
            print(i)
            cur.execute("select auction_goods_id from t_auction_record where auction_record_id=%s",
                    [i["auction_record_id"]])

            goods_id=cur.fetchone()["auction_goods_id"]
            cur.execute("select *  from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])
            record_message=cur.fetchone()
            cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                        [goods_id])
            goods_message=cur.fetchone()
            cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                        [goods_id])
            attribute=cur.fetchone()
            dict1["state"]="竞拍失败"
            dict1["goods"]=goods_message
            dict1["record"]=record_message
            dict1["attribute"]=attribute
            list2.append(dict1)
        if state==1:#竞拍中的记录
            dict1 = {}
            print(i)
            cur.execute("select auction_goods_id from t_auction_record where auction_record_id=%s",
                    [i["auction_record_id"]])
            goods_id=cur.fetchone()["auction_goods_id"]
            cur.execute("select *  from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])
            record_message=cur.fetchone()
            cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                        [goods_id])
            goods_message=cur.fetchone()
            cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                        [goods_id])
            attribute=cur.fetchone()
            dict1["state"]="竞拍中"
            dict1["goods"]=goods_message
            dict1["record"]=record_message
            dict1["attribute"]=attribute
            list1.append(dict1)
    if order_dict:
        for i in order_dict:
            print("订单",i)
            id=i["auction_order_id"]
            print("id")
            cur.execute("select auction_order_state from t_auction_order where auction_order_id=%s",[id])
            x=cur.fetchone()
            order_state=x["auction_order_state"]

            #这里待支付尾款的
            if order_state==0:
                dict1={}
                cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                goods_id = cur.fetchone()["auction_order_goods_id"]

                cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                            [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                            [goods_id])
                attribute = cur.fetchone()
                cur.execute("select * from t_auction_order where auction_order_goods_id=%s",[i["auction_order_id"]])
                order_messge = cur.fetchone()
                cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s", [i["auction_order_id"]])
                the_goods_state = cur.fetchone()["the_goods_state"]
                if the_goods_state:
                    dict1["state"] = the_goods_state
                else:
                    dict1["state"] ="待发货"
                dict1["goods"] = goods_message
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295
            #这里表示超过时间没有支付尾款的
            if order_state==1:
                pass
            #这里表示支付完成的
            if order_state==2:
                pass
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])

    goods_list.append(cur.fetchone()["auction_goods_id"])
    for i in goods_list:
        cur.execute("select * from t_auction_goods where auction_goods_id=%s", [i])
        info = cur.fetchone()
        goods_info_list.append(info)
    list4 = []
    for i in range(len(goods_record_list)):
        dict1 = {}
        dict1["record"] = goods_record_list[i]
        dict1["goods"] = goods_info_list[i]
        list4.append(dict1)


        dict1 = {}
        dict1["record"] = goods_record_list[i]
        dict1["goods"] = goods_info_list[i]

    for i in range(len(goods_record_list)):
        dict1 = {}
        dict1["record"] = goods_record_list[i]
        dict1["goods"] = goods_info_list[i]
<<<<<<< HEAD
            dict1["attribute"] = attribute
            dict1["order"] = order_messge
            list3.append(dict1)
        #这里表示支付完成的
        if order_state==1:
            dict1 = {}
            cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                        [i["auction_order_id"]])
            goods_id = cur.fetchone()["auction_order_goods_id"]
=======
>>>>>>> 5bd55ac73206ca4960e0b4ed17efbadfd14be180

        list4.append(dict1)

>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295

            cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                        [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                        [goods_id])
            attribute = cur.fetchone()
            cur.execute("select * from t_auction_order where auction_order_goods_id")
            order_messge = cur.fetchone()
            cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s",[i["auction_order_id"]])
            the_goods_state = cur.fetchone()["the_goods_state"]
            if the_goods_state==0:
                dict1["state"]="待发货"
            else:
                dict1["state"]=the_goods_state
            dict1["goods"] = goods_message
            dict1["attribute"] = attribute
            dict1["order"] = order_messge
            list5.append(dict1)
        #收货完成交易成功
        if order_state==2:
            dict1 = {}
            cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                        [i["auction_order_id"]])
            goods_id = cur.fetchone()["auction_order_goods_id"]


<<<<<<< HEAD
            cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                        [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_order where auction_order_goods_id")
            order_messge = cur.fetchone()
            cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s",
                        [i["auction_order_id"]])
            dict1["goods"] = goods_message
=======
                cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                            [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select * from t_auction_order where auction_order_goods_id")
                order_messge = cur.fetchone()
                cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                dict1["goods"] = goods_message
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295

            dict1["order"] = order_messge
            list6.append(dict1)
            pass
        print(list6)
<<<<<<< HEAD

=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295
    dict1 = {}
    dict1["record"] = goods_record_list[i]
    dict1["goods"] = goods_info_list[i]
    list4.append(dict1)
    print(list4)
<<<<<<< HEAD

=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295

        return render(request, 'my_auction_four.html', locals())


# ******************************************购买拍卖页面**********************************************


# 用户点击相应的商品图片或者竞拍按钮进入到商品的购买详情页
def buy_auction(request):
    id = request.session.get('user_id')
    dict1 = {}
    list1 = []
    if id:
        cur.execute('select user_name from t_user where user_id=%s', [id])
        username = cur.fetchone()
        print(username)
        goods_id = request.GET.get("id")
        cur.execute("select * from t_auction_goods where auction_goods_id=%s ", [goods_id])
        goods_messge = cur.fetchone()
        goods_user_id = goods_messge["auction_goods_user_id"]
        cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
        goods_auction_message = cur.fetchone()
        dict1["goods"] = goods_messge
        dict1["attribute"] = goods_auction_message
        list1.append(dict1)
        return render(request, 'buy_auction.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# ***********************************************计算拍卖的总价******************************************************
def calculate_price(request):

    price = request.POST.get('old_price')
    permium = request.POST.get('permium')
    floormium = request.POST.get("floormium")
    goods_user_id = request.POST.get("goods_user_id")
    floorprice = request.POST.get("floorprice")
    id = request.session.get("user_id")
    print(floormium, permium, floorprice)
    if int(permium) < int(floormium) or int(permium) > int(floorprice):
        return HttpResponse("你输入的加价有误")
    if int(id) == int(goods_user_id):
        return HttpResponse("不可购买自己的商品")  # 判断商品的发布者id和当前用户的id是不是一样

    price = request.POST.get('price')
    permium = request.POST.get('permium')
    floormium = request.POST.get("floormium")
    print(price)
    print(permium)
    if permium < floormium or permium > price:

        pass

        return HttpResponse("输入的加价有误")

    else:
        count_price = int(price) + int(permium)
        return HttpResponse(count_price)

# 购买拍卖页面
def buy_auction(request):
    id = request.session.get('user_id')
    dict1 = {}
    list1 = []
    if id:
        cur.execute('select user_name from t_user where user_id=%s', [id])
        username = cur.fetchone()
        print(username)
        goods_id = request.GET.get("id")
        cur.execute("select * from t_auction_goods where auction_goods_id=%s ", [goods_id])
        goods_messge = cur.fetchone()
        goods_user_id = goods_messge["auction_goods_user_id"]
        cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
        goods_auction_message = cur.fetchone()
        dict1["goods"] = goods_messge
        dict1["attribute"] = goods_auction_message
        list1.append(dict1)
        return render(request, 'buy_auction.html', locals())
    else:
        return HttpResponseRedirect('/login/')

# ******************************************用户输入价格完成确认竞拍*********************************************
# 这里主要是对用户输入的支付密码做判断，然后在对表进行更新插入

def confirm_buy(request):
    buy_user_id = request.session.get("user_id")  # 用户的
    floorprice = request.POST.get("floorprice")  # 商品的底价
    old_price = request.POST.get("old_price")  # 商品被这个用户竞拍前的价格
    print(old_price)
    goods_id = request.POST.get("goods_id")  # 商品的id
    price = request.POST.get("price")  # 商品加价现在的价格
    permium = request.POST.get("permium")  # 商品的加价
    margin = request.POST.get("margin")  # 商品的保证金
    cur.execute("select user_money from t_user where user_id=%s", [buy_user_id])
    user_money = cur.fetchone()["user_money"]
    cur.execute("select auction_goods_count from t_auction_attribute where auction_goods_id=%s", [goods_id])
    auction_goods_count = cur.fetchone()["auction_goods_count"]
    pay_password = request.POST.get("pay_password")
    global error
    cur.execute("select user_pay_password from t_user where user_id=%s", [buy_user_id])
    user_pay_password = cur.fetchone()["user_pay_password"]
    if user_pay_password:
        if pay_password:
            if len(pay_password) < 6:
                error = "pay_password_length"
                return HttpResponse(json.dumps({"msg": error}))
            elif int(pay_password) != int(user_pay_password):
                error = "diferent_password"
                return HttpResponse(json.dumps({"msg": error}))
            # 当用户输入的密码正确的时候做的判断
            else:
                if float(user_money) < float(margin):
                    error = "money_less"
                    return HttpResponse(json.dumps({"msg": error}))
                else:
                    try:
                        cur.execute(
                            "select auction_goods_buyuser_id from t_auction_attribute where auction_goods_id=%s",
                            [goods_id])
                        goods_buyuser_id = cur.fetchone()["auction_goods_buyuser_id"]
                        # 判断这个商品有没有人竞拍过
                        if goods_buyuser_id:
                            # 如果这个商品上一个竞拍者和现在的竞拍者是相同的话不能进行拍卖
                            if int(goods_buyuser_id) == (buy_user_id):
                                error = "same_user_buy"
                                return HttpResponse(json.dumps({"msg": error}))
                            else:
                                # 这里是先把当前竞拍者的保证金扣掉
                                new_user_money = float(user_money) - float(margin)
                                cur.execute("update t_user set user_money=%s where user_id=%s",
                                            [new_user_money, buy_user_id])
                                print("扣钱成功")
                                # 这里是将上一个竞拍者的保证金退给他
                                cur.execute("select user_money from t_user where user_id=%s", [goods_buyuser_id])
                                return_money = cur.fetchone()["user_money"] + float(margin)
                                cur.execute("update t_user set user_money=%s where user_id=%s",
                                            [return_money, goods_buyuser_id])
                                print("退钱成功")
                                # 更新拍卖商品的属性
                                auction_goods_count += 1
                                cur.execute(
                                    "update t_auction_attribute set auction_goods_count=%s,auction_goods_price=%s,auction_goods_buyuser_id=%s where auction_goods_id=%s",
                                    [auction_goods_count, price, buy_user_id, goods_id])
                                print("更新成功")
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295

                                cur.execute(
                                    "select auction_record_id from t_auction_record where auction_goods_id=%s",
                                    [goods_id])


                                cur.execute(
                                    "select auction_record_id from t_auction_record where auction_goods_id=%s",
                                    [goods_id])

                                cur.execute("select auction_record_id from t_auction_record where auction_goods_id=%s",
                                            [goods_id])

                                cur.execute(
                                    "select auction_record_id from t_auction_record where auction_goods_id=%s",
                                    [goods_id])

                                record_dict = cur.fetchall()
                                if record_dict:
                                    record_list = []
                                    for i in record_dict:
                                        record_list.append(i["auction_record_id"])
                                    record_maxid = max(record_list)
                                    cur.execute(
                                        "update t_auction_record set auction_goods_state=%s where auction_record_id=%s",
                                        ['0', record_maxid])

                                # 更新商品的拍卖属性以后需要生成一条拍卖记录
                                cur.execute("insert into t_auction_record (auction_goods_id,auction_goods_premium,auction_goods_floorprice,auction_goods_price,auction_goods_count,\
                                                            auction_goods_buyuser_id,auction_goods_oldprice)values (%s,%s,%s,%s,%s,%s,%s)",
                                            [goods_id, permium, floorprice, price, auction_goods_count, buy_user_id,
                                             old_price])
                                print("插入拍卖记录成功")

                        else:  # 如果上一个竞拍者的id不存在
                            new_user_money = float(user_money) - float(margin)
                            cur.execute("update t_user set user_money=%s where user_id=%s",
                                        [new_user_money, buy_user_id])
                            print("扣钱成功2")
                            # 更新拍卖商品的属性
                            auction_goods_count += 1
                            cur.execute(
                                "update t_auction_attribute set auction_goods_count=%s,auction_goods_price=%s,auction_goods_buyuser_id=%s where auction_goods_id=%s",
                                [auction_goods_count, price, buy_user_id, goods_id])
                            print("更新拍卖成功2")
                            # 更新商品的拍卖属性以后需要生成一条拍卖记录
                            cur.execute("insert into t_auction_record (auction_goods_id,auction_goods_premium,auction_goods_floorprice,auction_goods_price,auction_goods_count,\
                            auction_goods_buyuser_id,auction_goods_oldprice)values (%s,%s,%s,%s,%s,%s,%s)",
                                        [goods_id, permium, floorprice, price, auction_goods_count, buy_user_id,
                                         old_price])
                            print("插入记录成功2")
                        con.commit()
                        print("竞拍成功")

                    except Exception as e:
                        print(e)

                    error = "pay_ok"
                    return HttpResponse(json.dumps({"msg": error}))

        else:
            error = "no_pay_password"
            return HttpResponse(json.dumps({"msg": error}))
    else:
        error = "no_user_password"
        return HttpResponse(json.dumps({"msg": error}))


# ****************************************************************用户竞拍成功******************************************



def buy_auction_ok(request):
    return render(request, 'buy_auction_goods_ok.html')

<<<<<<< HEAD
=======

>>>>>>> f4d504ed34f968dcb3ffc7488120befed846cd42
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295

#**********************************************************提前结束拍卖*************************************************
def end_auction(request):
    user_id=request.session.get("user_id")
    goods_id=request.GET.get("id")
    print(user_id)
    print("商品id",goods_id)
    cur.execute("select ")
    cur.execute(
        "select auction_record_id from t_auction_record where auction_goods_id=%s",
        [goods_id])
    record_dict = cur.fetchall()
    #在用户自己结束拍卖的时候还有人竞拍
    if record_dict:
        if record_dict:
            record_list = []
            for i in record_dict:
                record_list.append(i["auction_record_id"])
            record_maxid = max(record_list)
        #找到开始竞拍的用户给退回保证金
        cur.execute("select auction_goods_buyuser_id from t_auction_record where auction_record_id=%s",[record_maxid])
        buy_user_id=cur.fetchone()["auction_goods_buyuser_id"]
        user_money=cur.execute("select user_money from t_user where user_id=%s",[buy_user_id])
        user_money+=30
        try:
            cur.execute("update t_user set user_money=%s where user_id=%s",[user_money,user_id])
            #将原来商品里面记录删除
            cur.execute("delete from t_auction_goods where auction_goods_id=%s", [i])
            print("删除成功")
            #将拍卖记录表里面的状态改变
            cur.execute(
            "update t_auction_record set auction_goods_state=%s where auction_record_id=%s",
            ['0', record_maxid])
            #将商品里面的状态改成5，表示已经下架
            cur.execute("update t_auction_goods_record set auction_goods_state =%s where auction_goods_id=%s",
                        ["5", i])
            con.commit()
        except Exception as e:
            print(e)
    else:
        cur.execute("delete from t_auction_goods where auction_goods_id=%s", [goods_id])
        # 将商品里面的状态改成5，表示已经下架
        cur.execute("update t_auction_goods_record set auction_goods_state =%s where auction_goods_id=%s",
                    ["5", goods_id])
        print("删除成功")

        con.commit()
    return redirect("/my_auction_one/")



# ****************************************************************用户竞拍成功******************************************






<<<<<<< HEAD

=======
>>>>>>> ccb563351bdee7d4f655dd64f295a1a062ae7295

#********************************************************************普通商品购买***************************************
def goods_confirm_buy(request):
    error=""
    price=request.POST.get("price")
    user_id=request.session.get("user_id")
    pay_password=request.POST.get("pay_password")
    goods_id=request.POST.get("goods_id")
    cur.execute("select user_pay_password,user_money from t_user where user_id=%s",[user_id])
    user_message=cur.fetchone()
    user_pay_password=user_message["user_pay_password"]
    user_money=user_message["user_money"]
    print(price,user_money)
    if user_pay_password:
        if len(pay_password)<6:
            error = "pay_password_length_error"
            return HttpResponse(json.dumps({"msg": error}))
        elif int(pay_password)!=int(user_pay_password):
            error="pay_password_error"
            return HttpResponse(json.dumps({"msg": error}))
        elif float(user_money)<float(price):
            error="money_less_error"
            return HttpResponse(json.dumps({"msg": error}))
        else:
            #购买完成，更新数据库和生成订单扣款等
            try:
                #先扣除购买者的钱
                user_money=float(user_money)-float(price)
                cur.execute("update t_user set user_money=%s where user_id=%s",[user_money,user_id])
                print("扣钱成功")
                #生成商品订单
                cur.execute("select user_id from t_goods where goods_id=%s",[goods_id])
                release_user_id=cur.fetchone()["user_id"]
                date=time.strftime('%Y-%m-%d', time.localtime(time.time()))
                cur.execute("insert into t_order(release_user_id,buy_user_id,order_date,order_goods_id) values (%s,%s,%s,%s)",[str(release_user_id),str(user_id),date,str(goods_id)])
                print("生成订单成功")
                cur.execute("update t_goods set goods_state=%s where goods_id=%s",["1",goods_id])
                print("更新商品状态成功")
                con.commit()
                error = "pay_ok"
                return HttpResponse(json.dumps({"msg": error}))

            except Exception as e:
                print(e)
    else:
        error="no_pay_password"
        return HttpResponse(json.dumps({"msg": error}))



#用户输入支付密码扣款完成
def buy_goods_ok(request):
    return render(request,"buy_goods_ok.html")

# ****************************************************************用户竞拍成功******************************************
def buy_auction_ok(request):
    return render(request, 'buy_auction_goods_ok.html')


# 我出售的
@login_required
def my_sale(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    # 发布中的商品------------------------------
    cur.execute(
        'select * from t_goods  where user_id=%s and goods_state=%s order by goods_id desc',
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


# my_sale 户中心商品下架——ajax: 待修改
@login_required
def user_lower_goods(request):
    goods_id = request.POST.get("goods_id")
    user_id = request.session.get('user_id')
    try:
        # 下架商品-------------------
        cur.execute("update t_goods set goods_state=%s where goods_id=%s", ['2', goods_id])
        con.commit()
        # ---页面拼接---------------------------
        cur.execute("select * from t_goods  where user_id=%s and goods_state=%s order by goods_id desc",
                    [user_id, 0])
        goods_list = cur.fetchall()
        print(goods_list)
        a = 0
        if goods_list:
            for item in goods_list:
                if item["goods_id"] == int(goods_id):
                    a = goods_list.index(item) + 3
            try:
                goods_list_ = goods_list[a]
                print(4444444444444444444, goods_id, goods_list_, a)
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
                                    <td width="15%"><input type="button" class="lower1_btn lower_{11}"
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
                return HttpResponse(json.dumps({"msg": msg, "html": html}))
            except:
                msg = "flash"
                href = "/my_sale/"
                return HttpResponse(json.dumps({"msg": msg, "href": href}))
    except:
        msg = "error"
        href = "/my_sale/"
        return HttpResponse(json.dumps({"msg": msg, "href": href}))


# 我的出售，上下架页面
@login_required
def my_sale_lower(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
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


# ******************************************************************我购买的*******************************************
def my_buy(request):
    user_id=request.session.get("user_id")
    list1=[]
    #找到该用户的所有订单号,已经订单号里面的商品id
    cur.execute("select order_id,order_goods_id from t_order where  buy_user_id=%s",[user_id])
    order_dict=cur.fetchall()
    if order_dict:
        order_id_list=[]
        goods_id_list=[]
        for i in order_dict:
            order_id_list.append(i["order_id"])
            goods_id_list.append(i["order_goods_id"])
        for i in range(len(order_id_list)):
            dict1={}
            cur.execute("select * from t_order where  order_id=%s", [order_id_list[i]])
            order_message=cur.fetchone()
            cur.execute("select * from t_goods where goods_id=%s",[goods_id_list[i]])
            goods_message=cur.fetchone()
            dict1["goods"]=goods_message
            dict1["order"]=order_message
            list1.append(dict1)


    return render(request, 'my_buy.html',locals())


# 我的收藏
def my_collection(request):
    username = request.session.get('username')  # 获取买家用户名
    user_id = request.session.get('user_id')  # 获取买家ID
    goods_id = request.GET.get('goods')
    # 商品收藏------------------------------------------
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s limit 5 ',
        [user_id, ])
    collection_list = cur.fetchall()
    print(collection_list, 45454544885454545554545)
    # -----------------------------------
    return render(request, 'my_collection.html', locals())


# 评价
def evaluate(request):
    username = request.session.get('username')  # 获取买家用户名
    user_id = request.session.get('user_id')  # 获取买家ID
    goods_id = request.GET.get('goods_id')
    customer = request.GET.get("customer")
    print("evaluate", "------", username, user_id, goods_id)
    # 商品收藏------------------------------------------
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s ',
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
    # 判断买卖家
    if customer == "buy":
        # --本商品是否已经评价-------------------
        cur.execute("select * from t_order_success where order_goods_id=%s", [goods_id, ])  # 获取商品表内容
        order_id_ = cur.fetchone()
        print(44444444444, order_id_, user_id, username, goods_id, customer)
        order_id = order_id_["order_id"]
        eva_state = order_id_["buy_eva_state"]
        print()
        if eva_state != 0:
            cur.execute("select * from t_evaluation where evaluation_order_id=%s", [order_id, ])
            buy_desc_list = cur.fetchone()
    else:
        print(customer)
        cur.execute("select * from t_order_success where order_goods_id=%s", [goods_id, ])  # 获取商品表内容
        eva_state = cur.fetchone()["buy_eva_state"]
        order_id = cur.fetchone()["order_id"]

        if eva_state != 0:
            cur.execute("select * from t_evaluation where evaluation_order_id=%s", [order_id, ])
            sell_desc_list = cur.fetchone()
            print(4444444, customer, eva_state, order_id, sell_desc_list)
    return render(request, 'evaluate.html', locals())


def evaluate_ajax(request):
    evaluate_text = request.POST.get('evaluate_text')
    dddddddd = request.POST.get('dddddddd')
    customer = request.POST.get('customer')
    order_id = request.POST.get('order_id')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    if customer == "buy":
        cur.execute(
            "update t_evaluation set buyer_evaluation_date = %s,buyer_desc=%s,buy_state=%s where evaluation_order_id = %s",
            [now_time, evaluate_text, dddddddd, order_id])
    else:
        cur.execute(
            "update t_evaluation set seller_evaluation_date = %s,seller_desc=%s,sell_state=%s where evaluation_order_id = %s",
            [now_time, evaluate_text, dddddddd, order_id])
    con.commit()
    msg = "success"

    return HttpResponse(json.dumps({"msg": msg}))


# 我收到的评价
def my_evaluate_get(request):
    return render(request, 'my_evaluate_get.html')


# 给他人的评价
def my_evaluate_give(request):
    return render(request, 'my_evaluate_give.html')


# 收到的回复
@login_required
def leave_message(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
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
def leave_message_two(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
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


# 修改信息
def modify_information(request):
    if request.method == 'GET':
        return render(request, 'modify_information.html')
    else:
        nickname = request.POST.get('nickname')
        shen = request.POST.get('cmbProvince')
        shi = request.POST.get('cmbCity')
        xian = request.POST.get('cmbArea')
        img = request.POST.get('img')
        date = request.POST.get('date')
        sex = request.POST.get('sex')
        print(nickname, shen, shi, xian, img, date, sex)

        imgurl = "pgwecu7z4.bkt.clouddn.com/" + img
        print(imgurl)
        return render(request, 'modify_information.html')


def modify_password(request):
    return render(request, 'modify_password.html')


def callback(request):
    if request.method == 'GET':
        key_json_base64 = request.GET.get('upload_ret')
        key_json = base64.b64decode(key_json_base64).decode('utf-8')
        print(key_json)
        key_dict = json.loads(key_json)
        key = key_dict['key']
        return HttpResponse('pgwecu7z4.bkt.clouddn.com/' + key + '-haima.shuiy')


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


#******************************************************判断拍卖时间************************************************
def Determine_auction_date(request):
    cur.execute("select auction_goods_id  from t_auction_goods")
    list_goods_id=[]
    dict_goods_id=cur.fetchall()
    for i in dict_goods_id:
        list_goods_id.append(i["auction_goods_id"])
    #对现在的商品的id进行遍历
    for i in list_goods_id:
        cur.execute("select end_date from t_auction_attribute where auction_goods_id=%s",[i])
        end_date=cur.fetchone()["end_date"]
        now_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        print(end_date)
        print(now_date)
        #如果现在的时间已经到了拍卖结束时间
        if now_date>end_date:
            try:
                cur.execute("select auction_goods_user_id from t_auction_goods_record where auction_goods_id=%s",[i])
                user_id=cur.fetchone()["auction_goods_user_id"]
                #退回保证金
                cur.execute("select user_money from t_user where user_id=%s", [user_id])
                user_money=cur.fetchone()["user_money"]
                user_money+=30
                cur.execute("update t_user set user_money=%s where user_id=%s",[user_money,user_id])
                print("退回保证金成功")
                #删除原来的商品
                cur.execute("delete from t_auction_goods where auction_goods_id=%s",[i])
                print("删除成功")
                #判断商品当前有没有人竞拍
                cur.execute("select auction_goods_buyuser_id,auction_goods_price from t_auction_attribute where auction_goods_id=%s",[i])
                x=cur.fetchone()
                who_buy=x["auction_goods_buyuser_id"]
                print(type(who_buy))
                price=x["auction_goods_price"]
                print(price)
                if str(who_buy)=='0':
                    print("没有人竞拍")
                    #1商品流拍
                    state = "1"
                    cur.execute("update t_auction_goods_record set auction_goods_state =%s where auction_goods_id=%s",
                                [state, i])
                    print("修改商品的状态成功")
                else:
                    #2商品有人竞拍
                    state = "2"
                    cur.execute("update t_auction_goods_record set auction_goods_state =%s where auction_goods_id=%s",
                                [state, i])
                    print("修改商品的状态成功")
                    #将拍卖记录里面的状态修改
                    cur.execute(
                        "select auction_record_id from t_auction_record where auction_goods_id=%s",
                        [i])
                    record_dict = cur.fetchall()
                    if record_dict:
                        record_list = []
                        for i in record_dict:
                            record_list.append(i["auction_record_id"])
                        record_maxid = max(record_list)
                        cur.execute(
                            "update t_auction_record set auction_goods_state=%s where auction_record_id=%s",
                            ['2', record_maxid])
                    cur.execute("update t_auction_record set auction_goods_state =%s where auction_goods_id=%s",
                                [state, i])
                    print("修改商品的状态成功")
                    cur.execute("insert into t_auction_order (auction_order_date,auction_order_goods_id,auction_order_fianl_price,\
                                auction_order_buy_user_id) values (%s,%s,%s,%s)",[now_date,str(i),str(price),str(who_buy)])
                    print("添加订单成功")
                con.commit()


            except Exception as e:
                print(e)

    return redirect("/auction_index/")

#***********************************************普通商品确认收货*************************************************
def confirm_goods(request):
    goods_id=request.POST.get("goods_id")
    cur.execute("select * from t_order where order_goods_id=%s",[goods_id])
    goods_message=cur.fetchone()
    date=datetime.datetime.now().strftime('%Y-%m-%d')
    print(goods_message)
    #把信息加到订单成功表：然后删除原来订单表里的数据
    try:
       cur.execute("insert into t_order_success (release_user_id,buy_user_id,order_date,order_goods_id) values (%s,%s,%s,%s\
                      )",[str(goods_message["release_user_id"]),str(goods_message["buy_user_id"]),date,str(goods_id)])
       cur.execute("delete from t_order where order_goods_id=%s",[str(goods_id)])
       #用户确认收货以后需要把卖家的钱增加
       cur.execute("select goods_price from t_goods where goods_id=%s",[goods_id])
       goods_price=cur.fetchone()["goods_price"]
       cur.execute("select user_money from t_user where user_id=%s",[goods_message["release_user_id"]])
       user_money=cur.fetchone()["user_money"]
       user_money=user_money+goods_price
       cur.execute("update t_user set user_money=%s where user_id=%s",[user_money,goods_message["release_user_id"]])
       print("ok")
    except Exception as e:
        con.rollback()
        print(e)
    con.commit()
    return HttpResponse(json.dumps({"msg": "123"}))

#***********************************************拍卖商品竞拍成功后，支付尾款********************************************
def pay_auction_money(request):
    error=""
    buy_user_id=request.session.get("user_id")
    order_id=request.POST.get("order_id")
    print(order_id)
    cur.execute("select auction_order_fianl_price from t_auction_order where auction_order_id=%s",[order_id])
    order_price=cur.fetchone()["auction_order_fianl_price"]
    print(order_price)
    cur.execute("select user_money from t_user where user_id=%s",[buy_user_id])
    user_money=cur.fetchone()["user_money"]
    print(user_money)
    #通过订单id找到商品id
    cur.execute("select auction_order_goods_id from t_auction_order where  auction_order_id=%s",[order_id])
    goods_id=cur.fetchone()["auction_order_goods_id"]
    #通过商品id找到保证金
    cur.execute("select auction_goods_margin from t_auction_attribute where auction_goods_id=%s",[goods_id])
    goods_margin=cur.fetchone()["auction_goods_margin"]
    #这里是用户输入的账号密码
    pay_password=request.POST.get("pay_password")
    cur.execute("select user_pay_password from t_user where user_id=%s", [buy_user_id])
    user_pay_password = cur.fetchone()["user_pay_password"]

    #先判断有没有输入支付密码：
    if pay_password:
        if len(pay_password) < 6:
            error = "pay_password_length_error"
            return HttpResponse(json.dumps({"msg": error}))
        elif int(user_pay_password) != int(pay_password):
            error = "pay_password_error"
            return HttpResponse(json.dumps({"msg": error}))
        elif float(user_money) < float(order_price):
            error = "money_less_error"
            return HttpResponse(json.dumps({"msg": error}))
        #用户账号正确而且余额足够
        else:
            print("进入支付操作")
            error="ok"
            try:
                user_money=user_money-order_price+goods_margin
                #付款以后把他的钱扣掉把保证金退还
                cur.execute("update t_user set user_money=%s where user_id=%s",[user_money,buy_user_id])
                #将订单那个状态改成1
                cur.execute("update t_auction_order set auction_order_state=%s where auction_order_id=%s",["1",order_id])
                #将商品记录表里的状态改成3,付款时间也改一下
                now_time = datetime.datetime.now().strftime('%Y-%m-%d')
                cur.execute("update t_auction_goods_record set auction_goods_state=%s,pay_monet_date=%s where  auction_goods_id=%s",["3",now_time,goods_id])

                print("操作完成")
            except Exception as e:
                print(e)
            con.commit()
            error="pay_ok"
            return HttpResponse(json.dumps({"msg": error}))

    else:
        print("无密码")
        error="no_pay_password"
        return HttpResponse(json.dumps({"msg": error}))


#********************************************返回支付拍卖成功的钱以后的跳转*********************************************
def  pay_auction_money_ok(request):
    return render(request,"pay_auction_money_ok.html")

#*****************************************处理拍卖商品的发货************************************************************
def delivery(request):
    courier_number=request.POST.get("courier_number")
    order_id=request.POST.get("order_id")
    try:
        cur.execute("update t_auction_order set the_goods_state=%s where auction_order_id=%s",[courier_number,order_id])
        con.commit()
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps({"msg": "ok"}))


#*********************************************拍卖商品的收货*******************************************************
def confirm_auction_goods(request):
    order_id=request.POST.get("order_id")
    #用户确认收货以后改变状态
    try:
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        cur.execute("update t_auction_order set auction_order_state=%s,order_success_date=%s where auction_order_id=%s",["2",now_date,order_id])
        cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",[order_id])
        auction_goods_id=cur.fetchone()["auction_order_goods_id"]
        #用户确认收货以后需要把钱打到卖家账户
        cur.execute("select auction_goods_user_id from t_auction_goods_record where auction_goods_id=%s",[auction_goods_id])
        maijia_id=cur.fetchone()["auction_goods_user_id"]
        cur.execute("update t_auction_goods_record set auction_goods_state=%s where auction_goods_id=%s", ["4", auction_goods_id])
        con.commit()
    except Exception as e:
        print(e)