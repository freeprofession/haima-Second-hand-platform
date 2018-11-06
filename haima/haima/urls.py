"""haima URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import view

from django.views.generic.base import RedirectView
from myapp import cz

urlpatterns = [
    path('admin/', view.admin),
    path('admin_login/', view.admin_login),
    path('admin_goodslist/', view.admin_goodslist),
    path('', view.homepage),

    path('haima/', view.homepage),
    path('login/', view.login),
    path('login_ajax/', view.login_ajax),
    path('captcha/', include('captcha.urls')),
    path('register/', view.register),
    path('register_ajax/', view.register_ajax),
    path('code/', view.code),
    path('register_ok/', view.register_ok),
    path('goods_list/', view.goods_list),
    path('publish/', view.publish),
    path('pub_success/', view.pub_success),
    path('assess/', view.assess),
    path('assess_ajax/', view.assess_ajax),
    path('auction_index/', view.auction_index),
    # 用户中心--------------------------------------
    path('user_center/', view.user_center),
    path('user_credit/', view.user_credit),  # 用户信誉
    path('my_collection/', view.my_collection),
    path('leave_message/', view.leave_message),
    path('leave_message_two/', view.leave_message_two),
    path('user_lower_goods/', view.user_lower_goods),
    path('my_sale_lower/', view.my_sale_lower),
    path('my_sale/', view.my_sale),
    path('my_buy/', view.my_buy),
    path('my_sale_complete/', view.my_sale_complete),
    path('my_evaluate_get/', view.my_evaluate_get),
    path('my_evaluate_give/', view.my_evaluate_give),
    path('my_buy_complete/', view.my_buy_complete),
    # 商品详情-------------------------
    path('goods_detail/', view.goods_detail),
    path('goods_detail_ajax/', view.goods_detail_ajax),
    path('review_ajax/', view.review_ajax),
    path('lea_message/', view.lea_message),
    path('collection/', view.collection),
    path('lower_goods/', view.lower_goods),
    path('evaluate/', view.evaluate),
    path('evaluate_ajax/', view.evaluate_ajax),
    # -------------------------
    path('my_auction/', view.my_auction),
    path('history_auction/', view.history_auction),
    path('release_auction/', view.release_auction),
    path('test/', view.text_message),
    path('test_ajax', view.test_ajax),
    path('my_auction/', view.my_auction),
    # 获取图片上传token
<<<<<<< HEAD
    path('gettokendata/', view.gettokendata),
    path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),
    path('modify_information/', view.modify_information),  # 修改信息
    path('modify_password/', view.modify_password),  # 修改密码
=======

    path('gettokendata/', view.gettokendata), path('modify_information/', view.modify_information),  # 修改信息
    path('modify_password/', view.modify_password),  # 修改密码


    path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),

    path('modify_information/', view.modify_information),  # 修改信息

    path('modify_information/', view.modify_information),  # 修改信息
    # path('modify_information/', view.modify_information),

>>>>>>> 869b82d8ad65aff779393a69d50ef0469c8e3f35
    path('buy_auction/', view.buy_auction),
    # 实时计算拍卖总价的路径
    path('calculate_price/', view.calculate_price),
    # 返回用户的拍卖发布历史记录
    path("my_release_record/", view.my_release_record),
    path('publish_auction/', view.publish_auction),
    path('release_auction_ok/', view.release_auction_ok),
    path('buy_auction/', view.buy_auction),
    # 实时计算拍卖总价的路径
    path('calculate_price/', view.calculate_price),
    # 用户输完价格确认竞拍
    path("confirm_buy/", view.confirm_buy),
    # 用户支付成功以后的跳转
    path("buy_auction_ok/", view.buy_auction_ok),
    # 提前结束拍卖
    path("end_auction/", view.end_auction),
    # 普通商品的购买
    # 普通商品购买成功
    path("buy_goods_ok/", view.buy_goods_ok),
    # 拍卖时间结束的判断
    path("Determine_auction_date/", view.Determine_auction_date),
    path('publish_auction/', view.publish_auction),
    path('release_auction_ok/', view.release_auction_ok),
    path('buy_auction/', view.buy_auction),
    # 实时计算拍卖总价的路径
    path('calculate_price/', view.calculate_price),
    # 返回用户的全部拍卖记录
    path("my_auction_one/", view.my_auction_one),
    path("my_auction_two/", view.my_auction_two),
    path("my_auction_three/", view.my_auction_three),
    path("my_auction_four/", view.my_auction_four),
<<<<<<< HEAD
=======

    # 用户输完价格确认竞拍
    path("confirm_buy/", view.confirm_buy),
    # 用户支付成功以后的跳转
    path("buy_auction_ok/", view.buy_auction_ok),
    # 普通商品收货
    path("confirm_goods/", view.confirm_goods),
    # 拍卖商品竞拍成功后，支付尾款
    path("pay_auction_money/", view.pay_auction_money),
    # 支付拍卖尾款成功
    path("pay_auction_money_ok/", view.pay_auction_money_ok),
    # 拍卖商品发货
    path("delivery/", view.delivery),
    # 拍卖商品收货
    path("confirm_auction_goods/", view.confirm_auction_goods),
    path("send_sms/", view.send_sms),

>>>>>>> 869b82d8ad65aff779393a69d50ef0469c8e3f35
    # 普通商品收货
    path("confirm_goods/", view.confirm_goods),
    # 拍卖商品竞拍成功后，支付尾款
    path("pay_auction_money/", view.pay_auction_money),
    # 支付拍卖尾款成功
    path("pay_auction_money_ok/", view.pay_auction_money_ok),
    # 拍卖商品发货
    path("delivery/", view.delivery),
    # 拍卖商品收货
    path("confirm_auction_goods/", view.confirm_auction_goods),
    path("send_sms/", view.send_sms),
<<<<<<< HEAD
=======

>>>>>>> 869b82d8ad65aff779393a69d50ef0469c8e3f35
]
