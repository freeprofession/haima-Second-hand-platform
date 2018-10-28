import pymysql
import redis

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import base64



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


def homepage(request):
    username = request.session.get('username')
    if username:
        login_status = username
    else:
        login_status = ''
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

# 搜索
def search(request):
    return render(request,)

# 用户中心
def user_center(request):
    username = request.session.get('username')
    print(username)
    if username:
        cur.execute("select * from t_user where user_name=%s", [username, ])
        user_info = cur.fetchall()
        print(user_info)
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


# 回复处理，留言板
def review_ajax(request):
    # ------接受值———————————
    child_review = request.POST.get('child_review')
    rp_user_id = request.POST.get('reply_id')
    message_id = request.POST.get('message_id')
    # parent_id = request.POST.get("parent_id")
    # goods_id = request.POST.get("goods_id")
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    print(" # ------接受值———————————")
    print(child_review, rp_user_id, message_id, username, user_id)
    cur.execute("select * from t_message where message_id=%s", [message_id, ])
    message_id_list = cur.fetchone()
    print(message_id_list)
    message_id = message_id_list["message_id"]
    goods_id = message_id_list["message_goods_id"]

    # 判断登陆状态----------------
    if user_id:
        login_state = username
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        cur.execute("select * from t_second_message where second_message_id=%s", [rp_user_id, ])
        check_child_name_ = cur.fetchone()
        reply_id1 = check_child_name_["child_user_id"]
        cur.execute("select * from t_user where user_id=%s", [reply_id1, ])
        check_child_name_2 = cur.fetchone()
        # check_child_name = check_child_name_['user_name']
        if child_name and check_child_name_2 and check_child_name_2:
            print("判断用户名", child_name[0], check_child_name_2['user_name'])
            if check_child_name_2['user_name'] == child_name[0]:
                rule2 = r':(.*)'
                print('ture')
                send_review = "@" + child_name[0] + re.findall(rule2, child_review)[0] + ":"
                reply_id = reply_id1
            else:
                send_review = child_review
                cur.execute("select * from t_message where message_id=%s", [message_id, ])
                reply_id__ = cur.fetchone()
                reply_id = reply_id__["message_user_id"]
        else:
            send_review = child_review
            cur.execute("select * from t_message where message_id=%s", [message_id, ])
            reply_id__ = cur.fetchone()
            reply_id = reply_id__["message_user_id"]
        # 储存数据
        user_id_ = str(user_id)
        print(send_review, goods_id, now_time, user_id, rp_user_id)
        # print(type, type(send_review), type(goods_id), type(now_time), type(user_id_), type(rp_user_id))
        cur.execute(
            "insert into t_second_message(parent_user_id,second_desc,second_goods_id,second_date,child_user_id,to_rid) value(%s,%s,%s,%s,%s,%s)",
            [message_id, send_review, goods_id, now_time, user_id_, reply_id])
        second_message_id = cur.lastrowid
        conn.commit()
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


def goods_detail_ajax(request):
    pass


def search(request):
    global b
    if request.method == "GET":
        return render(request, "search.html")
    else:
        one = request.POST.get("search_one")
        print(one)
        # 数据库操作获取ID
        id = '1'
        b = '/goods_detail/?goods=' + id
        print(b)
        return redirect("/tiaozhuan/")

# 商品分类展示
def goods_list(request):
    return render(request, 'goods_list.html')


# 发布商品
def publish(request):
    return render(request, 'publish.html')

# 估价
def assess(request):
    return render(request, 'assess.html')


# 拍卖首页
def auction_index(request):

    id = request.session.get('user_id')
    print(id)
    list1=[]
    if id:
        goods_list=[]
        cur.execute('select user_name from t_user where user_id=%s',[id])
        username=cur.fetchone()
        cur.execute("select auction_goods_id from t_auction_goods")
        goods_dict=cur.fetchall()
        #先将需要在首页展示的拍卖商品的id全部拿出来存进一个列表里
        for i in goods_dict:
            goods_list.append(i["auction_goods_id"])
        #对这个需要展示的商品id进行遍历，将他需要展示的数据全部一条一条的拿出来
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
        print(username)
        print(username["user_name"])
        print(list1)
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


        return render(request, 'histroy_auction.html',locals())
    else:
        return HttpResponseRedirect('/login/')


# ********************************************我的拍卖********************************************************
#默认是进入用户的发布历史界面
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
        return render(request, 'my_auction.html', locals())
    else:
        return HttpResponseRedirect('/login/')

# ******************************************发布拍卖*****************************************
#进入发布拍卖页面就是把他的名字显示出来
def release_auction(request):
    id = request.session.get('user_id')
    if id:
        cur.execute('select user_name from t_user where user_id=%s', [id])
        username = cur.fetchone()
        return render(request, 'release_auction.html', locals())
    else:
        return HttpResponseRedirect('/login/')


#*****************************************发布拍卖提交处理*************************************
#用户点击发布拍卖的时候的逻辑判断和数据库操作


def publish_auction(request):
    global error
    user_id= request.session.get('user_id')
    if request.method == 'POST':

        title=request.POST.get('title')
        desc= request.POST.get('desc')
        floorprice= request.POST.get('floorprice')
        floorpremium=request.POST.get("floorpremium")
        end_date=request.POST.get("end_date")
        start_date=request.POST.get("start_date")
        category=request.POST.get("category")
        postage=request.POST.get("postage")
        list1=[]
        date_now=datetime.datetime.now().strftime('%Y-%m-%d')
        if title and desc and floorpremium and floorprice and end_date and start_date and category and postage:
            if len(title)>=6 and floorpremium < floorprice and  str(floorprice).isdigit()==True and str(floorpremium).isdigit()==True\
                    and start_date==date_now:
                error="ok"

                cur.execute("insert into t_auction_goods(auction_goods_title,auction_goods_desc,auction_goods_imgurl,\
                            auction_goods_user_id,auction_goods_category_id) values(%s,%s,%s,%s,%s)",[title,desc,"http://pic.qiantucdn.com/58pic/18/56/71/03k58PICiRc_1024.jpg",\
                             str(user_id),str(postage)])
                print("插入到拍卖商品表可以成功")
                goods_id=cur.lastrowid
                cur.execute("insert into t_release_auction(release_auction_date,release_auction_goods_id,release_auction_user_id) values (%s,%s,%s)"\
                            ,[date_now,str(goods_id),str(user_id)])
                print("插入到拍卖记录表成功")
                cur.execute("insert into t_auction_goods_record(auction_goods_title,auction_goods_desc,auction_goods_imgurl,\
                                                auction_goods_user_id,auction_goods_category_id) values(%s,%s,%s,%s,%s)",
                            [title, desc, "http://pic.qiantucdn.com/58pic/18/56/71/03k58PICiRc_1024.jpg", \
                             str(user_id), str(postage)])
                print("插入到商品记录表成功")
                cur.execute("insert into t_auction_attribute (start_date,end_date,auction_goods_floorprice,auction_goods_floorpremium,\
                            auction_goods_price,auction_goods_id) values (%s,%s,%s,%s,%s,%s)",[start_date,end_date,floorprice,floorpremium,floorprice,str(goods_id)])
                print("插入到拍卖属性表成功")
                conn.commit()
                print("over ")

                return HttpResponse(json.dumps({"msg": error}))

            elif len(title)<6:
                error='title.length_error'
                return HttpResponse(json.dumps({"msg": error}))
            elif start_date!=date_now:
                error = 'time_error'
                return HttpResponse(json.dumps({"msg": error}))
            elif str(floorprice).isdigit()==False or str(floorpremium).isdigit()==False:
                error='price_error'

                return HttpResponse(json.dumps({"msg": error}))
            elif int(floorpremium) >= int(floorprice):
                error = 'floorpremium_error'
                return HttpResponse(json.dumps({"msg": error}))

        else:
            error = 'less_error'
            return HttpResponse(json.dumps({"msg": error}))



#发布拍卖成功
def release_auction_ok(request):
    return render(request,'release_auction_ok.html')

#*******************************返回用户的发布记录**************************************
def my_release_record(request):
    return_title=request.GET.get("id") #根据传回来的id 来判断返回的值
    print(type(return_title))
    print(return_title)

    if return_title=="one":
        list1=[]
        user_id=request.session.get("user_id")
        print(user_id)
        cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s",[user_id])
        message=cur.fetchall()
        id_list=[]
        for i in message:
            id_list.append(i["release_auction_goods_id"])
        for goods_id in id_list:
            dict1={}
            cur.execute("select * from t_auction_goods where auction_goods_id=%s ",[goods_id])
            goods_messge =cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s",[goods_id])
            goods_auction_message =cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            #所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"]=goods_messge
            dict1["attribute"]=goods_auction_message
            print(goods_auction_message["auction_goods_floorprice"])
            list1.append(dict1)
        print("查询成功")
        return render(request, 'my_auction.html',locals())


#******************************************购买拍卖页面**********************************************
#用户点击相应的商品图片或者竞拍按钮进入到商品的购买详情页
def buy_auction(request):
    id = request.session.get('user_id')
    dict1={}
    list1=[]
    if id:
        cur.execute('select user_name from t_user where user_id=%s', [id])
        username = cur.fetchone()
        print(username)
        goods_id = request.GET.get("id")
        cur.execute("select * from t_auction_goods where auction_goods_id=%s ", [goods_id])
        goods_messge = cur.fetchone()
        goods_user_id=goods_messge["auction_goods_user_id"]
        cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
        goods_auction_message = cur.fetchone()
        dict1["goods"] = goods_messge
        dict1["attribute"] = goods_auction_message
        list1.append(dict1)
        print(list1)
        return render(request, 'buy_auction.html',locals())

    else:
        return HttpResponseRedirect('/login/')


#***********************************************计算拍卖的总价******************************************************
def calculate_price(request):
    price=request.POST.get('old_price')
    permium=request.POST.get('permium')
    floormium=request.POST.get("floormium")
    goods_user_id= request.POST.get("goods_user_id")
    floorprice=request.POST.get("floorprice")
    id=request.session.get("user_id")
    if permium<floormium or  permium> floorprice:
        return HttpResponse("你输入的加价有误")
    if int(id)==int(goods_user_id):
        return HttpResponse("不可购买自己的商品")#判断商品的发布者id和当前用户的id是不是一样
    else:
        count_price=int(price)+int(permium)
        return HttpResponse(count_price)

#******************************************用户输入价格完成确认竞拍*********************************************88
def confirm_buy(request):
    buy_user_id=request.session.get("user_id")
    print("购买者id：",buy_user_id)
    floorprice=request.POST.get("floorprice")
    old_price=request.POST.get("old_price")
    goods_id=request.POST.get("goods_id")
    price=request.POST.get("price")
    permium=request.POST.get("permium")
    pay_password=request.POST.get("pay_password")
    global error
    cur.execute("select user_pay_password from t_user where user_id=%s",[buy_user_id])
    user_pay_password=cur.fetchone()
    if buy_user_id:
        pass
    else:
        error="pay_password_error2"
        return HttpResponse(json.dumps({"msg": error}))
    if len(pay_password)<6:
        error="pay_password_error"
        return HttpResponse(json.dumps({"msg": error}))


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


# 我收到的评价
def my_evaluate_get(request):
    return render(request, 'my_evaluate_get.html')


# 给他人的评价
def my_evaluate_give(request):
    return render(request, 'my_evaluate_give.html')


# 宝贝留言
def leave_message(request):
    return render(request, 'leave_message.html')


# 修改信息
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
