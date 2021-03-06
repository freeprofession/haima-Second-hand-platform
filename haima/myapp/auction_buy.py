import pymysql
import time
import redis
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = con.cursor(pymysql.cursors.DictCursor)
message_push = redis.Redis(host="47.100.200.132", port=6379, db=11,password='haima1234')
from myapp import view
def login_required(function):

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
# **********************************************************返回用户的我的拍卖中心我的竞拍的界面**************************************
@login_required
def my_auction_buy_one(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    user_id = request.session.get("user_id")
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
    username = request.session.get("username")
    login_status = username
    # 先找到该用户的所有竞拍记录
    cur.execute("select auction_record_id  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    record_id_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    # 找到用户的订单
    cur.execute("select *  from t_auction_order where auction_order_buy_user_id=%s", [user_id])
    order_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])

    goods_list = []
    list1=[]
    for i in record_id_dict:
        dict1 = {}
        # 这里拿到拍卖记录表的状态
        cur.execute("select auction_goods_state from t_auction_record where auction_record_id=%s",
                    [i["auction_record_id"]])
        x = cur.fetchone()
        state = x["auction_goods_state"]
        if state == 1:  # 竞拍中的记录
            dict1 = {}
            print(i)
            cur.execute("select auction_goods_id from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])
            goods_id = cur.fetchone()["auction_goods_id"]
            cur.execute("select *  from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])
            record_message = cur.fetchone()
            cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                        [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                        [goods_id])
            attribute = cur.fetchone()
            dict1["state"] = "竞拍中"
            dict1["goods"] = goods_message
            dict1["record"] = record_message
            dict1["attribute"] = attribute
            list1.append(dict1)
    list1.reverse()
    paginator = Paginator(list1, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    cur.close()
    return render(request,'my_auction_buy_one.html',locals())
def my_auction_buy_two(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    user_id = request.session.get("user_id")
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
    username = request.session.get("username")
    login_status = username
    # 先找到该用户的所有竞拍记录
    cur.execute("select auction_record_id  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    record_id_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    # 找到用户的订单
    cur.execute("select *  from t_auction_order where auction_order_buy_user_id=%s", [user_id])
    order_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    list2=[]
    goods_list = []
    list1=[]
    for i in record_id_dict:
        dict1 = {}
        # 这里拿到拍卖记录表的状态
        cur.execute("select auction_goods_state from t_auction_record where auction_record_id=%s",
                    [i["auction_record_id"]])
        x = cur.fetchone()
        state = x["auction_goods_state"]
        if state == 0:  # 竞拍失败的记录
            dict1 = {}
            print(i)
            cur.execute("select auction_goods_id from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])

            goods_id = cur.fetchone()["auction_goods_id"]
            cur.execute("select *  from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])
            record_message = cur.fetchone()
            cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                        [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                        [goods_id])
            attribute = cur.fetchone()
            dict1["state"] = "竞拍失败"
            dict1["goods"] = goods_message
            dict1["record"] = record_message
            dict1["attribute"] = attribute
            list2.append(dict1)
    list2.reverse()
    paginator = Paginator(list2, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    cur.close()
    return render(request,'my_auction_buy_two.html',locals())
def my_auction_buy_three(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    username = request.session.get("username")
    login_status = username
    user_id = request.session.get("user_id")
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
    username = request.session.get("username")
    login_status = username
    list3=[]
    # 先找到该用户的所有竞拍记录
    cur.execute("select auction_record_id  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    record_id_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    # 找到用户的订单
    cur.execute("select *  from t_auction_order where auction_order_buy_user_id=%s", [user_id])
    order_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    goods_list = []
    if order_dict:
        for i in order_dict:
            id = i["auction_order_id"]
            cur.execute("select auction_order_state from t_auction_order where auction_order_id=%s", [id])
            x = cur.fetchone()
            order_state = x["auction_order_state"]
            # 这里待支付尾款的
            if order_state == 0:
                dict1 = {}
                cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                print(i["auction_order_id"])
                goods_id = cur.fetchone()["auction_order_goods_id"]
                cur.execute(
                    "select auction_record_id from t_auction_record where auction_goods_id=%s",
                    [goods_id])
                record_dict = cur.fetchall()
                if record_dict:
                    record_list = []
                    for i in record_dict:
                        record_list.append(i["auction_record_id"])
                    record_maxid = max(record_list)

                    cur.execute("select * from t_auction_record where auction_record_id=%s",[record_maxid])
                    record_message=cur.fetchone()
                    cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                                [goods_id])
                    goods_message = cur.fetchone()
                    cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                                [goods_id])
                    attribute = cur.fetchone()
                    cur.execute("select * from t_auction_order where auction_order_goods_id=%s", [goods_id])
                    order_messge = cur.fetchone()
                    dict1["goods"] = goods_message
                    dict1["attribute"] = attribute
                    dict1["order"] = order_messge
                    dict1["record"]=record_message
                    list3.append(dict1)
    list3.reverse()
    paginator = Paginator(list3, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    cur.close()
    return render(request,'my_auction_buy_three.html',locals())
def my_auction_buy_four(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    username = request.session.get("username")
    login_status = username
    user_id = request.session.get("user_id")
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
    username = request.session.get("username")
    login_status = username
    # 找到用户的订单
    list2=[]
    cur.execute("select *  from t_auction_order where auction_order_buy_user_id=%s", [user_id])
    order_dict = cur.fetchall()
    for i in order_dict:
        state=i["auction_order_state"]

        if state == 3:  # 竞拍失败的记录
            dict1 = {}
            print(i)
            cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                        [i["auction_order_id"]])

            goods_id = cur.fetchone()["auction_order_goods_id"]
            cur.execute("select * from t_auction_order where auction_order_id=%s",
                        [i["auction_order_id"]])
            order_message=cur.fetchone()
            cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                        [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                        [goods_id])
            attribute = cur.fetchone()
            dict1["state"] = "付款失败"
            dict1["goods"] = goods_message
            dict1["order"]=order_message
            dict1["attribute"] = attribute
            list2.append(dict1)
    list2.reverse()
    print(list2)
    paginator = Paginator(list2, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    cur.close()
    return render(request, 'my_auction_buy_four.html', locals())


def my_auction_buy_five(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    username = request.session.get("username")
    login_status = username
    user_id = request.session.get("user_id")
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
    username = request.session.get("username")
    login_status = username
    list5=[]
    # 先找到该用户的所有竞拍记录
    cur.execute("select auction_record_id  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    record_id_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    # 找到用户的订单
    cur.execute("select *  from t_auction_order where auction_order_buy_user_id=%s", [user_id])
    order_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    if order_dict:
        for i in order_dict:
            id = i["auction_order_id"]
            cur.execute("select auction_order_state from t_auction_order where auction_order_id=%s", [id])
            x = cur.fetchone()
            order_state = x["auction_order_state"]
            if order_state == 1:
                print(i)
                dict1 = {}
                cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                goods_id = cur.fetchone()["auction_order_goods_id"]
                print(goods_id)
                cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                            [goods_id])
                goods_message = cur.fetchone()

                cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                            [goods_id])
                attribute = cur.fetchone()
                cur.execute("select * from t_auction_order where auction_order_id=%s", [i["auction_order_id"]])
                order_messge = cur.fetchone()
                cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                the_goods_state = cur.fetchone()["the_goods_state"]
                if the_goods_state == 0:
                    dict1["state"] = "待发货"
                else:
                    dict1["state"] = the_goods_state
                dict1["goods"] = goods_message
                dict1["attribute"] = attribute
                dict1["order"] = order_messge

                list5.append(dict1)
    list5.reverse()
    paginator = Paginator(list5, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    cur.close()
    return render(request,'my_auction_buy_five.html',locals())
def my_auction_buy_six(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    username = request.session.get("username")
    login_status = username
    user_id = request.session.get("user_id")
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
    username = request.session.get("username")
    login_status = username

    list6=[]
    # 先找到该用户的所有竞拍记录
    cur.execute("select auction_record_id  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    record_id_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    # 找到用户的订单
    cur.execute("select *  from t_auction_order where auction_order_buy_user_id=%s", [user_id])
    order_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    if order_dict:
        for i in order_dict:
            id = i["auction_order_id"]
            cur.execute("select auction_order_state from t_auction_order where auction_order_id=%s", [id])
            x = cur.fetchone()
            order_state = x["auction_order_state"]
            if order_state == 2:
                dict1 = {}
                cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                goods_id = cur.fetchone()["auction_order_goods_id"]
                cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                            [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select * from t_auction_order where auction_order_goods_id")
                order_messge = cur.fetchone()
                cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                dict1["goods"] = goods_message
                dict1["order"] = order_messge
                list6.append(dict1)
    list6.reverse()
    print(list6)
    paginator = Paginator(list6, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    cur.close()
    return render(request,'my_auction_buy_six.html',locals())

def my_auction_four(request):
    user_id = request.session.get("user_id")
    # 先找到该用户的所有竞拍记录
    cur.execute("select auction_record_id  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    record_id_dict = cur.fetchall()
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])
    # 找到用户的订单
    cur.execute("select *  from t_auction_order where auction_order_buy_user_id=%s", [user_id])
    order_dict = cur.fetchall()
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    cur.execute("select *  from t_auction_record where auction_goods_buyuser_id=%s",
                [user_id])

    goods_list = []


    for i in record_id_dict:
        dict1 = {}
        # 这里拿到拍卖记录表的状态
        cur.execute("select auction_goods_state from t_auction_record where auction_record_id=%s",
                    [i["auction_record_id"]])
        x = cur.fetchone()
        state = x["auction_goods_state"]
        if state == 0:  # 竞拍失败的记录
            dict1 = {}
            print(i)
            cur.execute("select auction_goods_id from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])

            goods_id = cur.fetchone()["auction_goods_id"]
            cur.execute("select *  from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])
            record_message = cur.fetchone()
            cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                        [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                        [goods_id])
            attribute = cur.fetchone()
            dict1["state"] = "竞拍失败"
            dict1["goods"] = goods_message
            dict1["record"] = record_message
            dict1["attribute"] = attribute
            list2.append(dict1)
        if state == 1:  # 竞拍中的记录
            dict1 = {}
            print(i)
            cur.execute("select auction_goods_id from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])
            goods_id = cur.fetchone()["auction_goods_id"]
            cur.execute("select *  from t_auction_record where auction_record_id=%s",
                        [i["auction_record_id"]])
            record_message = cur.fetchone()
            cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                        [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                        [goods_id])
            attribute = cur.fetchone()
            dict1["state"] = "竞拍中"
            dict1["goods"] = goods_message
            dict1["record"] = record_message
            dict1["attribute"] = attribute
            list1.append(dict1)
    print("竞拍中的",list1)
    if order_dict:
        for i in order_dict:
            id = i["auction_order_id"]
            cur.execute("select auction_order_state from t_auction_order where auction_order_id=%s", [id])
            x = cur.fetchone()
            order_state = x["auction_order_state"]

            # 这里待支付尾款的
            if order_state == 0:
                dict1 = {}
                cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                goods_id = cur.fetchone()["auction_order_goods_id"]
                cur.execute(
                    "select auction_record_id from t_auction_record where auction_goods_id=%s",
                    [goods_id])
                record_dict = cur.fetchall()
                if record_dict:
                    record_list = []
                    for i in record_dict:
                        record_list.append(i["auction_record_id"])
                    record_maxid = max(record_list)
                cur.execute("select * from t_auction_record where auction_record_id=%s",[record_maxid])
                record_message=cur.fetchone()
                cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                            [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                            [goods_id])
                attribute = cur.fetchone()
                cur.execute("select * from t_auction_order where auction_order_goods_id=%s", [goods_id])
                order_messge = cur.fetchone()
                dict1["goods"] = goods_message
                dict1["attribute"] = attribute
                dict1["order"] = order_messge
                dict1["record"]=record_message
                list3.append(dict1)
            print(list3)            # 这里表示支付完成的
            if order_state == 1:
                print(i)
                dict1 = {}
                cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                goods_id = cur.fetchone()["auction_order_goods_id"]
                print(goods_id)
                cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                            [goods_id])
                goods_message = cur.fetchone()

                cur.execute("select *  from t_auction_attribute where auction_goods_id=%s",
                            [goods_id])
                attribute = cur.fetchone()
                cur.execute("select * from t_auction_order where auction_order_id=%s",[i["auction_order_id"]])
                order_messge = cur.fetchone()
                cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                the_goods_state = cur.fetchone()["the_goods_state"]
                if the_goods_state == 0:
                    dict1["state"] = "待发货"
                else:
                    dict1["state"] = the_goods_state
                dict1["goods"] = goods_message
                dict1["attribute"] = attribute
                dict1["order"] = order_messge

                list5.append(dict1)
            # 收货完成交易成功
            if order_state == 2:
                dict1 = {}
                cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                goods_id = cur.fetchone()["auction_order_goods_id"]
                cur.execute("select *  from t_auction_goods_record where auction_goods_id=%s",
                            [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select * from t_auction_order where auction_order_goods_id")
                order_messge = cur.fetchone()
                cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s",
                            [i["auction_order_id"]])
                dict1["goods"] = goods_message

                dict1["order"] = order_messge
                list6.append(dict1)
                pass
        print(list1)

        #
        # dict1 = {}
        # dict1["record"] = goods_record_list[i]
        # dict1["goods"] = goods_info_list[i]
        # list4.append(dict1)
        # print(list4)

        return render(request, 'my_auction_buy_one.html', locals())

