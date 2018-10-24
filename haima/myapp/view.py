import pymysql
import redis
import base64

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
    # print(goods_list)
    return render(request, 'homepage.html', {'goods_list': goods_list})


# 登录
def login(request):
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
                href = request.session.get('href')
                print(href)
                error = "login_ok"
                if href:
                    pass
                else:
                    href = "/haima/"
                return HttpResponse(json.dumps({"msg": error, "href": href}))
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
    # print(code, phone)
    r.set(phone, code_, 60)
    return HttpResponse(code)


# 注册成功页面跳转
def register_ok(request):
    return render(request, "register_ok.html")


# 用户中心
def user_center(request):
    username = request.session.get('username')
    if username:
        cur.execute("select * from t_user where user_name=%s", [username, ])
        user_info = cur.fetchall()
        return render(request, 'user_center.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# 商品界面设置
def goods_detail(request):
    username = request.session.get('username')  # 获取买家用户名
    user_id = request.session.get('user_id')  # 获取买家ID
    goods_id = request.GET.get('goods')
    print(goods_id)  # 获取商品ID
    cur.execute("select * from t_goods where goods_id=%s", [goods_id, ])  # 获取商品表内容
    goods_list = cur.fetchall()  # 商品表内容
    print(username, user_id, goods_id, goods_list)
    seller_id = goods_list[0]['user_id']  # 获取卖家ID
    cur.execute("select * from t_user where user_id=%s", [seller_id, ])  # 获取卖家信息
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 记录当前时间
    print(username, user_id, goods_id, seller_id, now_time)
    goods_desc = goods_list[0]['goods_desc']  # 商品详细介绍
    cur.execute('select * from t_user right join t_message on user_id = message_user_id')
    message_list = cur.fetchall()  # 留言
    print(message_list)
    # ++++++++++++++++++++++++商品留言处理++++++++++++++++++++++++++++++
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
    print(p_comment_dict)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    if username:  # 登录后才记录，浏览记录
        cur.execute("select * from t_user_browse where browse_user_id=%s", [user_id, ])
        browse = cur.fetchone()
        if browse is None:
            login_status = username
            count = goods_list[0]['goods_browse_count']
            count += 1
            # 更新商品浏览次数
            cur.execute("update t_goods set goods_browse_count=%s where goods_id=%s", [count, goods_id])
        # 用户浏览记录
        cur.execute("insert into t_user_browse(browse_user_id,browse_date,browse_goods_id) value(%s,%s,%s) ",
                    [user_id, now_time, goods_id])
        conn.commit()
    else:
        login_status = '未登录'

    return render(request, "detail.html", locals())


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


def goods_detail_ajax(request):
    pass


# 商品分类展示
def goods_list(request):
    return render(request, 'goods_list.html')


# 发布商品
@get_token
def publish(request, token):
    return render(request, 'publish.html', {'token': token})


# 估价
def assess(request):
    return render(request, 'assess.html')


# 拍卖
def auction_index(request):
    return render(request, 'auction_index.html')


# 历史拍卖
def history_auction(request):
    return render(request, 'histroy_auction.html')


# 我的拍卖
def my_auction(request):
    return render(request, 'my_auction.html')


# 发布拍卖
def release_auction(request):
    return render(request, 'release_auction.html')


# 发布拍卖提交处理
def publish_auction(request):
    global error
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        floorprice = request.POST.get('floorprice')
        floorpremium = request.POST.get("floorpremium")
        end_date = request.POST.get("end_date")
        start_date = request.POST.get("start_date")
        category = request.POST.get("category")
        postage = request.POST.get("postage")
        list1 = []
        print(title, desc, floorprice, floorpremium, end_date, start_date, category, postage)
        if title and desc and floorpremium and floorprice and end_date and start_date and category and postage:
            if len(title) >= 6 and floorpremium < floorprice and str(floorprice).isdigit() == True and str(
                    floorpremium).isdigit() == True:
                error = "ok"
                try:
                    cursor.execute("insert into test_agoods(goods_title) values(%s)", [title])
                    new_id = cursor.lastrowid
                    con.commit()
                    sql = "insert into test_auction(auction_goods_id,auction_goods_title,auction_goods_desc,auction_goods_floorprice," \
                          "auction_goods_imgurl,auction_goods_floorpremium,auction_goods_startdate,auction_goods_enddate,auction_goods_margin,auction_goods_postage) " \
                          "values (%d,%s,%s,%d,%s,%d,%s,%s,%d,%d)", [new_id, title, desc, floorprice,
                                                                     "../static/Images/goods/goods003.jpg",
                                                                     floorpremium, start_date, end_date, 200,
                                                                     int(postage)]
                    cursor.execute(sql)
                    con.commit()
                except:
                    con.rollback()
                    error = "sql_error"
                    print("数据库插入错误！")
                return HttpResponse(json.dumps({"msg": error}))
            elif len(title) < 6:
                error = 'title.length_error'
                return HttpResponse(json.dumps({"msg": error}))
            elif str(floorprice).isdigit() == False or str(floorpremium).isdigit() == False:
                error = 'price_error'
                return HttpResponse(json.dumps({"msg": error}))
            elif int(floorpremium) >= int(floorprice):
                error = 'floorpremium_error'
                return HttpResponse(json.dumps({"msg": error}))

        else:
            error = 'less_error'
            return HttpResponse(json.dumps({"msg": error}))


# 发布拍卖成功
def release_auction_ok(request):
    return render(request, 'release_auction_ok.html')


# 用户中心
def user_center(request):
    return render(request, 'user_center.html')


# 我出售的
def my_sale(request):
    return render(request, 'my_sale.html')


# 我购买的
def my_buy(request):
    return render(request, 'my_buy.html')


# 我的收藏
def my_collection(request):
    return render(request, 'my_collection.html')


# 评价
def evaluate(request):
    return render(request, 'evaluate.html')


# 我的评价
def my_evaluate(request):
    return render(request, 'my_evaluate.html')


# 宝贝留言
def leave_message(request):
    return render(request, 'leave_message.html')


# 修改信息
def modify_information(request):
    return render(request, 'modify_information.html')


@get_token
def test_qiniu(request, token):
    return render(request, '7cow.html', {'token': token})


def callback(request):
    if request.method == 'GET':
        key_json_base64 = request.GET.get('upload_ret')
        key_json = base64.b64decode(key_json_base64).decode('utf-8')
        print(key_json)
        key_dict = json.loads(key_json)
        key = key_dict['key']
        print(key)
        return HttpResponse('pgwecu7z4.bkt.clouddn.com/' + key + '-haima.shuiy')
    else:
        # json_result = json.loads(postBody)
        # print(json_result)
        return HttpResponse("POST")
