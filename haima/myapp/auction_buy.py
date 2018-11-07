import pymysql
import time
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = con.cursor(pymysql.cursors.DictCursor)
# **********************************************************返回用户的我的拍卖中心我的竞拍的界面**************************************
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

        return render(request, 'my_auction_four.html', locals())

