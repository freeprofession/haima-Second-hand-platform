import pymysql
import time
import datetime
from utils.pay import AliPay
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = con.cursor(pymysql.cursors.DictCursor)
def get_ali_object():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2016092000555548"  #  APPID （沙箱应用）
    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
    # notify_url = "http://47.94.172.250:8804/page2/"
    notify_url = "http://127.0.0.1:80/page4/"
    # 支付完成后，跳转的地址。
    return_url = "http://127.0.0.1:80/page4/"
    merchant_private_key_path = "keys/app_private_2048.txt" # 应用私钥
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

#前端跳转的支付页面
def auction_money(request):
    # 根据当前用户的配置，生成URL，并跳转。
    money = request.POST.get('price')
    order_id=request.POST.get('order_id')
    request.session['auction_order_id'] = order_id
    phone = request.POST.get('phone')
    name = request.POST.get('name')
    address = request.POST.get('address') + request.POST.get("user_address")
    alipay = get_ali_object()
    request.session['auction_user_buy_phone'] = phone
    request.session['auction_name'] = name
    request.session['auction_address'] = address
    print(money,phone,name,address)
     # 生成支付的url
    query_params = alipay.direct_pay(
        subject="拍卖支付尾款"+money,  # 商品简单描述
        out_trade_no="x2" + str(time.time()),  # 用户购买的商品订单号（每次不一样） 20180301073422891
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)

    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
    print(pay_url)
    return HttpResponse(pay_url)


def page4(request):
    con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = con.cursor(pymysql.cursors.DictCursor)
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
        cur.execute("select user_money from t_user where user_id=%s", [user_id])
        user_money = cur.fetchone()["user_money"]
        order_id=request.session.get("auction_order_id")
        auction_user_name=request.session.get("auction_name")
        auction_phone=request.session.get("auction_user_buy_phone")
        address=request.session.get("auction_address")
        # 通过订单id找到商品id
        cur.execute("select auction_order_goods_id from t_auction_order where  auction_order_id=%s", [order_id])
        goods_id = cur.fetchone()["auction_order_goods_id"]
        # 通过商品id找到保证金
        cur.execute("select auction_goods_margin from t_auction_attribute where auction_goods_id=%s", [goods_id])
        goods_margin = cur.fetchone()["auction_goods_margin"]
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================开始==================')
        print('GET验证', status)
        print('==================结束==================')
        print("支付成功")

        try:
            user_money = user_money + goods_margin
            # 付款以后把把保证金退还
            cur.execute("update t_user set user_money=%s where user_id=%s", [user_money, user_id])
            # 将订单那个状态改成1
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            cur.execute("update t_auction_order set auction_order_state=%s,pay_money_date=%s,order_address=%s,order_name=%s,order_phone=%s where auction_order_id=%s",
                        ["1",now_time ,address,auction_user_name,auction_phone,order_id])
            # 将商品记录表里的状态改成3,付款时间也改一下
            print("订单修改完成")
            cur.execute(
                "update t_auction_goods_record set auction_goods_state=%s where auction_goods_id=%s",
                ["3", goods_id])
            con.commit()
            print("操作完成")
            return redirect("/my_auction_buy_five/")
        except Exception as e:

            print(e)
