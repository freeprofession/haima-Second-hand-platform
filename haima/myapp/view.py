import pymysql
import time
from utils.pay import AliPay

st_time = time.localtime(time.time())
loc_time = '{}-{}-{}'.format(st_time.tm_year, st_time.tm_mon, st_time.tm_mday)

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
from myapp import goods_recommend

r = redis.Redis(host="47.100.200.132", port=6379)
r1 = redis.Redis(host="47.100.200.132", port=6379, db=1)
img = redis.Redis(host="47.100.200.132", port=6379, db=2)
category = redis.Redis(host="47.100.200.132", port=6379, db=3)
cut_words = redis.Redis(host="47.100.200.132", port=6379, db=4)
auction_img = redis.Redis(host="47.100.200.132", port=6379, db=5)
sms = redis.Redis(host="47.100.200.132", port=6379, db=5)  # æ³¨åéªè¯ç ?
set_eva = redis.Redis(host="47.100.200.132", port=6379, db=7)  # è®¾ç½®è¯è®º
get_eva = redis.Redis(host="47.100.200.132", port=6379, db=8)  # å¾å°è¯è®º
search_record = redis.Redis(host="47.100.200.132", port=6379, db=9)  # ç¨æ·æç´¢è®°å½
goods_browse = redis.Redis(host="47.100.200.132", port=6379, db=10)  # æµè§è®°å½
history_auction = redis.Redis(host="47.100.200.132", port=6379, db=11)


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


# ç»å½ç¶ææ£æ¥ï¼è£é¥°å?
def login_required(function):
    def check_login_status(request):
        user_id = request.session.get('user_id')
        if user_id:
            return function(request)
        else:
            return HttpResponseRedirect('/login/')

    return check_login_status


# æéè£é¥°å?
def root_request(function):
    @login_required
    def check_request(request):
        user_id = request.session.get('user_id')
        customer = request.GET.get('customer')
        goods_id = request.GET.get('goods_id')
        print("æéï¼?, user_id, customer, goods_id, "______________________________________")
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
            print(sell_check)
            if sell_check:
                return function(request)
            else:
                return HttpResponseRedirect('/haima/')
        else:
            return HttpResponseRedirect('/haima/')

    return check_request


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
        # recommend = goods_recommend.goods_recommend(user_id)[0:5]
        # goods_recommend_list = []
        # for goods_id in recommend:
        #     cur.execute("select goods_title,goods_id,goods_imgurl,goods_price from t_goods where goods_id=%s",
        #                 [goods_id, ])
        #     goods_recommend_list.append(cur.fetchone())
        # print(goods_recommend_list)
    else:
        login_status = "æªç»å½?
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
        ['1', '0'])
    phone_list = cur.fetchall()
    # æ¶è--------------------------
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


# ç»å½
def login(request):
    url = request.META.get('HTTP_REFERER', '/')
    print(url, "è¿åå°å")
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


# å¾çéªè¯ç ?


# def ajax_captcha(request):
#     global login_code
#     if request.is_ajax():
#         result = CaptchaStore.objects.filter(response=request.GET.get('response'), hashkey=request.GET.get('hashkey'))
#         if result:
#             login_code = {'status': 1}
#         else:
#             login_code = {'status': 0}
#         return HttpResponse(json.dumps(login_code))


# ç»å½éªè¯
def login_ajax(request):
    # éªè¯ç å¤æ?
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
    # è·åè¡¨åä¿¡æ¯
    username = request.POST.get("username")
    password = request.POST.get("password")
    cur.execute("select * from t_user where user_name=%s", [username, ])  # å¨è¡¨æç´¢ï¼å¾å»ºç«ç´¢å¼
    user_login = cur.fetchone()
    # print(user_login)
    if user_login is None:  # å¤æ­ç¨æ·åå¯ç ?
        error = "login_error"
        return HttpResponse(json.dumps({"msg": error}))
    else:
        if login_code['status'] == 1:  # å¤æ­éªè¯ç ?
            print(login_code['status'])
            if password == user_login['user_password']:
                if user_login["user_state"] == 0:
                    user_id = user_login['user_id']  # å¤æ­ç¨æ·åå¯ç ?
                    request.session['username'] = username
                    request.session['user_id'] = user_id
                    # href = request.session.get('href') #åºå¼è·³è½¬æè·¯
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
                    error = "abnormal"
                    return HttpResponse(json.dumps({"msg": error}))
            else:

                error = "login_error"  # ç¨æ·åæå¯ç éè¯¯
                return HttpResponse(json.dumps({"msg": error}))
        else:
            error = "code_error"  # éªè¯ç éè¯?
            return HttpResponse(json.dumps({"msg": error}))


# æ³¨å
def register(request):
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    code = CaptchaStore.generate_key()
    return render(request, 'register.html', locals())


# æ³¨åæ¡ä»¶å¤æ­
def register_ajax(request):
    global user_error
    if request.method == "GET":
        # è·åç¨æ·åï¼
        username = request.GET.get("username")
        cur.execute("select * from t_user where user_name=%s", [username, ])  # å¨è¡¨æç´¢ï¼å¾å»ºç«ç´¢å¼
        user_list = cur.fetchall()
        if len(username) in range(6, 17):
            check_name = re.compile(r'^\w+$')
            check_ = check_name.match(username)
            if check_ is None:
                user_error = "ç¨æ·åä¸º6-16ä½çæ°å­æè±æ?
                return HttpResponse(json.dumps({"error": user_error}))
            else:
                if user_list:  # å¤æ­ç¨æ·åæ¯å¦å­å?
                    user_error = "ç¨æ·åå·²å­å¨"
                    return HttpResponse(json.dumps({"error": user_error}))
                else:
                    user_error = ""  # ç¨æ·åå¯ç?
                    return HttpResponse(json.dumps({"error": user_error}))
        else:
            user_error = "ç¨æ·åä¸º6-16ä½çæ°å­æè±æ?
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
        # è·åç¨æ·è¡¨åä¿¡æ¯
        username = request.POST.get("username")
        password = request.POST.get("password")
        # email = request.POST.get("email")
        phone = request.POST.get("phone")
        code = request.POST.get("code")
        check_all = request.POST.get("check_all")
        print(phone)
        # print(username, password, phone, check_code, check_all, login_code)
        if login_code['status'] == 1:  # å¾çéªè¯ç ?
            check_code = sms.get(phone)  # è·åææºéªè¯ç ?
            check_code = check_code.decode("utf-8")
            if check_code == code:  # ææºéªè¯å¤æ­ï¼?
                if user_error == "" and check_all == 'true':
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
                    cur.execute(
                        "insert into t_user(user_name,user_password,user_phone,user_startdate) values(%s,%s,%s,%s)",
                        [username, password, phone, now_time])
                    # print(username, email, phone, password)
                    con.commit()
                    r.delete(phone)
                    code_error = 'register_ok'  # æ³¨åæåï¼è·³è½?

                    request.session['username'] = username
                    return HttpResponse(json.dumps({"msg": code_error}))
                elif user_error == "ç¨æ·åå·²å­å¨":
                    code_error = 'user_exists'  # ç¨æ·åå­å?
                    return HttpResponse(json.dumps({"msg": code_error}))
                else:
                    code_error = 'check_all'  # æ£æ¥æ¯å¦æéè¯¯
                    return HttpResponse(json.dumps({"msg": code_error}))
            else:
                code_error = 'phone_code_error'  # ææºéªè¯ç éè¯¯éªè¯ç 
                return HttpResponse(json.dumps({"msg": code_error}))

        else:
            code_error = 'img_code_error'  # å¾çéªè¯ç éè¯?
            return HttpResponse(json.dumps({"msg": code_error}))
            # code_error = 'phone_code_error'  # ææºéªè¯ç éè¯¯éªè¯ç 
            # return HttpResponse(json.dumps({"msg": code_error}))


# éªè¯ç ï¼
def code(request):
    phone = request.GET.get("phone")
    code_ = random.randint(100000, 999999)
    # print(code, phone)
    r.set(phone, code_, 60)
    return HttpResponse(code)


# æ³¨åæåé¡µé¢è·³è½¬
def register_ok(request):
    return render(request, "register_ok.html")


# æç´¢è·³è½¬å°åååè¡?------------------------------------------
def goods_list(request):
    value_list = []
    start_list = []
    goods_lst = []
    if request.method == 'GET':
        question = request.GET.get('q')
        if question == 'å¨æ°é²ç½®':
            prompt = 'ä»¥ä¸ååä¸ºæ¬å¹³å°ææ°ä¸æ¶ååï¼åªæ¾ç¤ºææ°ç60æ¡åï¼?
            cur.execute("select * from t_goods order by goods_id desc limit 60")
            goods_lst = cur.fetchall()
        elif question == 'ååäº¤æ':
            if request.session.get('user_id'):
                user_id = request.session.get('user_id')
                cur.execute("select user_address from t_user where user_id = %s", [user_id])
                user_address_dict = cur.fetchone()
                user_address = user_address_dict['user_address']
                if user_address:
                    cur.execute("select * from t_goods where goods_address = %s", [user_address, ])
                    goods_lst = cur.fetchall()
                    prompt = 'ä»¥ä¸ååä¸? + user_address + 'å°åºååçååï¼å¦éè¦æ¥è¯¢å¶ä»å°åºè¯·å¨ç¨æ·ä¸­å¿ä¸­ä¿®æ¹å±ä½å?
                else:
                    prompt = 'äº²è¿æ²¡æè®¾ç½®å±ä½å°çä¸å°åååååï¼è¯·å¨ç¨æ·ä¸­å¿è®¾ç½®'
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
                        value_list.append(value)
            value_list = sorted(set(value_list), key=value_list.index)
            for goods_id in value_list:
                sql = "select * from t_goods where goods_id = %d" % goods_id
                cur.execute(sql)
                goods = cur.fetchone()
                goods_lst.append(goods)
            prompt = 'å·²éæ¡ä»¶ï¼ ææä¸' + '"' + question + '"' + 'ç¸å³çå®è´?
            if count == 0:
                return render(request, 'register_ok.html')
        # ä»·æ ¼ç­é?
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

        # åé¡µ
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


# ç¨æ·ä¸­å¿ââââââââââââââââââââââ?
@login_required
def user_center(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    if username:
        # ç¨æ·ä¿¡æ¯------------------
        cur.execute("select * from t_user where user_name=%s", [username, ])
        user_info = cur.fetchall()
        # æµè§è®°å½--------------------------------
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
        # è¿ééè¦è¿åä»çè´­ä¹°ååºå®æ°éï¼ä»order_success è®¢åæåè¡¨å»æ?
        cur.execute("select * from t_order_success where buy_user_id=%s", [user_id])
        dict1 = cur.fetchall()
        buy_count = len(dict1)
        cur.execute("select * from t_order_success where release_user_id=%s", [user_id])
        dict2 = cur.fetchall()
        sell_count = len(dict2)
        buy_conut = 0
        if dict1:
            buy_conut = len(dict1)
        print(user_info, browse_list, 77777777777777777777)

        return render(request, 'user_center.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# ç¨æ·ä¿¡èª-----------------------------------
@login_required
def user_credit(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    user_credit_id = request.GET.get('user_credit_id')
    # å¤æ­æ¯å¦ç»é-------------------------------
    if user_id:
        # å¤æ­æ¯å¦ä¸ºæ¬äººè¿å?
        print(user_id, user_credit_id)
        if str(user_credit_id) == str(user_id):
            return redirect("/user_center/")
        else:
            # -ç¨æ·ä¿¡æ¯
            # åå¸åå--------------------------------------------------------------
            cur.execute("select * from t_user where user_id=%s ", [user_credit_id, ])
            user_info = cur.fetchall()
            # è®¡ç®å¤©æ°------------------
            day_ = str(user_info[0]["user_startdate"])
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            d1 = datetime.datetime.strptime(day_, "%Y-%m-%d")
            d2 = datetime.datetime.strptime(now_time, "%Y-%m-%d")
            d3 = str(d2 - d1)
            if d3.split(" ")[0] == "0:00:00":
                day_count = 0
            else:
                day_count = d3.split(" ")[0]
            # -ç´¯è®¡ååº-----------------
            # -æ¶å°çè¯ä»?------------------
            # -æ­£å¨åå¸çåå?---------------
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
                    i["count"] = str(count) + " ä»¶åå?
                    break
                goods[j] = lst

            print(goods)
            # cur.execute(
            #     'select * from t_order_success right join t_evaluation on order_id=evaluation_order_id where buy_user_id=%s ',
            #     [user_id, ])
            # buy_list = cur.fetchall()
            # cur.execute(
            #     'select * from t_order_success inner join t_evaluation on order_id= evaluation_order_id inner join t_goods on order_goods_id=goods_id '
            #     'where to_rid=%s order by second_message_id desc',
            #     [user_id, ])
            # # åå®¶æ¶å°çè¯ä»?--------------------------
            # cur.execute(
            #     'select * from t_order_success right join t_evaluation on order_id=evaluation_order_id where sell_user_id=%s ',
            #     [user_id, ])
            # sell_list = cur.fetchall()
            # è¯ä»·------------------------------------------------
            # ä¹°å®¶æ¶å°çè¯ä»?----------
            cur.execute(
                "select order_id from t_order_success where buy_user_id=%s and sell_eva_state=%s or release_user_id=%s and buy_eva_state=%s",
                [user_credit_id, 1, user_credit_id, 1])
            order_id = cur.fetchall()
            eva_list = []
            print(user_id)
            count_order = len(order_id)
            for id in order_id:
                one = {}
                key = str(user_credit_id) + str(id["order_id"])
                a = get_eva.hgetall(key)
                print(key, a)
                if a:
                    for i in a:
                        c = a[i].decode("utf-8")
                        i = i.decode("utf-8")
                        one[i] = c
                    eva_list.append(one)
                else:
                    eva_list.append("none")
            print("è¯ä»·åå®¹", eva_list)
            count_eva = len(eva_list)
            return render(request, "user_credit.html", locals())
    else:
        return redirect('/login/')


# _____________________________________________________________-

# ******************************************************ååçé¢è®¾ç½®,è¿åååè¯¦æ***************************************
def goods_detail(request):
    username = request.session.get('username')  # è·åä¹°å®¶ç¨æ·å?
    user_id = request.session.get('user_id')  # è·åä¹°å®¶ID
    goods_id = request.GET.get('goods')

    # ååæ¶è------------------------------------------
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s ',
        [user_id, ])
    collection_list = cur.fetchall()
    # --------------------------------------------------
    print(goods_id)  # è·åååID
    cur.execute("select * from t_goods where goods_id=%s", [goods_id, ])  # è·åååè¡¨åå®?
    goods_list = cur.fetchall()  # ååè¡¨åå®?
    print(username, user_id, goods_id, goods_list)
    seller_id = goods_list[0]['user_id']  # è·ååå®¶ID
    goods_state = goods_list[0]['goods_state']  # ååç¶æ?
    # è·åååå¾ç
    img_list = []
    for item in img.lrange(goods_id, 0, 4):
        item = item.decode("utf-8")
        img_list.append(item)
    print("ååå¾çå°å", img_list)

    # å¤æ­æ¯å¦ä¸ºåå¸äººè¿å»é¡µé¢---------------------
    if user_id == seller_id:
        cur.execute("SELECT count(*) FROM t_user_collection WHERE collection_goods_id = %s;", [goods_id, ])
        collection_count = str(cur.fetchone()['count(*)']) + "äººæ¶è?
        seller_in = "seller_in"
    else:
        seller_in = "no_seller"
        collection_count = ""

    # =-----åå®¶ä¿¡æ¯ââââââââââââââââ?
    cur.execute("select * from t_user where user_id=%s", [seller_id, ])  # è·ååå®¶ä¿¡æ¯
    seller_info = cur.fetchall()
    # cur.execute("select count(*) from test where id=1")æäº¤è®°å½
    # ------------------------------------
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # è®°å½å½åæ¶é´
    # print(username, user_id, goods_id, seller_id, now_time)
    goods_desc = goods_list[0]['goods_desc']  # ååè¯¦ç»ä»ç»
    cur.execute('select * from t_user right join t_message on user_id = message_user_id')
    message_list = cur.fetchall()  # çè¨
    # ++++++++++++++++++++++++ååçè¨å¤ç++++++++++++++++++++++++++++++
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
    # æé®åè¡¨
    button_list = []
    for i in p_comment_dict:
        button_list.append(int(i))
    # print(p_comment_dict)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    if username:  # ç»å½åæè®°å½ï¼æµè§è®°å½?
        key = goods_id
        goods_browse.lpush(key, user_id)
        key = goods_id
        cur.execute("select user_imgurl from t_user where user_id=%s", [user_id])
        user_imgurl = cur.fetchone()["user_imgurl"]
        print("å¾ç", user_imgurl)
        login_status = username
        cur.execute("select * from t_user_browse where browse_user_id=%s and browse_goods_id=%s", [user_id, goods_id])
        browse = cur.fetchone()
        # print(browse, "æ£æ?)
        if browse is None:
            count = goods_list[0]['goods_browse_count']
            count += 1
            # æ´æ°ååæµè§æ¬¡æ°
            cur.execute("update t_goods set goods_browse_count=%s where goods_id=%s", [count, goods_id])
            print(count, goods_id, "ååæµè§è®°å½")
        # ç¨æ·æµè§è®°å½
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
        login_status = 'æªç»å½?
        user_imgurl = '../static/Images/default_hp.jpg'
    href = 1
    return render(request, "detail.html", locals())


# æµè¯ç?--------------------------------
def text_message(request):
    cur.execute("select * from t_second_message right join t_user on child_user_id=user_id where  second_goods_id=%s",
                ['2', ])
    b = cur.fetchall()
    cur.execute('select * from t_message right join t_user on message_user_id=user_id where message_goods_id=%s ',
                ['2', ])
    a = cur.fetchall()
    print(a)
    print(b)
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
        # cur.execute()   #å å¥æ°æ®åº?
        # è¯è®ºæ¼æ¥
        tt = """            
                    <div style="margin-left: 100px">
                        <img src="{0}" alt="" height="50" width="50">
                        {1}
                        <p>{2}<input type="text" id="message"><input type="button" value="åå¤"
                                                                                         id="btn_message"></p>
                        <p><input type="text" id="c_message" value="" hidden></p>
                  
                </div>
            """
        tt = tt.format(child_user['user_imgurl'], child_user['user_name'], message)

        return HttpResponse(json.dumps({"msg": tt}))
    else:
        href = request.session.get('username')
        r_error = 'need_login'
        href = '/login/?href=/test/%23abc'  # getæ¹æ³#å?
        return HttpResponse(json.dumps({"msg": r_error, "href": href}))


# åå¤å¤çï¼çè¨æ?
def review_ajax(request):
    # å¤æ­ç»éç¶æ?---------------
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ------æ¥åå¼âââââââââââ?
    child_review = request.POST.get('child_review')
    rp_user_id = request.POST.get('reply_id')
    message_id = request.POST.get('message_id')
    # parent_id = request.POST.get("parent_id")
    # goods_id = request.POST.get("goods_id")
    print(" # ------æ¥åå¼âââââââââââ?)
    print(child_review, rp_user_id, message_id, username, user_id)
    cur.execute("select * from t_message where message_id=%s", [message_id, ])
    message_id_list = cur.fetchone()
    print(message_id_list)
    message_id = message_id_list["message_id"]
    parent_id = message_id_list["message_user_id"]
    goods_id = message_id_list["message_goods_id"]
    if user_id:
        login_state = username
        # ------è·åç¨æ·ä¿¡æ¯âââââââââââ?
        cur.execute("select * from t_user where user_id=%s", [user_id, ])
        child_user = cur.fetchone()
        # æåè¦åå¤äººçåå­?
        # child_name_ = child_review
        rule1 = r'åå¤(.*?):'
        child_name = re.findall(rule1, child_review)
        print(child_name, "è¦åå¤äºº")
        print(rp_user_id, child_review, "åå¤åå®¹ï¼ID")
        # å¤æ­@åå­æ¯å¦åæ³ï¼?
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
                print("å¤æ­ç¨æ·å?, child_name[0], check_child_name_2['user_name'])
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

        # å¨å­æ°æ®
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
                                                       type="button" value="åå¤"
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
        login_state = "æªç»å½?
        r_error = 'need_login'
        href = '/login/?href=/goods_detail/?goods=' + str(goods_id)  # getæ¹æ³#å?
        return HttpResponse(json.dumps({"msg": r_error, "href": href}))


def lea_message(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if username:
        Published = request.POST.get("Published")
        goods_id = request.POST.get("goods_id")
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("ååçè¨", user_id, Published, goods_id, now_time)
        cur.execute(
            "insert into t_message(message_user_id,message_desc,message_goods_id,message_date) values(%s,%s,%s,%s)",
            [user_id, Published, goods_id, now_time])
        con.commit()
        url = "success"
        return HttpResponse(json.dumps({"href": url}))

    else:
        p_error = 'need_login'
        url = '/login'
        return HttpResponse(json.dumps({"msg": p_error, "href": url}))


# ååæ¶èé¡µé¢++++++++++++++++++++++++++++++++++++++++
def collection(request):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    goods_id = request.POST.get("goods_id")
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("select * from t_user_collection where collection_user_id=%s and collection_goods_id=%s",
                [user_id, str(goods_id)])
    collection_check_ = cur.fetchone()
    print("ååæ¶è", collection_check_)
    if username:
        if collection_check_:
            msg = "æ¨å·²æ¶èè¿æ¹åå"
        else:
            msg = "æ¶èæå"
            cur.execute(
                "insert into t_user_collection(collection_date,collection_goods_id,collection_user_id) values(%s,%s,%s)",
                [now_time, goods_id, user_id])
            con.commit()
        return HttpResponse(json.dumps({"msg": msg}))
    else:
        msg = "need_login"
        href = '/login'
        return HttpResponse(json.dumps({"msg": msg, "href": href}))


# ååä¸æ¶ï¼ä¸æ?
def lower_goods(request):
    goods_id = request.POST.get("goods_id")
    print(goods_id, 888888888888888888888)
    state = request.POST.get("state")
    if state == "lower":
        cur.execute("update t_goods set goods_state=%s where goods_id=%s", ['2', goods_id])
        msg = "ä¸æ¶æå"
        # msg = "ä¸æ¶å¤±è´¥"
        con.commit()
        href = '/goods_detail/?goods=' + str(goods_id)
    else:
        cur.execute("update t_goods set goods_state=%s where goods_id=%s", ['0', goods_id])
        msg = "ä¸æ¶æå"
        con.commit()
        href = '/goods_detail/?goods=' + str(goods_id)
        print(href)

    return HttpResponse(json.dumps({"msg": msg, "href": href}))


def goods_detail_ajax(request):
    pass


# åå¸åå
def publish(request):
    if request.method == 'POST':
        price = int(request.POST.get('price_hid').replace('Â¥', ''))
    return render(request, 'publish.html', locals())


def pub_success(request):
    user_id = request.session.get('user_id')
    title = request.POST.get('title')
    category = request.POST.get('type')
    price = float(request.POST.get('price'))
    postage = request.POST.get('postage')
    desc = request.POST.get('desc')
    appearance = request.POST.get('apperance')
    filelist = json.loads(request.POST.get('filelist'))
    address = 'æ±èèå· å´æ±å?
    appearance = '4'
    if desc:
        pass
    else:
        desc = 'è¯¥åå®¶æ¯è¾æï¼è¿æ²¡æååæè¿°'
    for i in filelist:
        print(i)
    sql = "INSERT INTO t_goods(`user_id`,`release_date`,`goods_title`,`goods_desc`,`goods_price`,`goods_category_id`,`goods_imgurl`,`goods_address`,`goods_appearance`) \
                                                                   VALUES ('%s','%s','%s','%s','%f','%s','%s','%s','%s')" % \
          (
              1, loc_time, title, desc, price, category, "http://pgwecu7z4.bkt.clouddn.com/" + filelist[0], address,
              appearance)
    cur.execute(sql)
    last_id = cur.lastrowid
    for file in filelist:
        img.rpush(last_id, "http://pgwecu7z4.bkt.clouddn.com/" + file)
    con.commit()
    print(title, category, price, postage, filelist)
    return HttpResponse("publish success é¡µé¢è¿æ²¡å?)


# ä¼°ä»·
def assess(request):
    user_name = request.session.get('username')
    return render(request, 'assess.html', locals())


# ä¼°è®¡ajax
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
    price = 'Â¥' + str(int(price))
    print(price)
    time.sleep(1)
    return HttpResponse(json.dumps({"price": price}))

# ********************************************************************æ®éååè´­ä¹?**************************************
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
            # è´­ä¹°å®æï¼æ´æ°æ°æ®åºåçæè®¢åæ£æ¬¾ç­
            try:
                # åæ£é¤è´­ä¹°èçé?
                user_money = float(user_money) - float(price)
                cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, user_id])
                print("æ£é±æå")
                # çæååè®¢å
                cur.execute("select user_id from t_goods where goods_id=%s", [goods_id])
                release_user_id = cur.fetchone()["user_id"]
                date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                cur.execute(
                    "insert into t_order(release_user_id,buy_user_id,order_date,order_goods_id) values (%s,%s,%s,%s)",
                    [str(release_user_id), str(user_id), date, str(goods_id)])
                print("çæè®¢åæå")
                cur.execute("update t_goods set goods_state=%s where goods_id=%s", ["1", goods_id])
                print("æ´æ°ååç¶ææå?)
                con.commit()
                error = "pay_ok"
                return HttpResponse(json.dumps({"msg": error}))

            except Exception as e:
                print(e)
    else:
        error = "no_pay_password"
        return HttpResponse(json.dumps({"msg": error}))


# ç¨æ·è¾å¥æ¯ä»å¯ç æ£æ¬¾å®æ

def buy_goods_ok(request):
    return render(request, "buy_goods_ok.html")


# æåºå®ç
@login_required
def my_sale(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    # åå¸ä¸­çåå------------------------------
    cur.execute(
        'select * from t_goods  where user_id=%s and goods_state=%s order by goods_id desc',
        [user_id, 0])
    p_sale_list = cur.fetchall()
    print(5555555555555555555, p_sale_list)
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
    # äº¤æä¸­çåå---------------------------------
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


# my_sale æ·ä¸­å¿ååä¸æ¶ââajax: å¾ä¿®æ?
@login_required
def user_lower_goods(request):
    goods_id = request.POST.get("goods_id")
    user_id = request.session.get('user_id')
    try:
        # ä¸æ¶åå-------------------
        cur.execute("update t_goods set goods_state=%s where goods_id=%s", ['2', goods_id])
        con.commit()
        # ---é¡µé¢æ¼æ¥---------------------------
        cur.execute("select * from t_goods  where user_id=%s and goods_state=%s order by goods_id desc",
                    [user_id, 0])
        goods_list = cur.fetchall()
        print("444444444444444444444", goods_list)

        a = 0
        if goods_list:
            # for item in goods_list:
            #     print(item["goods_id"], type(item["goods_id"]), goods_id, type(goods_id))
            #     if item["goods_id"] == int(goods_id):
            #         a = goods_list.index(item) + 3
            #         print(777777777777777777777777777777777777777, a)
            #     b = a
            try:
                goods_list_ = goods_list[3]
                print(4444444444444444444, goods_id, goods_list_)
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
                                                    style="color: red">{9}å?/em>
                                            </li>
                                            <li class="col04">{10}äººæµè§?/li>
                                        </ul>
                                    </td>
                                    <td width="15%"><input type="button" class="lower1_btn lower_{11}"
                                               onclick="lower({12})" value="ä¸æ¶"></td>
                                    <td width="15%"><a href="" class="oper_btn">ä¿®æ¹</a></td>
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


# æçåºå®ï¼ä¸ä¸æ¶é¡µé¢
@login_required
def my_sale_lower(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    if request.is_ajax():
        goods_id = request.POST.get("goods_id")
        try:
            cur.execute("update t_goods set goods_state=%s where goods_id=%s", ['0', goods_id])
            msg = "ä¸æ¶æå"
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


# åºå®å®æé¡µé¢
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


# ******************************************************************æè´­ä¹°ç*******************************************
def my_buy(request):
    username = request.session.get('username')
    user_id = request.session.get("user_id")
    cur.execute("select * from t_order right join t_goods on order_goods_id=goods_id where buy_user_id=%s", [user_id])
    order_list = cur.fetchall()
    print(order_list)
    return render(request, 'my_buy.html', locals())


def my_buy_complete(request):
    username = request.session.get('username')
    user_id = request.session.get("user_id")
    cur.execute("select * from t_order_success right join t_goods on order_goods_id=goods_id where buy_user_id=%s",
                [user_id, ])
    order_success_list = cur.fetchall()
    return render(request, "my_buy_complete.html", locals())




# æçæ¶è
def my_collection(request):
    username = request.session.get('username')  # è·åä¹°å®¶ç¨æ·å?
    user_id = request.session.get('user_id')  # è·åä¹°å®¶ID
    goods_id = request.GET.get('goods')
    # ååæ¶è------------------------------------------
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s limit 5 ',
        [user_id, ])
    collection_list = cur.fetchall()
    print(collection_list, 45454544885454545554545)
    # -----------------------------------
    return render(request, 'my_collection.html', locals())


# è¯ä»·
@root_request
def evaluate(request):
    username = request.session.get('username')  # è·åä¹°å®¶ç¨æ·å?
    user_id = request.session.get('user_id')  # è·åä¹°å®¶ID
    goods_id = request.GET.get('goods_id')
    customer = request.GET.get("customer")
    print("evaluate", "------", username, user_id, goods_id)
    # ååæ¶è------------------------------------------
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s ',
        [user_id, ])
    collection_list = cur.fetchall()
    # --------------------------------------------------
    print(goods_id)  # è·åååID
    cur.execute("select * from t_goods where goods_id=%s", [goods_id, ])  # è·åååè¡¨åå®?
    goods_list = cur.fetchall()  # ååè¡¨åå®?
    print(username, user_id, goods_id, goods_list)
    seller_id = goods_list[0]['user_id']  # è·ååå®¶ID
    goods_state = goods_list[0]['goods_state']  # ååç¶æ?
    goods_desc = goods_list[0]["goods_desc"]
    # è·åååå¾ç
    img_list = []
    for item in img.lrange(goods_id, 0, 4):
        item = item.decode("utf-8")
        img_list.append(item)
    print("ååå¾çå°å", img_list)
    # =-----åå®¶ä¿¡æ¯ââââââââââââââââ?
    cur.execute("select * from t_user where user_id=%s", [seller_id, ])  # è·ååå®¶ä¿¡æ¯
    seller_info = cur.fetchall()
    # å¤æ­ä¹°åå®?
    if customer == "buy":
        # --æ¬ååæ¯å¦å·²ç»è¯ä»?------------------
        cur.execute("select * from t_order_success where order_goods_id=%s", [goods_id, ])  # è·åååè¡¨åå®?
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
        cur.execute("select * from t_order_success where order_goods_id=%s", [goods_id, ])  # è·åååè¡¨åå®?
        sell_list = cur.fetchone()
        print(sell_list)
        eva_state = sell_list["sell_eva_state"]
        order_id = sell_list["order_id"]
        print("è®¢åï¼?, order_id, "ç¶æ?, type(eva_state))
        if eva_state != 0:
            cur.execute("select * from t_evaluation where evaluation_order_id=%s", [order_id, ])
            sell_desc_list = cur.fetchall()
            print(55555555, customer, eva_state, order_id, sell_desc_list)

    return render(request, 'evaluate.html', locals())


def evaluate_ajax(request):
    user_id = request.session.get('user_id')
    evaluate_text = request.POST.get('evaluate_text')
    eva_state = request.POST.get('dddddddd')
    customer = request.POST.get('customer')
    order_id = request.POST.get('order_id')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(evaluate_text, eva_state, customer, type(order_id))
    if customer == "buy":
        cur.execute(
            "update t_evaluation set buyer_evaluation_date = %s,buyer_desc=%s,buy_state=%s where evaluation_order_id = %s",
            [now_time, evaluate_text, eva_state, order_id])
        cur.execute("update t_order_success set buy_eva_state=%s where order_id=%s", [1, order_id])
        # __________________redisä¿å­è¢«åå¤äººè®°å½(å«äººæ¥çè®°å½)-----------------------------------------------------------------------
        cur.execute("select * from t_order_success where order_id=%s", [int(order_id), ])
        order_list = cur.fetchone()
        key = str(order_list["release_user_id"]) + str(order_id)
        print("è´­ä¹°äººï¼", key)
        # è¯ä»·äººçä¿¡æ¯ï¼?------------
        cur.execute("select * from t_user where user_id=%s", [user_id, ])
        get_user_list = cur.fetchone()
        # ååä¿¡æ¯ï¼?---------------------------------------------------
        cur.execute("select * from t_goods where goods_id=%s", [order_list["order_goods_id"], ])
        goods_lst = cur.fetchone()
        get_eva.hset(key, "username", get_user_list["user_name"])
        get_eva.hset(key, "user_imgurl", get_user_list["user_imgurl"])
        get_eva.hset(key, "user_id", get_user_list["user_id"])
        get_eva.hset(key, "desc", evaluate_text)
        get_eva.hset(key, "date", now_time)
        get_eva.hset(key, "goods_id", goods_lst["goods_id"])
        get_eva.hset(key, "goods_name", goods_lst["goods_title"])
        get_eva.hset(key, "goods_price", goods_lst["goods_price"])
        get_eva.hset(key, "eva_state", eva_state)
        get_eva.hset(key, "customer", "ä¹°å®¶")
        # __________________redisä¿å­åå¤äººè®°å½?----------------------------------------------------------------------
        # è¯ä»·ç¨æ·çä¿¡æ¯ï¼-------------
        key_ = str(order_list["buy_user_id"]) + str(order_id)
        cur.execute("select * from t_user where user_id=%s", [order_list["release_user_id"], ])
        set_user_list = cur.fetchone()
        set_eva.hset(key_, "username", set_user_list["user_name"])
        set_eva.hset(key_, "user_imgurl", set_user_list["user_imgurl"])
        set_eva.hset(key_, "user_id", set_user_list["user_id"])
        set_eva.hset(key_, "desc", evaluate_text)
        set_eva.hset(key_, "date", now_time)
        set_eva.hset(key_, "goods_id", goods_lst["goods_id"])
        set_eva.hset(key_, "goods_name", goods_lst["goods_title"])
        set_eva.hset(key_, "goods_price", goods_lst["goods_price"])
        set_eva.hset(key_, "eva_state", eva_state)
        set_eva.hset(key_, "customer", "åå®¶")
    else:
        cur.execute(
            "update t_evaluation set seller_evaluation_date = %s,seller_desc=%s,sell_state=%s where evaluation_order_id = %s",
            [now_time, evaluate_text, eva_state, order_id])
        cur.execute("update t_order_success set sell_eva_state=%s where order_id=%s", [1, order_id])
        # __________________redisä¿å­è¢«åå¤äººè®°å½(å«äººæ¥çè®°å½)-----------------------------------------------------------------------
        cur.execute("select * from t_order_success where order_id=%s", [int(order_id), ])
        order_list = cur.fetchone()
        key = str(order_list["buy_user_id"]) + str(order_id)
        # è¢«è¯ä»·ç¨æ·çä¿¡æ¯ï¼?------------
        cur.execute("select * from t_user where user_id=%s", [user_id, ])
        get_user_list = cur.fetchone()
        # ååä¿¡æ¯ï¼?---------------------------------------------------
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
        get_eva.hset(key, "customer", "åå®¶")
        # __________________redisä¿å­åå¤äººè®°å½?----------------------------------------------------------------------
        # è¯ä»·ç¨æ·çä¿¡æ¯ï¼-------------
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
        set_eva.hset(key_, "customer", "ä¹°å®¶")
    con.commit()
    msg = "success"
    return HttpResponse(json.dumps({"msg": msg}))


# ææ¶å°çè¯ä»·
def my_evaluate_get(request):
    return render(request, 'my_evaluate_get.html')


# ç»ä»äººçè¯ä»·
def my_evaluate_give(request):
    return render(request, 'my_evaluate_give.html')


# æ¶å°çåå¤?
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


# æçåå¤
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


def leave_message_three(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
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


# ä¿®æ¹ä¿¡æ¯
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


# ä¸ä¼ å¾çæéè¦çtoken
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

# ***********************************************æ®éååç¡®è®¤æ¶è´?************************************************
def confirm_goods(request):
    goods_id = request.POST.get("goods_id")
    cur.execute("select * from t_order where order_goods_id=%s", [goods_id])
    goods_message = cur.fetchone()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    print(goods_message)
    # æä¿¡æ¯å å°è®¢åæåè¡¨ï¼ç¶åå é¤åæ¥è®¢åè¡¨éçæ°æ®
    try:
        cur.execute("insert into t_order_success (release_user_id,buy_user_id,order_date,order_goods_id) values (%s,%s,%s,%s\
                      )",
                    [str(goods_message["release_user_id"]), str(goods_message["buy_user_id"]), date, str(goods_id)])
        cur.execute("delete from t_order where order_goods_id=%s", [str(goods_id)])
        # ç¨æ·ç¡®è®¤æ¶è´§ä»¥åéè¦æåå®¶çé±å¢å 
        cur.execute("select goods_price from t_goods where goods_id=%s", [goods_id])
        goods_price = cur.fetchone()["goods_price"]
        cur.execute("select user_money from t_user where user_id=%s", [goods_message["release_user_id"]])
        user_money = cur.fetchone()["user_money"]
        user_money = user_money + goods_price
        cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, goods_message["release_user_id"]])
        print("ok")
    except Exception as e:
        con.rollback()
        print(e)
    con.commit()
    return HttpResponse(json.dumps({"msg": "123"}))

# æ¯ä»å®æ¯ä»?

# *********************************************æåååçæ¶è´?******************************************************
def confirm_auction_goods(request):
    order_id = request.POST.get("order_id")
    # ç¨æ·ç¡®è®¤æ¶è´§ä»¥åæ¹åç¶æ?
    try:
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        cur.execute("update t_auction_order set auction_order_state=%s,order_success_date=%s where auction_order_id=%s",
                    ["2", now_date, order_id])
        cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s", [order_id])
        auction_goods_id = cur.fetchone()["auction_order_goods_id"]
        # ç¨æ·ç¡®è®¤æ¶è´§ä»¥åéè¦æé±æå°åå®¶è´¦æ?
        cur.execute("select auction_goods_margin from t_auction_attribute where auction_goods_id=%s",
                    [auction_goods_id])
        goods_margin = cur.fetchone()["auction_goods_margin"]
        cur.execute("select auction_goods_fianl_prcie from t_auction_goods where auction_order_id=%s", [order_id])
        goods_money = cur.fetchone()["auction_goods_fianl_prcie"]
        cur.execute("select auction_goods_user_id from t_auction_goods_record where auction_goods_id=%s",
                    [auction_goods_id])
        maijia_id = cur.fetchone()["auction_goods_user_id"]
        cur.execute("select user_money from t_user where user_id=%s", [maijia_id])
        user_money = cur.fetchone()["user_money"]
        user_money = user_money + goods_money + goods_margin
        cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, maijia_id])
        cur.execute("update t_auction_goods_record set auction_goods_state=%s where auction_goods_id=%s",
                    ["4", auction_goods_id])
        con.commit()
    except Exception as e:
        print(e)

def get_ali_object():
    # æ²ç®±ç¯å¢å°åï¼https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2016092000555548"  # APPID ï¼æ²ç®±åºç¨ï¼

    # æ¯ä»å®æåï¼æ¯ä»å·å·åè¿éå°ååéä¸ä¸ªpostè¯·æ±ï¼è¯å«å¬ç½IP,å¦ææ?192.168.20.13å±åç½IP ,æ¯ä»å®æ¾ä¸å°ï¼def page2() æ¥æ¶ä¸å°è¿ä¸ªè¯·æ±
    # notify_url = "http://47.94.172.250:8804/page2/"
    notify_url = "http://127.0.0.1:8000/page2/"
    # æ¯ä»å®æåï¼è·³è½¬çå°åã?
    return_url = "http://127.0.0.1:8000/page2/"
    merchant_private_key_path = "keys/app_private_2048.txt"  # åºç¨ç§é¥
    alipay_public_key_path = "keys/alipay_public_2048.txt"  # æ¯ä»å®å¬é?
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # æ¯ä»å®çå¬é¥ï¼éªè¯æ¯ä»å®åä¼ æ¶æ¯ä½¿ç¨ï¼ä¸æ¯ä½ èªå·±çå¬é?
        debug=True,  # é»è®¤False,
    )
    return alipay


# åç«¯è·³è½¬çæ¯ä»é¡µé?
@login_required
def page1(request):
    # æ ¹æ®å½åç¨æ·çéç½®ï¼çæURLï¼å¹¶è·³è½¬ã?
    user_id = request.session.get("user_id")
    money = request.POST.get('price')
    title = request.POST.get('title')
    alipay = get_ali_object()
    goods_id = request.POST.get('goods_id')
    request.session['goods_id'] = goods_id
    # çææ¯ä»çurl
    query_params = alipay.direct_pay(
        subject=title,  # ååç®åæè¿?
        out_trade_no="x2" + str(time.time()),  # ç¨æ·è´­ä¹°çååè®¢åå·ï¼æ¯æ¬¡ä¸ä¸æ ·ï¼ 20180301073422891
        total_amount=money,  # äº¤æéé¢(åä½: å?ä¿çä¿©ä½å°æ°)

    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # æ¯ä»å®ç½å³å°åï¼æ²ç®±åºç¨ï¼

    print(pay_url)

    return HttpResponse(pay_url)


def page2(request):
    alipay = get_ali_object()
    if request.method == "POST":
        # æ£æµæ¯å¦æ¯ä»æå?
        # å»è¯·æ±ä½ä¸­è·åææè¿åçæ°æ®ï¼ç¶æ?è®¢åå?
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        # post_dictæ?0keyï¼?9 ï¼?
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('------------------å¼å§?-----------------')
        print('POSTéªè¯', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']

        # ä¿®æ¹è®¢åç¶æ?
        # models.Order.objects.filter(trade_no=out_trade_no).update(status=2)
        print('------------------ç»æ------------------')
        # ä¿®æ¹è®¢åç¶æï¼è·åè®¢åå?
        return HttpResponse('POSTè¿å')

    else:
        user_id = request.session.get("user_id")
        goods_id = request.session.get("goods_id")
        print(goods_id)
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================å¼å§?=================')
        print('GETéªè¯', status)
        print('==================ç»æ==================')
        print("æ¯ä»æå")
        try:
            # çæååè®¢å
            cur.execute("select user_id from t_goods where goods_id=%s", [goods_id])
            release_user_id = cur.fetchone()["user_id"]
            date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            cur.execute(
                "insert into t_order(release_user_id,buy_user_id,order_date,order_goods_id) values (%s,%s,%s,%s)",
                [str(release_user_id), str(user_id), date, str(goods_id)])
            print("çæè®¢åæå")
            cur.execute("update t_goods set goods_state=%s where goods_id=%s", ["1", goods_id])
            print("æ´æ°ååç¶ææå?)
            con.commit()

        except Exception as e:
            print(e)
        return redirect("/haima/")


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
    return render(request, 'admin.html', {'user': user})


@admin_session
def admin_goods(request, user):
    cur.execute("select * from t_goods inner join t_user on t_goods.user_id=t_user.user_id")
    goodslist = cur.fetchall()
    paginator = Paginator(goodslist, 35)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'admin_goods.html', {'user': user, 'contacts': contacts})


@admin_session
def admin_search_goods(request, user):
    start = request.POST.get('start')
    end = request.POST.get('end')
    print(start, end)
    return HttpResponse("POST")


@admin_session
def admin_update(request, user):
    goods_id = request.POST.get('goods_id')
    user_id = request.POST.get('user_id')
    action = request.POST.get('action')
    if goods_id:
        result = cur.execute("update t_goods set goods_state = %s where goods_id = %s", [action, goods_id, ])
    else:
        result = cur.execute("update t_user set user_state = %s where user_id = %s", [action, user_id, ])
    con.commit()
    if result:
        return HttpResponse("success")
    else:
        return HttpResponse('')


@admin_session
def admin_user(request, user):
    cur.execute("select * from t_user")
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
