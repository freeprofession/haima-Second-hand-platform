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

urlpatterns = [
    path("", view.homepage),
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
    path('auction_index/', view.auction_index),
    path('my_sale/', view.my_sale),
    path('my_buy/', view.my_buy),
    # 用户中心--------------------------------------
    path('user_center/', view.user_center),
    path('user_credit/', view.user_credit),  # 用户信誉
    path('my_collection/', view.my_collection),
    path('leave_message/', view.leave_message),
    path('leave_message_two/', view.leave_message_two),
    # 商品详情-------------------------
    path('goods_detail/', view.goods_detail),
    path('goods_detail_ajax/', view.goods_detail_ajax),
    path('review_ajax/', view.review_ajax),
    path('lea_message/', view.lea_message),
    path('collection/', view.collection),
    path('leave_message/', view.leave_message),
    path('leave_message_two/', view.leave_message_two),
    path('lower_goods/', view.lower_goods),
    # -------------------------
    path('callback/', view.callback),
    path('my_auction/', view.my_auction),
    path('history_auction/', view.history_auction),
    path('release_auction/', view.release_auction),
    path('test/', view.text_message),
    path('test_ajax', view.test_ajax),
    path('my_auction/', view.my_auction),
    path('evaluate/', view.evaluate),
    path('my_evaluate_get/', view.my_evaluate_get),
    path('my_evaluate_give/', view.my_evaluate_give),
    # 获取图片上传token
    path('gettokendata/', view.gettokendata),
    path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),
<<<<<<< HEAD
    path('modify_information/', view.modify_information),  # 修改信息
    path('modify_password/', view.modify_password),  # 修改密码

=======
    path('modify_information/', view.modify_information),
    path('modify_information/', view.modify_information), # 修改信息
    # path('modify_information/', view.modify_information),
>>>>>>> 4de8f5ca56e48374ee3f7eafcd87f01da0d514e5
    path('buy_auction/', view.buy_auction),
    # 实时计算拍卖总价的路径
    path('calculate_price/', view.calculate_price),
    # 返回用户的拍卖发布历史记录
    path("my_release_record/", view.my_release_record),
<<<<<<< HEAD
=======



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
    # 用户输完价格确认竞拍
    path("confirm_buy/", view.confirm_buy),
    # 用户支付成功以后的跳转
    path("buy_auction_ok/", view.buy_auction_ok),

>>>>>>> 4de8f5ca56e48374ee3f7eafcd87f01da0d514e5
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
    # 用户输完价格确认竞拍
    path("confirm_buy/", view.confirm_buy),
    # 用户支付成功以后的跳转
    path("buy_auction_ok/", view.buy_auction_ok),

]
