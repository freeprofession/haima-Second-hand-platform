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
from myapp import goods_recommend
from django.views.generic.base import RedirectView
from myapp import cz
from myapp import auction_pay
from myapp import auction_buy
from myapp import auction_sale
from myapp import auction

urlpatterns = [
    path('admin/', view.admin),
    path('admin_login/', view.admin_login),
    path('admin_goods/', view.admin_goods),
    path('admin_user/', view.admin_user),
    path('admin_order/', view.admin_order),
    path('admin_search_goods/', view.admin_search_goods),
    path('admin_search_user/', view.admin_search_user),
    path('admin_update/', view.admin_update),
    path('exit/', view.exit),
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
    path('publish/', view.goods_republish),
    path('publish_ok/', view.publish_ok),
    path('pub_success/', view.pub_success),
    path('assess/', view.assess),
    path('assess_ajax/', view.assess_ajax),
    path('auction_index/', auction.auction_index),
    # 用户中心--------------------------------------
    path('user_center/', view.user_center),
    path('user_credit/', view.user_credit),  # 用户信誉
    path('my_collection/', view.my_collection),
    path('system_message/', view.system_message),
    path('leave_message/', view.leave_message),
    path('leave_message_two/', view.leave_message_two),
    path('leave_message_three/', view.leave_message_three),
    path('user_lower_goods/', view.user_lower_goods),
    path('my_sale_lower/', view.my_sale_lower),
    path('my_sale/', view.my_sale),
    path('my_buy/', view.my_buy),
    path('my_sale_complete/', view.my_sale_complete),
    path('my_evaluate_get/', view.my_evaluate_get),
    path('my_evaluate_give/', view.my_evaluate_give),
    path('my_buy_complete/', view.my_buy_complete),
    path('order_mark/', view.order_mark),
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
    path('history_auction/', auction.history_auction),
    path('test/', view.text_message),
    path('test_ajax', view.test_ajax),
    # 获取图片上传token
    path('gettokendata/', view.gettokendata), path('modify_information/', view.modify_information),  # 修改信息
    path('my_auction/', auction.my_auction),
    path('history_auction/', auction.history_auction),
    path('release_auction/', auction.release_auction),
    path('test/', view.text_message),
    path('test_ajax', view.test_ajax),
    path('my_auction/', auction.my_auction),
    # 获取图片上传token
    path('gettokendata/', view.gettokendata),
    path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),
    path('modify_information/', view.modify_information),  # 修改信息
    path('modify_password/', view.modify_password),  # 修改密码

    path('modify_password/', view.modify_password),  # 修改密码
    path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),
    path('modify_information/', view.modify_information),  # 修改信息

    # path('modify_information/', view.modify_information),
    path('buy_auction/', auction.buy_auction),

    # 实时计算拍卖总价的路径
    path('calculate_price/', auction.calculate_price),
    # 返回用户的拍卖发布历史记录

    path("my_release_record/", auction.my_release_record),
    path('publish_auction/', auction.publish_auction),
    path('release_auction_ok/', auction.release_auction_ok),
    path('buy_auction/', auction.buy_auction),
    # 实时计算拍卖总价的路径
    path('calculate_price/', auction.calculate_price),

    # 用户输完价格确认竞拍
    path("confirm_buy/", auction.confirm_buy),
    # 用户支付成功以后的跳转
    path("buy_auction_ok/", auction.buy_auction_ok),
    # 提前结束拍卖
    path("end_auction/", auction.end_auction),
    # 普通商品的购买
    # 普通商品购买成功
    path("buy_goods_ok/", view.buy_goods_ok),
    # 拍卖时间结束的判断

    path("send_sms/", view.send_sms),
    path("goods_recommend/", goods_recommend.goods_recommend),  # 商品推荐
    path("my_auction_one/", auction_sale.my_auction_one),
    path("my_auction_four/", auction_buy.my_auction_four),
    # 普通商品收货

    path("Determine_auction_date/", auction.Determine_auction_date),
    path('publish_auction/', auction.publish_auction),
    path('release_auction_ok/', auction.release_auction_ok),
    path('buy_auction/', auction.buy_auction),
    # 实时计算拍卖总价的路径
    path('calculate_price/', auction.calculate_price),
    # 返回用户的全部拍卖记录

    path("my_auction_four/", auction_buy.my_auction_four),
    # 普通商品收货
    path("confirm_goods/", view.confirm_goods),
    # 拍卖商品竞拍成功后，支付尾款
    # 拍卖商品收货
    path("confirm_auction_goods/", auction.confirm_auction_goods),
    path("send_sms/", view.send_sms),
    path("page1/", view.page1),
    path("page2", view.page2),
    # 普通商品收货
    path("confirm_goods/", view.confirm_goods),
    # 拍卖商品竞拍成功后，支付尾款

    path("send_sms/", view.send_sms),
    path("goods_recommend/", goods_recommend.goods_recommend),

    path("my_auction_one/", auction_sale.my_auction_one),

    # 用户输完价格确认竞拍
    path("confirm_buy/", auction.confirm_buy),
    # 用户支付成功以后的跳转

    path("buy_auction_ok/", auction.buy_auction_ok),

    path("confirm_goods/", view.confirm_goods),
    # 拍卖商品发货
    path("delivery/", auction.delivery),
    # 拍卖商品收货
    path("confirm_auction_goods/", auction.confirm_auction_goods),
    path('page1/', view.page1),
    path('page2/', view.page2),
    path('page3/', cz.page3),
    path('top_up_money/', cz.top_up_money),  # 充值
    path('auction_money/', auction_pay.auction_money),
    path('page4/', auction_pay.page4),
    path('place_order/', view.place_order),
    path("my_auction_buy_one/", auction_buy.my_auction_buy_one),
    path("my_auction_buy_two/", auction_buy.my_auction_buy_two),
    path("my_auction_buy_three/", auction_buy.my_auction_buy_three),
    path("my_auction_buy_four/", auction_buy.my_auction_buy_four),
    path("my_auction_buy_five/", auction_buy.my_auction_buy_five),
    path("my_auction_buy_six/", auction_buy.my_auction_buy_six),
    path("my_auction_sale_one/", auction_sale.my_auction_sale_one),
    path("my_auction_sale_two/", auction_sale.my_auction_sale_two),
    path("my_auction_sale_three/", auction_sale.my_auction_sale_three),
    path("my_auction_sale_four/", auction_sale.my_auction_sale_four),
    path("my_auction_sale_five/", auction_sale.my_auction_sale_five),
    path("my_auction_sale_six/", auction_sale.my_auction_sale_six),
    path("my_auction_sale_seven/", auction_sale.my_auction_sale_seven),
    path('auction_place_order/', auction.auction_place_order),
    path('Determine_pay_date/', auction.Determine_pay_date),
    path('time_test/', auction.time_test),
    path('search_image/', view.search_image),
    path('test_auction_pay_time/',auction.test_auction_pay_time),
    path('cate_auction_index/',auction.cate_auction_index),


]
