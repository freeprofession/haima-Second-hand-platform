import pymysql
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = con.cursor(pymysql.cursors.DictCursor)
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
# **********************************************************返回用户的我的拍卖中心的我的发布界面**************************************
# 这里主要是显示他的发布记录,和发布商品现在的状态
def my_auction_sale_one(request):
    username = request.session.get("username")
    login_status = username
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    user_id = request.session.get("user_id")
    username = request.session.get('username')
    print(username)
    # 从发布记录表里找到商品id
    cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s", [user_id])
    message = cur.fetchall()
    id_list = []
    id_list = []
    for i in message:
        id_list.append(i["release_auction_goods_id"])
    list10=[]
    for goods_id in id_list:
        dict1 = {}
        cur.execute("select auction_goods_state from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
        x = cur.fetchone()
        state = x["auction_goods_state"]
        if int(state) == 0:  # 0代表的是正常拍卖的
            # print("正常拍卖")

            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["state"] = "正在拍卖"
            # 返回当前竞拍者的姓名
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
                    cur.execute("select auction_goods_buyuser_id from t_auction_record where auction_record_id=%s",
                                [record_maxid])
                    buy_user_id = cur.fetchone()
                    cur.execute("select user_name from t_user where user_id=%s",
                                [buy_user_id["auction_goods_buyuser_id"]])
                    user_name = cur.fetchone()["user_name"]
                    if user_name:
                        dict1["user_name"] = user_name
                    else:
                        dict1["user_name"] = "无"
            list10.append(dict1)
    list10.reverse()
    paginator = Paginator(list10, 2)
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
    return render(request,'my_auction_sale_one.html',locals())
def my_auction_sale_two(request):
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    login_status = username
    # 从发布记录表里找到商品id
    cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s", [user_id])
    message = cur.fetchall()
    id_list = []
    id_list = []
    for i in message:
        id_list.append(i["release_auction_goods_id"])
    list11=[]
    for goods_id in id_list:
        dict1 = {}
        cur.execute("select auction_goods_state from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
        x = cur.fetchone()

        state = x["auction_goods_state"]
        if int(state) == 1:  # 1流拍
            # print("流拍")
            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["state"] = "商品已经流拍"
            dict1["user_name"] = "无"
            list11.append(dict1)
            # 分页
    list11.reverse()
    paginator = Paginator(list11, 2)
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
    return render(request,'my_auction_sale_two.html',locals())
def my_auction_sale_three(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    login_status = username
    # 从发布记录表里找到商品id
    cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s", [user_id])
    message = cur.fetchall()
    id_list = []
    id_list = []
    for i in message:
        id_list.append(i["release_auction_goods_id"])
    list12=[]
    for goods_id in id_list:
        dict1 = {}
        cur.execute("select auction_goods_state from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
        x = cur.fetchone()

        state = x["auction_goods_state"]
        if int(state) == 2:  # 2被竞拍成功
            # print("被竞拍成功")
            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message

            dict1["state"] = "商品已经被竞拍成功等待买家付款"
            cur.execute("select auction_order_buy_user_id from t_auction_order where auction_order_goods_id=%s",
                        [goods_id])
            buy_user_id = cur.fetchone()
            print(buy_user_id)
            cur.execute("select user_name from t_user where user_id=%s", [buy_user_id["auction_order_buy_user_id"]])
            user_name = cur.fetchone()["user_name"]
            dict1["user_name"] = user_name

            list12.append(dict1)
    list12.reverse()
    paginator = Paginator(list12, 2)
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
    return render(request,'my_auction_sale_three.html',locals())
def my_auction_sale_four(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    login_status = username
    # 从发布记录表里找到商品id
    cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s", [user_id])
    message = cur.fetchall()
    id_list = []
    id_list = []
    for i in message:
        id_list.append(i["release_auction_goods_id"])
    list13=[]
    for goods_id in id_list:
        dict1 = {}
        cur.execute("select auction_goods_state from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
        x = cur.fetchone()

        state = x["auction_goods_state"]
        if int(state) == 3:  # 商品付款成功

            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            cur.execute("select auction_order_id from t_auction_order where auction_order_goods_id=%s", [goods_id])
            order_id = cur.fetchone()["auction_order_id"]
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
            dict1["order"] = order_messge
            dict1["user_name"] = user_name
            cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s", [order_id])
            the_goods_state = cur.fetchone()["the_goods_state"]
            if the_goods_state:
                pass
                # dict1["the_goods_state"] = the_goods_state
                # list14.append(dict1)
            else:
                list13.append(dict1)
    list13.reverse()
    paginator = Paginator(list13, 2)
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
    return render(request,'my_auction_sale_four.html',locals())
def my_auction_sale_five(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    login_status = username
    # 从发布记录表里找到商品id
    cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s", [user_id])
    message = cur.fetchall()
    id_list = []
    id_list = []
    for i in message:
        id_list.append(i["release_auction_goods_id"])
    list14=[]
    for goods_id in id_list:
        dict1 = {}
        cur.execute("select auction_goods_state from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
        x = cur.fetchone()

        state = x["auction_goods_state"]
        if int(state) == 3:  # 商品付款成功

            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            cur.execute("select auction_order_id from t_auction_order where auction_order_goods_id=%s", [goods_id])
            order_id = cur.fetchone()["auction_order_id"]
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
            dict1["order"] = order_messge
            dict1["user_name"] = user_name
            cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s", [order_id])
            the_goods_state = cur.fetchone()["the_goods_state"]
            if the_goods_state:

                dict1["the_goods_state"] = the_goods_state
                list14.append(dict1)
    list14.reverse()
    paginator = Paginator(list14, 2)
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
    return render(request,'my_auction_sale_five.html',locals())
def my_auction_sale_six(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    login_status = username
    # 从发布记录表里找到商品id
    cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s", [user_id])
    message = cur.fetchall()
    id_list = []
    id_list = []
    for i in message:
        id_list.append(i["release_auction_goods_id"])
    list15=[]
    for goods_id in id_list:
        dict1 = {}
        cur.execute("select auction_goods_state from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
        x = cur.fetchone()

        state = x["auction_goods_state"]
        if int(state) == 4:  # 商品收货成功
            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            cur.execute("select auction_order_id from t_auction_order where auction_order_goods_id=%s", [goods_id])
            order_id = cur.fetchone()["auction_order_id"]
            cur.execute("select * from t_auction_order where auction_order_id=%s", [order_id])
            order_messge = cur.fetchone()
            cur.execute("select auction_order_buy_user_id from t_auction_order where auction_order_goods_id=%s",
                        [goods_id])
            buy_user_id = cur.fetchone()
            cur.execute("select user_name from t_user where user_id=%s", [buy_user_id["auction_order_buy_user_id"]])
            user_name = cur.fetchone()["user_name"]

            dict1["order"] = order_messge
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["user_name"] = user_name
            dict1["state"] = "商品已经收货"

            list15.append(dict1)
    list15.reverse()
    paginator = Paginator(list15, 2)
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
    return render(request,'my_auction_sale_six.html',locals())
def my_auction_sale_seven(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    login_status = username
    # 从发布记录表里找到商品id
    cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s", [user_id])
    message = cur.fetchall()
    id_list = []
    id_list = []
    for i in message:
        id_list.append(i["release_auction_goods_id"])
    list16=[]
    for goods_id in id_list:
        dict1 = {}
        cur.execute("select auction_goods_state from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
        x = cur.fetchone()

        state = x["auction_goods_state"]
        if int(state) == 6:  # 商品支付时间失效
            # print("被竞拍成功")
            cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
            goods_message = cur.fetchone()
            cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
            goods_auction_message = cur.fetchone()
            cur.execute("select * from t_auction_order where auction_order_goods_id=%s ", [goods_id])
            order_message = cur.fetchone()
            # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
            # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
            dict1["goods"] = goods_message
            dict1["attribute"] = goods_auction_message
            dict1["state"] = "商品已经超过付款时间"
            dict1["order"]=order_message
            cur.execute("select auction_order_buy_user_id from t_auction_order where auction_order_goods_id=%s",
                        [goods_id])
            buy_user_id = cur.fetchone()
            cur.execute("select user_name from t_user where user_id=%s", [buy_user_id["auction_order_buy_user_id"]])
            user_name = cur.fetchone()["user_name"]
            dict1["user_name"] = user_name

            list16.append(dict1)
    list16.reverse()
    paginator = Paginator(list16, 2)
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
    return render(request,'my_auction_sale_seven.html',locals())
def my_auction_one(request):
    user_id = request.session.get("user_id")
    list10 = []
    list11 = []
    list12 = []
    list13 = []
    list14 = []
    list15 = []
    list16 = []
    username = request.session.get('username')
    print(username)
    # 从发布记录表里找到商品id
    cur.execute("select release_auction_goods_id from t_release_auction where release_auction_user_id=%s", [user_id])
    message = cur.fetchall()
    id_list = []
    for i in message:
        id_list.append(i["release_auction_goods_id"])
    for goods_id in id_list:
        dict1 = {}
        cur.execute("select auction_goods_state from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
        x = cur.fetchone()

        state = x["auction_goods_state"]
        try:
            # 返回发布记录的时候就要判断他发布的商品是否5已经下架，2竞拍成功，4购买成功，3付款成功，1流拍
            if int(state) == 0:  # 0代表的是正常拍卖的
                # print("正常拍卖")

                cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
                goods_auction_message = cur.fetchone()
                # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
                # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
                dict1["goods"] = goods_message
                dict1["attribute"] = goods_auction_message
                dict1["state"] = "正在拍卖"
                # 返回当前竞拍者的姓名
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
                        cur.execute("select auction_goods_buyuser_id from t_auction_record where auction_record_id=%s",
                                    [record_maxid])
                        buy_user_id = cur.fetchone()
                        cur.execute("select user_name from t_user where user_id=%s",
                                    [buy_user_id["auction_goods_buyuser_id"]])
                        user_name = cur.fetchone()["user_name"]
                        if user_name:
                            dict1["user_name"] = user_name
                        else:
                            dict1["user_name"] = "无"
                list10.append(dict1)

            if int(state) == 1:  # 1流拍
                # print("流拍")
                cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
                goods_auction_message = cur.fetchone()
                # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
                # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
                dict1["goods"] = goods_message
                dict1["attribute"] = goods_auction_message
                dict1["state"] = "商品已经流拍"
                dict1["user_name"] = "无"
                list11.append(dict1)

            if int(state) == 2:  # 2被竞拍成功
                # print("被竞拍成功")
                cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
                goods_auction_message = cur.fetchone()
                # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
                # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
                dict1["goods"] = goods_message
                dict1["attribute"] = goods_auction_message

                dict1["state"] = "商品已经被竞拍成功等待买家付款"
                cur.execute("select auction_order_buy_user_id from t_auction_order where auction_order_goods_id=%s",
                            [goods_id])
                buy_user_id = cur.fetchone()
                cur.execute("select user_name from t_user where user_id=%s", [buy_user_id["auction_order_buy_user_id"]])
                user_name = cur.fetchone()["user_name"]
                dict1["user_name"] = user_name

                list12.append(dict1)

            if int(state) == 3:  # 商品付款成功

                cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
                goods_auction_message = cur.fetchone()
                cur.execute("select auction_order_id from t_auction_order where auction_order_goods_id=%s", [goods_id])
                order_id = cur.fetchone()["auction_order_id"]
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
                dict1["order"] = order_messge
                dict1["user_name"] = user_name
                cur.execute("select the_goods_state from t_auction_order where auction_order_id=%s", [order_id])
                the_goods_state = cur.fetchone()["the_goods_state"]
                if the_goods_state:
                    dict1["the_goods_state"] = the_goods_state
                    list14.append(dict1)
                else:
                    list13.append(dict1)

            if int(state) == 4:  # 商品收货成功
                cur.execute("select * from t_auction_goods_record where auction_goods_id=%s ", [goods_id])
                goods_message = cur.fetchone()
                cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
                goods_auction_message = cur.fetchone()
                # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
                # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
                cur.execute("select auction_order_id from t_auction_order where auction_order_goods_id=%s", [goods_id])
                order_id = cur.fetchone()["auction_order_id"]
                cur.execute("select * from t_auction_order where auction_order_id=%s", [order_id])
                order_messge = cur.fetchone()
                cur.execute("select auction_order_buy_user_id from t_auction_order where auction_order_goods_id=%s",
                            [goods_id])
                buy_user_id = cur.fetchone()
                cur.execute("select user_name from t_user where user_id=%s", [buy_user_id["auction_order_buy_user_id"]])
                user_name = cur.fetchone()["user_name"]

                dict1["order"] = order_messge
                dict1["goods"] = goods_message
                dict1["attribute"] = goods_auction_message
                dict1["user_name"] = user_name
                dict1["state"] = "商品已经收货"

                list15.append(dict1)

            if int(state) == 5:  # 商品被用户自己下架
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

        except Exception as e:
            print(e)

    return render(request, 'my_auction_sale_one.html', locals())
