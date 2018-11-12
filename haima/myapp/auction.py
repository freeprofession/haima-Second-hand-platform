import pymysql
import time
import json
import redis
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = con.cursor(pymysql.cursors.DictCursor)

history_auction = redis.Redis(host="47.100.200.132", port=6379, db=11, password='haima1234')
auction_img = redis.Redis(host="47.100.200.132", port=6379, db=5, password='haima1234')
message_push = redis.Redis(host="47.100.200.132", port=6379, db=11, password='haima1234')

import datetime


# 历史拍卖
def history_auction(request):
    list1 = []
    goods_list = []
    id = request.session.get('user_id')
    print(id)
    for item in history_auction.lrange("history", 0, 10):
        item = item.decode("utf-8")
        goods_list.append(item)
    cur.execute('select user_name from t_user where user_id=%s', [id])
    username = cur.fetchone()
    for goods_id in goods_list:
        dict1 = {}
        data_list = []
        cur.execute("select * from t_auction_goods where auction_goods_id=%s ", [goods_id])
        goods_messge = cur.fetchone()
        cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
        goods_auction_message = cur.fetchone()
        # 这里需要去两个表的数据，放不同的列表里,在前端需要用字典索引不能用二级列表
        # 所以在这里转化成两个字典，在存进列表，可以在前端遍历
        cur.execute("select end_date from t_auction_attribute where auction_goods_id=%s", [goods_id])
        end_data = cur.fetchone()["end_date"]
        data_list.append(end_data)
        dict1["goods"] = goods_messge
        dict1["attribute"] = goods_auction_message
        list1.append(dict1)
    return render(request, 'histroy_auction.html', locals())


# *********************************************拍卖商品的收货*******************************************************
def confirm_auction_goods(request):
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
    order_id = request.POST.get("order_id")
    # 用户确认收货以后改变状态
    user_id = request.session.get("user_id")
    print(order_id)
    try:
        now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("update t_auction_order set auction_order_state=%s,order_success_date=%s where auction_order_id=%s",
                    ["2", now_date, order_id])
        print("更新状态成功")
        cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s", [order_id])
        auction_goods_id = cur.fetchone()["auction_order_goods_id"]

        # history_auction.lpush("history",auction_goods_id)

        # 用户确认收货以后需要把钱打到卖家账户
        cur.execute("select auction_goods_margin from t_auction_attribute where auction_goods_id=%s",
                    [auction_goods_id])
        goods_margin = cur.fetchone()["auction_goods_margin"]
        cur.execute("select auction_goods_user_id from t_auction_goods_record where auction_goods_id=%s",
                    [auction_goods_id])
        maijia_id = cur.fetchone()["auction_goods_user_id"]
        cur.execute("select user_money from t_user where user_id=%s", [maijia_id])
        user_money = cur.fetchone()["user_money"]
        user_money = user_money + goods_margin
        cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, maijia_id])
        print("退钱成功")
        cur.execute("update t_auction_goods_record set auction_goods_state=%s where auction_goods_id=%s",
                    ["4", auction_goods_id])
        cur.execute("insert into t_evaluation (buy_id,evaluation_order_id,sell_id) values (%s,%s,%s)",
                    [str(user_id), str(order_id), str(maijia_id)])
        con.commit()
        print("收货成功")
    except Exception as e:
        con.rollback()
        print(e)
    return HttpResponse("/my_auction_buy_one/")


# ******************************************购买拍卖页面**********************************************
# 用户点击相应的商品图片或者竞拍按钮进入到商品的购买详情页
def buy_auction(request):
    id = request.session.get('user_id')
    username = request.session.get("username")
    login_status = username
    dict1 = {}
    list1 = []
    img_list = []
    if id:
        cur.execute('select user_name from t_user where user_id=%s', [id])
        username = cur.fetchone()
        print(username)
        print("123")
        goods_id = request.GET.get("id")
        print(goods_id)
        for item in auction_img.lrange(goods_id, 0, 4):
            item = item.decode("utf-8")
            img_list.append(item)
        print(img_list)
        cur.execute("select * from t_auction_goods where auction_goods_id=%s ", [goods_id])
        goods_messge = cur.fetchone()
        goods_user_id = goods_messge["auction_goods_user_id"]
        cur.execute("select * from t_auction_attribute where auction_goods_id=%s", [goods_id])
        goods_auction_message = cur.fetchone()
        dict1["goods"] = goods_messge
        dict1["attribute"] = goods_auction_message
        dict1["img"] = img_list
        print('图片的地址', img_list)
        print("12364456555")
        list1.append(dict1)
        return render(request, 'buy_auction.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# 拍卖首页
def auction_index(request):
    id = request.session.get('user_id')
    message_check1 = message_push.lrange(id, 0, 1)
    message_list_push = []
    message_list_push1 = message_push.lrange(id, 0, 3)
    for item in message_list_push1:
        message_list_push.append(item.decode("utf-8"))
    print(message_list_push)
    if message_check1:
        message_check = "../static/Images/new02.gif"
    else:
        message_check = "../static/Images/message.png"
    username = request.session.get("username")
    login_status = username
    list1 = []
    data_list = []
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s ',
        [id])
    collection_list = cur.fetchall()
    if id:
        goods_list = []
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
            cur.execute("select end_date from t_auction_attribute where auction_goods_id=%s", [goods_id])
            end_data = cur.fetchone()["end_date"]
            data_list.append(end_data)
            username = request.session.get("session")
            dict1["goods"] = goods_messge
            dict1["attribute"] = goods_auction_message
            list1.append(dict1)
        time_length = len(data_list)
        paginator = Paginator(list1, 5)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, "auction_index.html", locals())
    else:
        return HttpResponseRedirect('/login/')


# ********************************************我的拍卖********************************************************
# 默认是进入用户的发布历史界面
def my_auction(request):
    id = request.session.get('user_id')
    username = request.session.get("username")
    login_status = username
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
        return render(request, 'my_auction_sale_one.html', locals())
    else:
        return HttpResponseRedirect('/login/')


# ******************************************发布拍卖*****************************************
# 进入发布拍卖页面把他的名字显示出来


def release_auction(request):
    username = request.session.get("username")
    login_status = username
    id = request.session.get('user_id')
    message_check1 = message_push.lrange(id, 0, 1)
    message_list_push = []
    message_list_push1 = message_push.lrange(id, 0, 3)
    for item in message_list_push1:
        message_list_push.append(item.decode("utf-8"))
    print(message_list_push)
    if message_check1:
        message_check = "../static/Images/new02.gif"
    else:
        message_check = "../static/Images/message.png"
    login_status = username
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
    cur.execute("select user_money from t_user where user_id=%s", [user_id])
    user_money = cur.fetchone()["user_money"]
    username = request.session.get("username")
    login_status = username
    if request.method == 'POST':

        title = request.POST.get('title')
        desc = request.POST.get('desc')
        floorprice = request.POST.get('floorprice')
        floorpremium = request.POST.get("floorpremium")
        end_date = request.POST.get("end_date")
        start_date = request.POST.get("start_date")
        category = request.POST.get("category")
        print(category)
        postage = request.POST.get("postage")
        imgurl_list = json.loads(request.POST.get("img_address"))
        imgurl = "http://pgwecu7z4.bkt.clouddn.com/" + imgurl_list[0]
        list1 = []
        date_now = datetime.datetime.now().strftime('%Y-%m-%d')
        if title and desc and floorpremium and floorprice and end_date and start_date and category and postage:
            if len(title) >= 6 and floorpremium < floorprice and str(floorprice).isdigit() == True and str(
                    floorpremium).isdigit() == True \
                    and start_date == date_now and user_money >= 30:
                error = "ok"
                # 扣除保证金
                user_money = user_money - 30
                cur.execute("insert into t_auction_goods(auction_goods_title,auction_goods_desc,auction_goods_imgurl,\
                            auction_goods_user_id,auction_goods_category_id) values(%s,%s,%s,%s,%s)",
                            [title, desc, imgurl, \
                             str(user_id), str(category)])

                goods_id = cur.lastrowid
                # 把其余的图片传到redis
                for i in imgurl_list:
                    i = "http://pgwecu7z4.bkt.clouddn.com/" + i

                    auction_img.lpush(goods_id, i)
                try:
                    cur.execute(
                        "insert into t_release_auction(release_auction_date,release_auction_goods_id,release_auction_user_id) values (%s,%s,%s)" \
                        , [date_now, str(goods_id), str(user_id)])
                    cur.execute("insert into t_auction_goods_record(auction_goods_id,auction_goods_title,auction_goods_desc,auction_goods_imgurl,\
                                                    auction_goods_user_id,auction_goods_category_id) values(%s,%s,%s,%s,%s,%s)",
                                [str(goods_id), title, desc, imgurl, \
                                 str(user_id), str(category)])
                    cur.execute("insert into t_auction_attribute (start_date,end_date,auction_goods_floorprice,auction_goods_floorpremium,\
                                auction_goods_price,auction_goods_id) values (%s,%s,%s,%s,%s,%s)",
                                [start_date, end_date, floorprice, floorpremium, floorprice, str(goods_id)])
                    cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, user_id])
                    con.commit()
                except Exception as e:
                    con.rollback()
                    print(e)
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
            elif user_money < 30:
                error = "margin_error"
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
    print(return_title)
    if return_title == "one":
        list1 = []
        user_id = request.session.get("user_id")

    print(type(return_title))


# 发布拍卖成功
def release_auction_ok(request):
    return render(request, 'release_auction_ok.html')


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
    else:
        count_price = int(price) + int(permium)
        return HttpResponse(count_price)


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


# **********************************************************提前结束拍卖*************************************************
def end_auction(request):
    user_id = request.session.get("user_id")
    goods_id = request.POST.get("goods_id")
    cur.execute(
        "select auction_record_id from t_auction_record where auction_goods_id=%s",
        [goods_id])
    record_dict = cur.fetchall()
    # 在用户自己结束拍卖的时候还有人竞拍
    if record_dict:
        if record_dict:
            record_list = []
            for i in record_dict:
                record_list.append(i["auction_record_id"])
            record_maxid = max(record_list)
        # 找到开始竞拍的用户给退回保证金
        cur.execute("select auction_goods_buyuser_id from t_auction_record where auction_record_id=%s", [record_maxid])
        buy_user_id = cur.fetchone()["auction_goods_buyuser_id"]
        user_money = cur.execute("select user_money from t_user where user_id=%s", [buy_user_id])
        user_money += 30
        try:
            cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, user_id])
            # 将原来商品里面记录删除
            cur.execute("delete from t_auction_goods where auction_goods_id=%s", [goods_id])
            print("删除成功")
            # 将拍卖记录表里面的状态改变
            cur.execute(
                "update t_auction_record set auction_goods_state=%s where auction_record_id=%s",
                ['0', record_maxid])
            # 将商品里面的状态改成5，表示已经下架
            cur.execute("update t_auction_goods_record set auction_goods_state =%s where auction_goods_id=%s",
                        ["5", goods_id])
            con.commit()
            print("下架成功")
        except Exception as e:
            print(e)
    else:
        cur.execute("delete from t_auction_goods where auction_goods_id=%s", [goods_id])
        # 将商品里面的状态改成5，表示已经下架
        cur.execute("update t_auction_goods_record set auction_goods_state =%s where auction_goods_id=%s",
                    ["5", goods_id])
        print("删除成功")

        con.commit()
    return HttpResponse("/my_auction_sale_one/")


# ******************************************************判断拍卖时间************************************************
def Determine_auction_date(request):
    su = request.POST.get("su")
    cur.execute("select auction_goods_id  from t_auction_goods")
    list_goods_id = []
    dict_goods_id = cur.fetchall()
    for i in dict_goods_id:
        list_goods_id.append(i["auction_goods_id"])
    # 对现在的商品的id进行遍历
    for i in list_goods_id:
        cur.execute("select end_date from t_auction_attribute where auction_goods_id=%s", [i])
        end_date = cur.fetchone()["end_date"]
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        print(end_date)
        print(now_date)
        # 如果现在的时间已经到了拍卖结束时间
        if now_date > end_date:
            try:
                cur.execute("select auction_goods_user_id from t_auction_goods_record where auction_goods_id=%s", [i])
                user_id = cur.fetchone()["auction_goods_user_id"]
                # 退回保证金
                cur.execute("select user_money from t_user where user_id=%s", [user_id])
                user_money = cur.fetchone()["user_money"]
                user_money += 30
                cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, user_id])
                print("退回保证金成功")
                # 删除原来的商品
                cur.execute("delete from t_auction_goods where auction_goods_id=%s", [i])
                print("删除成功")
                # 判断商品当前有没有人竞拍
                cur.execute(
                    "select auction_goods_buyuser_id,auction_goods_price from t_auction_attribute where auction_goods_id=%s",
                    [i])
                x = cur.fetchone()
                who_buy = x["auction_goods_buyuser_id"]
                print(type(who_buy))
                price = x["auction_goods_price"]
                print(price)
                if str(who_buy) == '0':
                    print("没有人竞拍")
                    # 1商品流拍
                    state = "1"
                    cur.execute("update t_auction_goods_record set auction_goods_state =%s where auction_goods_id=%s",
                                [state, i])
                    print("修改商品的状态成功")
                else:
                    print("有人竞拍")
                    # 2商品有人竞拍
                    state = "2"
                    cur.execute("update t_auction_goods_record set auction_goods_state =%s where auction_goods_id=%s",
                                [state, i])
                    print("修改商品的状态成功")
                    # 将拍卖记录里面的状态修改
                    cur.execute(
                        "select auction_record_id from t_auction_record where auction_goods_id=%s",
                        [i])
                    record_dict = cur.fetchall()
                    if record_dict:
                        record_list = []
                        for i in record_dict:
                            record_list.append(i["auction_record_id"])
                        record_maxid = max(record_list)
                        print(record_maxid)
                        cur.execute(
                            "update t_auction_record set auction_goods_state=%s where auction_record_id=%s",
                            ['2', record_maxid])

                        print("修改商品的状态成功")
                        cur.execute("insert into t_auction_order (auction_order_date,auction_order_goods_id,auction_order_fianl_price,\
                                                                                    auction_order_buy_user_id) values (%s,%s,%s,%s)",
                                    [now_date, str(i), str(price), str(who_buy)])
                        print("添加订单成功")

                    con.commit()

            except Exception as e:

                print(e)
    print(su)
    return HttpResponse("你好")


# ********************************************返回支付拍卖成功的钱以后的跳转*********************************************
def pay_auction_money_ok(request):
    return render(request, "pay_auction_money_ok.html")


# *****************************************处理拍卖商品的发货************************************************************
def delivery(request):
    courier_number = request.POST.get("courier_number")
    order_id = request.POST.get("order_id")
    try:
        print("发货", order_id)
        cur.execute("update t_auction_order set the_goods_state=%s where auction_order_id=%s",
                    [courier_number, order_id])
        con.commit()
    except Exception as e:
        print(e)
    return HttpResponse("my_auction_sale_five.html")


def auction_place_order(request):
    username = request.session.get("username")
    login_status = username
    user_id = request.session.get("user_id")
    order_id = request.GET.get("id")
    cur.execute("select * from t_auction_order where auction_order_id=%s", [order_id])
    order_message = cur.fetchone()
    cur.execute(
        "select * from t_auction_goods_record left join t_auction_order on auction_goods_id=auction_order_goods_id where auction_order_id=%s",
        [order_id])
    goods_message = cur.fetchone()
    print(goods_message)
    return render(request, 'auction_place_order.html', locals())


# ***************************************付款时间判断*******************************************
def Determine_pay_date(request):
    now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    cur.execute(
        "select auction_order_id  from t_auction_order where (auction_order_date<%s and auction_order_state=%s) ",
        [now_date, '0'])
    order_id_list = cur.fetchall()
    if order_id_list:
        for i in order_id_list:
            cur.execute("select auction_order_goods_id from t_auction_order where auction_order_id=%s",
                        [str(i["auction_order_id"])])
            goods_id = cur.fetchone()["auction_order_goods_id"]
            try:
                cur.execute("update t_auction_order set auction_order_state=%s where auction_order_id=%s",
                            ["3", i["auction_order_id"]])
                cur.execute("update t_auction_goods_record set auction_goods_state=%s where auction_goods_id=%s",
                            ['6', goods_id])
                print("操作成功")
                con.commit()
            except Exception as e:
                con.rollback()
                print(e)
    return HttpResponse("ok")
    # and auction_order_date = % s


def time_test(request):
    return render(request, 'test_time.html')


def test_auction_pay_time(request):
    return render(request, 'test_auction_pay_time.html')


# 这里是拍卖首页分类的：
def cate_auction_index(request):
    cate_id = request.GET.get("id")
    id = request.session.get('user_id')
    list1 = []
    data_list = []
    cur.execute(
        'select * from t_goods right join t_user_collection on collection_goods_id=goods_id where collection_user_id=%s ',
        [id, ])
    collection_list = cur.fetchall()

    goods_list = []
    cur.execute('select user_name from t_user where user_id=%s', [id])
    username = cur.fetchone()
    cur.execute("select auction_goods_id from t_auction_goods where auction_goods_category_id=%s", [cate_id])
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
        cur.execute("select end_date from t_auction_attribute where auction_goods_id=%s", [goods_id])
        end_data = cur.fetchone()["end_date"]
        data_list.append(end_data)
        dict1["goods"] = goods_messge
        dict1["attribute"] = goods_auction_message
        list1.append(dict1)
    time_length = len(data_list)
    paginator = Paginator(list1, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "auction_index.html", locals())
