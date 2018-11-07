import pymysql
import time
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = con.cursor(pymysql.cursors.DictCursor)
import datetime
# 历史拍卖
def history_auction(request):
    id = request.session.get('user_id')
    print(id)
    if id:
        cur.execute('select user_name from t_user where user_id=%s',[id])
        username = cur.fetchone()
        return render(request, 'histroy_auction.html', locals())


# *********************************************拍卖商品的收货*******************************************************
def confirm_auction_goods(request):
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
        # 用户确认收货以后需要把钱打到卖家账户
        cur.execute("select auction_goods_margin from t_auction_attribute where auction_goods_id=%s",
                    [auction_goods_id])
        goods_margin = cur.fetchone()["auction_goods_margin"]
        cur.execute("select auction_goods_user_id from t_auction_goods_record where auction_goods_id=%s",
                    [auction_goods_id])
        maijia_id = cur.fetchone()["auction_goods_user_id"]
        cur.execute("select user_money from t_user where user_id=%s", [maijia_id])
        user_money = cur.fetchone()["user_money"]
        user_money = user_money  + goods_margin
        cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, maijia_id])
        print("退钱成功")
        cur.execute("update t_auction_goods_record set auction_goods_state=%s where auction_goods_id=%s",
                    ["4", auction_goods_id])
        cur.execute("insert into t_evaluation (buy_id,evaluation_order_id,sell_id) values (%s,%s,%s)",[str(user_id),str(order_id),str(maijia_id)])
        con.commit()
        print("收货成功")
    except Exception as e:
        con.rollback()
        print(e)
    return HttpResponse("/my_auction_four/")