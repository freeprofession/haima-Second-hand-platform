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

# from django.views.generic.base import RedirectView

urlpatterns = [
    path('haima/', view.homepage),
    path('login/', view.login),
    path('login_ajax/', view.login_ajax),
    path('captcha/', include('captcha.urls')),
    path('register/', view.register),
    path('register_ajax/', view.register_ajax),
    path('code/', view.code),
    path('register_ok/', view.register_ok),
    path('goods_list/', view.goods_list),
    path('user_center/', view.user_center),
    path('publish/', view.publish),
    path('assess/', view.assess),
    path('auction_index/', view.auction_index),
    path('my_sale/', view.my_sale),
    path('my_buy/', view.my_buy),
    # path('address/', view.address),
    path('goods_detail/', view.goods_detail),
    path('goods_detail_ajax/', view.goods_detail_ajax),
    path('gettokendata/', view.gettokendata),
    path('my_auction/', view.my_auction),
    path('history_auction/', view.history_auction),
    path('release_auction/', view.release_auction),
    path('test/', view.text_message),
    path('test_ajax', view.test_ajax),
    path('my_auction/', view.my_auction),
    path('my_collection/', view.my_collection),
    path('evaluate/', view.evaluate),
    path('my_evaluate_get/', view.my_evaluate_get),
    path('my_evaluate_give/', view.my_evaluate_give),
    path('leave_message/', view.leave_message),
    # path("favicon.ico", RedirectView.as_view(url='static/favicon.ico')),
    path('publish_auction/', view.publish_auction),
    path('release_auction_ok/', view.release_auction_ok),
<<<<<<< HEAD
    path('publish_auction/',view.publish_auction),
    path('release_auction_ok/',view.release_auction_ok),
    path('buy_auction/',view.buy_auction),
    #实时计算拍卖总价的路径
    path('calculate_price/',view.calculate_price),
    #返回用户的拍卖发布历史记录
    path("my_release_record/",view.my_release_record),




=======
    path('publish_auction/', view.publish_auction),
    path('buy_auction/', view.buy_auction),
    #实时计算拍卖总价的路径
    path('calculate_price/',view.calculate_price),
>>>>>>> b62fb970b05ffb59d5482216a7a7beaa0d40655a
]
