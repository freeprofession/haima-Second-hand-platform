import pymysql
import redis
from django.test import TestCase
import json
import re

r = redis.Redis(host="47.100.200.132", port=6379)
conn = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)
# cur.execute("select * from t_message where message_goods_id=%s", [1, ])
# a = cur.fetchall()
# cur.execute("select * from t_second_message right join t_user on child_user_id=user_id where  second_goods_id=%s",
#             [1, ])
# b = cur.fetchall()
# c_comment_dict = {}
# cur.execute('select * from t_message right join t_user on message_user_id=user_id where message_goods_id=%s ', [1, ])
# c = cur.fetchall()
# for d in b:
#     id = d.get('second_message_id')
#     c_comment_dict[id] = d
# p_comment_dict = {}
# for d in c:
#     id = d.get('message_user_id')
#     p_comment_dict[id] = d
# print(p_comment_dict)
#
# for i in p_comment_dict:
#     lst = []
#     for j in c_comment_dict:
#         if p_comment_dict[i]['message_user_id'] == c_comment_dict[j]['parent_user_id']:
#             lst.append(c_comment_dict[j])
#     p_comment_dict[i]['child_message'] = lst
# # print(p_comment_dict)
#
# ppppp = [{'1': {'message_id': 1, 'message_user_id': '1', 'message_desc': 'jqlove', 'message_goods_id': 1,
#                 'message_date': '2018-10-22', 'child_message': None, 'user_id': 1, 'user_name': 'jqlove',
#                 'user_password': '123456',
#                 'user_imgurl': 'http://img.crawler.qq.com/lolwebvideo/20170802165439/c91a5a13e7bff101a4a75aecc191b075/0',
#                 'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': '2018-10-22', 'user_money': 100.0,
#                 'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
#           '2': {'message_id': 2, 'message_user_id': '2', 'message_desc': 'clear', 'message_goods_id': 1,
#                 'message_date': '2018-10-23', 'child_message': None, 'user_id': 1, 'user_name': 'jqlove',
#                 'user_password': '123456',
#                 'user_imgurl': 'http://img.crawler.qq.com/lolwebvideo/20170802165439/c91a5a13e7bff101a4a75aecc191b075/0',
#                 'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': '2018-10-22', 'user_money': 100.0,
#                 'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
#           '3': {'message_id': 3, 'message_user_id': '3', 'message_desc': '43976', 'message_goods_id': 1,
#                 'message_date': '2018-10-23', 'child_message': None, 'user_id': 1, 'user_name': 'jqlove',
#                 'user_password': '123456',
#                 'user_imgurl': 'http://img.crawler.qq.com/lolwebvideo/20170802165439/c91a5a13e7bff101a4a75aecc191b075/0',
#                 'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': '2018-10-22', 'user_money': 100.0,
#                 'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'}}]
tt = """            <div class="reply">

                   <div style="margin-left: 100px">
                       <img src="{0}" alt="" height="50" width="50">
                       {1}
                       <p>{2}<input type="text" id="message"><input type="button" value="回复"
                                                                                        id="btn_message"></p>
                       <p><input type="text" id="c_message" value="" hidden></p>
                   </div>

           </div>"""
# a = tt.format('ddddd', 'jqlopv', 'wwweq')
# print(a)
# template = "回复clearlove:dsaddadaddsd@454:"
# rule = r':(.*)'
# slotList = re.findall(rule, template)[0]
# print(slotList)
# rr = """ <dl>
#                                     <dd style="margin-left: 75px;height: 50px;">
#                                         <input type="text" id="child_user_id" value="{{ item.child_user_id }}" hidden>
#                                         <img src="{{ item.user_imgurl }}" alt="" height="40" width="40">
#                                         <div style="margin-left: 45px;position: relative;top: -50px;"><a
#                                                 href="" style="color: #2d64b3"
#                                                 class="c_name_{{ item.second_message_id }}">{{ item.user_name }}</a>:
#                                             <span style="color: #333333;font-size: 14px">{{ item.second__desc }}</span>
#                                             <div><span style="color: #a3a3a3">{{ item.second_date }}</span>
#                                                 <a name="abc">1</a>
#                                                 <input id="review" class="c_review_{{ item.second_message_id }}"
#                                                        type="button" value="回复"
#                                                        onclick="c_review({{ item.second_message_id }})">
#                                             </div>
#                                         </div>
#                                     </dd>
#                                 </dl>"""
# tt = [{'second_message_id': 1, 'parent_user_id': '6', 'second_desc': '爱你哦', 'second_goods_id': '1',
#        'second_date': '2018-10-26 11:05:07', 'child_user_id': '1', 'to_rid': '1', 'user_id': 1, 'user_name': 'jqlove',
#        'user_password': '123456',
#        'user_imgurl': 'http://img.crawler.qq.com/lolwebvideo/20170802165439/c91a5a13e7bff101a4a75aecc191b075/0',
#        'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': '2018-10-22', 'user_money': 100.0,
#        'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
#       {'second_message_id': 2, 'parent_user_id': '1', 'second_desc': '爱我的哇啊切 ', 'second_goods_id': '1',
#        'second_date': '2018-10-26 11:16:11', 'child_user_id': '1', 'to_rid': '1', 'user_id': 1, 'user_name': 'jqlove',
#        'user_password': '123456',
#        'user_imgurl': 'http://img.crawler.qq.com/lolwebvideo/20170802165439/c91a5a13e7bff101a4a75aecc191b075/0',
#        'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': '2018-10-22', 'user_money': 100.0,
#        'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
#       {'second_message_id': 3, 'parent_user_id': '2', 'second_desc': '挨打的而且', 'second_goods_id': '1',
#        'second_date': '2018-10-26 11:16:19', 'child_user_id': '1', 'to_rid': '2', 'user_id': 1, 'user_name': 'jqlove',
#        'user_password': '123456',
#        'user_imgurl': 'http://img.crawler.qq.com/lolwebvideo/20170802165439/c91a5a13e7bff101a4a75aecc191b075/0',
#        'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': '2018-10-22', 'user_money': 100.0,
#        'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
#       {'second_message_id': 4, 'parent_user_id': '1', 'second_desc': '回复jqlovejqlovejqlovejqlove:nmsl',
#        'second_goods_id': '1', 'second_date': '2018-10-26 11:17:02', 'child_user_id': '2', 'to_rid': '1', 'user_id': 2,
#        'user_name': 'clearlove', 'user_password': '123456',
#        'user_imgurl': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540203476459&di=4e89eef785b6e15ddc965e80e15fcdfb&imgtype=0&src=http%3A%2F%2Fwww.gamemei.com%2Fbackground%2Fuploads%2Fallimg%2F20160525%2F1464153091927021.jpg',
#        'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': ' 2018-10-22', 'user_money': 100.0,
#        'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
#       {'second_message_id': 5, 'parent_user_id': '2', 'second_desc': '?W?Das\nD  as a ', 'second_goods_id': '1',
#        'second_date': '2018-10-26 11:17:31', 'child_user_id': '2', 'to_rid': '2', 'user_id': 2,
#        'user_name': 'clearlove', 'user_password': '123456',
#        'user_imgurl': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540203476459&di=4e89eef785b6e15ddc965e80e15fcdfb&imgtype=0&src=http%3A%2F%2Fwww.gamemei.com%2Fbackground%2Fuploads%2Fallimg%2F20160525%2F1464153091927021.jpg',
#        'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': ' 2018-10-22', 'user_money': 100.0,
#        'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
#       {'second_message_id': 6, 'parent_user_id': '3', 'second_desc': 'ada qrqqerqtq', 'second_goods_id': '1',
#        'second_date': '2018-10-26 11:17:36', 'child_user_id': '2', 'to_rid': '3', 'user_id': 2,
#        'user_name': 'clearlove', 'user_password': '123456',
#        'user_imgurl': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540203476459&di=4e89eef785b6e15ddc965e80e15fcdfb&imgtype=0&src=http%3A%2F%2Fwww.gamemei.com%2Fbackground%2Fuploads%2Fallimg%2F20160525%2F1464153091927021.jpg',
#        'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': ' 2018-10-22', 'user_money': 100.0,
#        'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
#       {'second_message_id': 7, 'parent_user_id': '1', 'second_desc': 'sxada  dasdas ', 'second_goods_id': '1',
#        'second_date': '2018-10-26 11:18:05', 'child_user_id': '2', 'to_rid': '1', 'user_id': 2,
#        'user_name': 'clearlove', 'user_password': '123456',
#        'user_imgurl': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540203476459&di=4e89eef785b6e15ddc965e80e15fcdfb&imgtype=0&src=http%3A%2F%2Fwww.gamemei.com%2Fbackground%2Fuploads%2Fallimg%2F20160525%2F1464153091927021.jpg',
#        'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': ' 2018-10-22', 'user_money': 100.0,
#        'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'}]
#
# cur.execute("select * from t_second_message right join t_user on child_user_id=user_id where  second_goods_id=%s",
#             [1, ])
# b = cur.fetchall()
# c_comment_dict = {}
# for d in b:
#     id = d.get('second_message_id')
#     c_comment_dict[id] = d
# lst = []
# for j in c_comment_dict:
#     lst.append(c_comment_dict[j])
# print(c_comment_dict)
import datetime
import time

a = "2018-1-21"
# www = a.strftime('%Y-%m-%d')
# print(a)
# result_time = ptime.strftime('%Y-%m-%d')
# now_time = datetime.datetime.now().strftime('%Y-%m-%d')
# result_time1 = a
# d1 = datetime.datetime.strptime(result_time1, "%Y-%m-%d")
#
# result_time2 = now_time
# d2 = datetime.datetime.strptime(result_time2, "%Y-%m-%d")
# #
# d = str(d2 - d1)
# s=[]
# s=d.split(" ")
# print(d, s)
# day = now_time.split("-")
# day_ = a.split("-")
# year = int(day[0]) * 365 - int(day_[0])
# mon = int(day[1]) - int(day_[1])
# day1 = int(day[2]) - int(day_[2])
# print(year, mon, day1)

# 返回两个变量相差的值，就是相差天数
# 结果:47
# cur.execute("select * from t_goods where user_id=%s and goods_state=%s", [1, 0])
# goods_list = cur.fetchall()
# goods = {}
# lst = []
# count_list = {}
# for item in goods_list:
#     date = item.get('release_date')
#     goods[date] = ""
#     count_list[date] = ""
# for j in goods:
#     lst = []
#     count = 0
#     for item in goods_list:
#         if j == item['release_date']:
#             count += 1
#             lst.append(item)
#         for i in lst:
#             i["count"] = count
#             break
#     goods[j] = lst
# print(goods)
# goods_ = {}
# print(goods)
# for j in goods_:
#     for item in goods:
#         if goods[item]["release_date"] == j:
#             print(goods[item]["release_date"], j)
#             goods_[j].append(goods[item])
# print(goods_)

# for item in goods_list:
#     date = item.get('release_date')
#     if item["release_date"] == date:
#         count = +1
#         lst.append(item)
#     goods[date] = lst
#     goods["count"] = count
# print(goods)
# cur.execute(
#     'select * from t_second_message inner join t_user on child_user_id=user_id inner join t_goods on second_goods_id=goods_id where to_rid=%s ',
#     [1, ])
# review_list = cur.fetchall()
# print(review_list)
# day_ = "2018-10-31"
# now_time = datetime.datetime.now().strftime('%Y-%m-%d')
# d1 = datetime.datetime.strptime(day_, "%Y-%m-%d")
# d2 = datetime.datetime.strptime(now_time, "%Y-%m-%d")
# d3 = str(d1 - d2)
# print(d3.split(" ")[0])
# cur.execute("select * from t_goods  where user_id=%s and goods_state=%s order by goods_id desc",
#             [1, 0])
# goods_list = cur.fetchall()
# print(goods_list)
# a=0
# for item in goods_list:
#     if item["goods_id"] == 0:
#         a = goods_list.index(item) - 1
#         print(goods_list[a])
#
# print(a)
# cur.execute("select * from t_order_success  where release_user_id=%s or buy_user_id=%s",
#             [1, 1])
# goods_list = cur.fetchall()
# buy = []
# mai = []
# for i in goods_list:
#     # print(i["order_id"])
#     cur.execute("select * from t_evaluation  where evaluation_order_id=%s",
#                 [i["order_id"], ])
#     a = cur.fetchone()
#     if i["release_user_id"] == 1:
#         a["state"] = "卖家6666666666"
#         buy.append(a)
#     elif i["buy_user_id"] == 1:
#         a["state"] = "买家++++++++++"
#         buy.append(a)
# #         print(1111)
# # print(buy)
# # print(goods_list)
# cur.execute("select * from t_evaluation  where evaluation_order_id=%s",
#             [10, ])
# a = cur.fetchone()
# cur.execute("select order_id from t_order_success where buy_user_id=%s or release_user_id=%s",
#                         [1, 1])
# order_id = cur.fetchall()
# for i in order_id:
#     print(i)
# print(order_id)
set_eva = redis.Redis(host="47.100.200.132", port=6379, db=7)  # 设置评论
get_eva = redis.Redis(host="47.100.200.132", port=6379, db=8)  # 得到评论
# cur.execute("select order_id from t_order_success where buy_user_id=%s or release_user_id=%s",
#             [2, 2])
# order_id = cur.fetchall()
# eva_list = []
# for id in order_id:
#     one = {}
#     key = str(2) + str(id["order_id"])
#     a = get_eva.hgetall(key)
#     for i in a:
#         c = a[i].decode("utf-8")
#         i = i.decode("utf-8")
#         one[i]=c
#     eva_list.append(one)
# b = get_eva.hgetall(str(210))
# w={}
# print(eva_list)
a = [{'goods_id': 580670260232, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': 'iphone5s',
      'goods_desc': '16g 银色 型号A1528 请自行百度 功能一切正常 个人用的移动 没有4g 成色如图 售出不退 怕被调包 邮费自理 不议价 不闲聊 请自行百度\n', 'goods_price': 350.0,
      'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i2/O1CN011UvgJvvfjX7Sjav_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '河南驻马店 上蔡县5', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i2/580/670/580670260232/TB1uRwYlyLaK1RjSZFx8qumPFla.desc%7Cvar%5Edesc%3Bsign%5E1ddef7e357bc594c9bc45b5a362c8bee%3Blang%5Egbk%3Bt%5E1540801412'},
     {'goods_id': 580670168236, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '苹果6s 64G国行全网通粉色 无拆无修 全原装', 'goods_desc': '特价转让一台全原装的苹果6S 粉色 功能全好 无拆无修 看上的私聊 64G 内存\n',
      'goods_price': 1500.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i4/O1CN011LTRM4Ki5MmvPSo_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '四川成都 青羊区', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i5/580/670/580670168236/TB1cHEClrrpK1RjSZTE8qwWAVla.desc%7Cvar%5Edesc%3Bsign%5E92d168c5bfea322f54c13d8429f97e4a%3Blang%5Egbk%3Bt%5E1540801405'},
     {'goods_id': 580669616396, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '苹果6plus 9新 16G无密码有ID，当配件出',
      'goods_desc': '苹果6plus 9新 16G无密码有ID，当配件出，成色很好，一切原装的，没修过主板，没换过电池，没换过屏幕，屏没有划痕！\n问题:屏幕偶尔不灵，大部分时间都好使。\n         有ID，退不掉。\n当配件出吧\n本人芝麻721\n',
      'goods_price': 450.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/O1CN011YTWQqoNv6YkdFu_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '辽宁盘锦 兴隆台区', 'goods_postage': 0, 'goods_appearance': 1,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i2/580/661/580669616396/TB1qnswlzTpK1RjSZKP8qu3Upla.desc%7Cvar%5Edesc%3Bsign%5E592445785a9275c57c97ba569edd58d5%3Blang%5Egbk%3Bt%5E1540801413'},
     {'goods_id': 580668892295, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': 'iPhone 7 Plus 玫瑰金 128G 国行 8新',
      'goods_desc': 'iPhone 7 Plus 玫瑰金 128G 国行 箱说配件全 原码原盒 女生一手自用  无拆无修无进水 所有功能正常。屏幕没有明显的深的划痕，细微划痕强光下可见，不影响显示效果。最后一张图，左侧中间白色背景下有一点点暗影，不知什么原因，其他颜色背景下无。电池健康度87% ，视频中已经拍出显示效果的问题，其他没有任何暗病。橙色定义8新。手机价格不刀。\n',
      'goods_price': 2599.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/O1CN011Fhk1sq3gdqbmX2_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '北京北京 朝阳区', 'goods_postage': 0, 'goods_appearance': 1,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i1/580/661/580668892295/TB1EZEwlyrpK1RjSZFh8qtSdXla.desc%7Cvar%5Edesc%3Bsign%5Ed41d39a8abe5b0ac881c9299b4154364%3Blang%5Egbk%3Bt%5E1540800529'},
     {'goods_id': 580668512351, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': '华为荣耀10',
      'goods_desc': '全网通，6+64G低价出售，手机使用没任何问题，需要的联系，橙色不错，如图，手机换过原装后盖100多换的，送充电器，数据线，顺丰邮费到付，统一价\n', 'goods_price': 1480.0,
      'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i2/O1CN011eRaSCiOSvyi5Bv_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '江西萍乡 安源区', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i5/580/661/580668512351/TB1bnwxlrvpK1RjSZFq8qwXUVla.desc%7Cvar%5Edesc%3Bsign%5E66f5f7026376643d129dce61f1f4ab39%3Blang%5Egbk%3Bt%5E1540800522'},
     {'goods_id': 580668240587, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': 'iPhone7Plus128G亮黑色99新',
      'goods_desc': '机器成色如图！本人使用手机 不是其他人卖的那种便宜货妖机！本机Apple官网购买！一起购买的官方真皮保护壳！机器跟保护壳都有发票！因为一开始就用保护壳到现在 所以机器本身没有任何划痕 几近全新 苹果官方真皮套真的耐用！！屏幕也有膜 所以不用担心屏幕有划痕！了解苹果的都知道 亮黑色128G只在7P发售那段时期出现过！之后都只有64G的了！所以机器已经使用一年多了 不在保修期！！但是18年12月31号之前 可以享受一次200块钱官方售后换新电池的政策！！！电子产品换新电池意味着新生！！价格包含手机跟全套配件跟手机壳！大礼包！！懂的来！不接受砍价！！目前只接受同城面交！！！\n',
      'goods_price': 4000.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/O1CN011zI49SNzqrbpaYe_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '江苏常州 武进区', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i2/580/661/580668240587/TB1vPUClwHqK1RjSZFk8qt.WFla.desc%7Cvar%5Edesc%3Bsign%5E5ceb3349e1dae78b87b3296e5f3200a1%3Blang%5Egbk%3Bt%5E1540801421'},
     {'goods_id': 580667768716, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': '新款苹果XR全网通，',
      'goods_desc': '捡漏了！激活两天时间未使用，全套充新！\n白色，128G\n', 'goods_price': 6200.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/O1CN011YaqlfDK5tdGZay_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '陕西西安 新城区', 'goods_postage': 0, 'goods_appearance': 1,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i4/580/660/580667768716/TB1QmMDlq6qK1RjSZFm8qt0PFla.desc%7Cvar%5Edesc%3Bsign%5Ec5d1675d43fbecb415cf8f49c2e99fbb%3Blang%5Egbk%3Bt%5E1540801419'},
     {'goods_id': 580667416595, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': 'vivo y66L',
      'goods_desc': '全网通4G,   3+32G配置，  原装手机，屏幕无划伤，没有保护膜，后壳有划伤。看清成色拍，   手机功能使用正常，电池耐用没任何暗病，有问题包退！零风险购机，   没配件\n',
      'goods_price': 450.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i4/O1CN0123HqQHS56Mh4Y1t_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '山东德州 夏津县', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i7/580/660/580667416595/TB1akkvlrPpK1RjSZFF8qu5Ppla.desc%7Cvar%5Edesc%3Bsign%5Ec63d8f010a4208f98490675d68658101%3Blang%5Egbk%3Bt%5E1540800531'},
     {'goods_id': 580666572693, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '苹果7plus 128g国行黑色', 'goods_desc': '苹果7plus 128g国行黑色，原装无修，所有功能正常，指纹灵敏，9.3新，非诚勿扰！\n',
      'goods_price': 2999.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i4/O1CN011TMaM4BQXCl8S4Q_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 1, 'goods_address': '广东深圳 龙岗区', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i8/580/660/580666572693/TB1MFcslxTpK1RjSZFG8qwHqFla.desc%7Cvar%5Edesc%3Bsign%5E4c3b2d762ac43f73421f512137f2419d%3Blang%5Egbk%3Bt%5E1540800488'},
     {'goods_id': 580666516666, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '三块苹果6s和6拆机电池',
      'goods_desc': '如图所示，手机里面有一块还没拆下来，外面有两块。带标的是在网上买的，全新的iPhone6的电池，不带标的是一块就等6s的电池。因为考虑到iPhone6的电池容量比6s高，我就想把这个全新的iPhone6的电池芯片拆下来换上6s的，结果没有成功，大家可以看图片。至于手机里面这一块，也是在网上买的，全新的充电只有几次，但是装在手机里面感觉耗电很快，所以不想要了，我在网上买了个日本进口的2400毫安的电池。所以这三块电池全都出售。35包邮华中，华南，华东。会折腾的买，不会折腾的就不要买了。\n',
      'goods_price': 35.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/O1CN011xyXeS0V6cpaKTt_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '湖北孝感 安陆市', 'goods_postage': 0, 'goods_appearance': 1,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i4/580/660/580666516666/TB17nculwHqK1RjSZJn8qvNLpla.desc%7Cvar%5Edesc%3Bsign%5E485267339b5fff50cbc492fcd9d0192a%3Blang%5Egbk%3Bt%5E1540800484'},
     {'goods_id': 580666296989, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '全新美版有锁iPhonexs max64',
      'goods_desc': '全新美版有锁iphone XS Max 64G 全新仅激活的机子！！\n移动联通4G直接插卡直接可以用！\n单机零售7050，全套＋200\n顺丰邮费到付，签收确认后返邮费！\n',
      'goods_price': 7050.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/O1CN011lYBT1bXFouwsEg_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '江苏扬州 仪征市', 'goods_postage': 0, 'goods_appearance': 1,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i5/580/660/580666296989/TB1Jt3ClAvoK1RjSZFN8qwxMVla.desc%7Cvar%5Edesc%3Bsign%5E6a264c813e8e6cb2ba143ac3352d1720%3Blang%5Egbk%3Bt%5E1540801406'},
     {'goods_id': 580665960721, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': '华为荣耀V9',
      'goods_desc': '主板坏了，开机没有反应，其它配件正常，二手产品售出不退。\n', 'goods_price': 300.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i2/O1CN011lf3PMjKR9Bu9xS_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '广东阳江 阳春市', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i4/580/660/580665960721/TB1pKQIlxYaK1RjSZFn8qu80pla.desc%7Cvar%5Edesc%3Bsign%5Ea7c88a47e6d2a4c59358bbe21addabe6%3Blang%5Egbk%3Bt%5E1540800419'},
     {'goods_id': 580665216881, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': '苹果七',
      'goods_desc': '苹果7 32g 两网 纯原装 靓  粉色 黑色 价格 1898\n只有五个 先到先挑  6s的价格买个7  优不优势你说了算，打包惊喜价\n', 'goods_price': 1898.0,
      'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/O1CN0124mMQUomu3LVRKu_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 4, 'goods_address': '河北保定 莲池区', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i3/580/660/580665216881/TB1nwImlCrqK1RjSZK98qtyypla.desc%7Cvar%5Edesc%3Bsign%5E189eef0b21bbd66550765499f6445a25%3Blang%5Egbk%3Bt%5E1540800421'},
     {'goods_id': 580624175065, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': 'Mate20',
      'goods_desc': '一定要购买mate20系列的原因：\n01 麒麟980, 六个世界第一, 攀登性能巅峰；\n02 保时捷超跑之&ldquo;四眼车灯&rdquo;，注入Mate 20的美学灵魂；\n03 全新徕卡超广角三摄，引领手机摄影新高度；\n04 超广角摄影大师；\n05 超微距摄影大师；\n06 AI电影大师；\n07 AI压感屏幕指纹，超快超安全；\n08 首次通过全球金融支付标准认证；\n09 3D结构光，玩出新高度；\n10 3D卡路里识别，控制食欲神器；\n11 40W超级快充，再一次刷新安全快充标准；\n12 15W无线超级快充，支持反向充电\n13 首发LTE Cat.21 基带，刷新4G上网速率；\n14 双卡双待双VoLTE，又一座通信高峰；\n15 自研Wi-Fi芯片，Wi-Fi上网前所未有的快；\n16 自研双频GPS芯片，定位精度提升10倍；\n17 首创Nano SD卡标准，手机最小存储卡诞生；\n18 无线投屏，一直被追赶，从未被超越；\n19 Mate 20 X，引入液冷散热技术；\n20 Mate 20 X，首次引入石墨烯散热。  预定电话，18398068122微信同步。\n',
      'goods_price': 200.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/O1CN011cOGLT6z8LX0Zii_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 1, 'goods_address': '四川成都 新都区', 'goods_postage': 0, 'goods_appearance': 4,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i6/580/620/580624175065/TB12H_CkgHqK1RjSZFk8qt.WFla.desc%7Cvar%5Edesc%3Bsign%5E22d555db00037ac7d2cab47cb459021c%3Blang%5Egbk%3Bt%5E1540801409'},
     {'goods_id': 580602961224, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': '华为nova3黑色',
      'goods_desc': '华为nova3黑色今天吵架扔坏了，不开机，屏幕弯了，没碎。拆后盖拍了两张图，主板有磕碰芯片掉了。有兴趣自己看有人要没，要的出价，价高者拿，当尸体配件卖，售出不退，2999才买了一个月\n',
      'goods_price': 99.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i2/O1CN011y5rzHiDJnzyPtq_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '贵州贵阳 云岩区', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i4/580/600/580602961224/TB1xbw.lbvpK1RjSZPi8qvmwXla.desc%7Cvar%5Edesc%3Bsign%5Ee0d52f515c6cfd90a014cf89048b97d7%3Blang%5Egbk%3Bt%5E1540800440'},
     {'goods_id': 580559904680, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '全新iphoneX256G全网通', 'goods_desc': '全新美版iphoneX，空间灰，256GB。全网通，朋友送的，闲置转让。\n', 'goods_price': 7800.0,
      'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/O1CN011vSMaoKiQckGJix_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 1, 'goods_address': '北京北京 朝阳区', 'goods_postage': 0, 'goods_appearance': 4,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i6/580/551/580559904680/TB1Y9oHlhjaK1RjSZKz8qtVwXla.desc%7Cvar%5Edesc%3Bsign%5E1b91e5805389402a7ee4421ed6d9230f%3Blang%5Egbk%3Bt%5E1540801405'},
     {'goods_id': 580544674755, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '苹果X 美版黑色64g 原封机 iPhoneXs',
      'goods_desc': '苹果X 美版64G 全原封 Ip67防水防尘 \n充新99新 不严可以封包卖 完美靓充\nS版 解好锁 插卡三网4g 面容正常 \n无id锁 随意刷机升级 无任何问题！\n需要拍下即可发货 默认顺丰 邮自理！\n关于售后：撕标不退不保 不撕标签保修一个月！\n长期供应有锁X Xs Xsmax 8代8P 7代7P 全系列\n拿货欢迎关注 三年老店 诚寻合作！\n',
      'goods_price': 4650.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i4/O1CN011uY1sLMb1PPnlqS_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 1, 'goods_address': '广东深圳 福田区', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i5/580/540/580544674755/TB1m1KhkxTpK1RjSZR08qvEwXla.desc%7Cvar%5Edesc%3Bsign%5E6a6f52f14dc7ec0bc694fe210002fa1d%3Blang%5Egbk%3Bt%5E1540800430'},
     {'goods_id': 580479146836, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': 'iphone 6SP IPHONE 6SP 16 苹果',
      'goods_desc': '苹果6splus 16g 6sp16 国行银色，成色如图。 三网4g，无id，无越狱，指纹灵敏，自用机，所有功能一切正常相机有点小毛病，有时候会抖，介意的自己拿去换个相机也就一百多，没花柳，任意刷机，二手商品不退不换，可接水果刀 本交易支持自提、当面交易、邮寄\n',
      'goods_price': 1100.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i2/O1CN011dhKRuvSzjkT6dZ_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '广东清远 英德市', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i8/580/471/580479146836/TB1nLW_kkvoK1RjSZPf8qtPKFla.desc%7Cvar%5Edesc%3Bsign%5Ed8b4e7fd59c2f66c3267a3a4cd8cccf1%3Blang%5Egbk%3Bt%5E1540801419'},
     {'goods_id': 580445151842, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '女孩自用 iPhone 8plus金色 国行全网通4G',
      'goods_desc': '女孩自用iPhone 8plus金色 全网通4G 64G 转让女生自用iphone 8plus金色全网通4G 国行 转让女孩自用 iphone 8plus 金色 全网通4G\n 手机内存64G 功能都正常使用 原装配件齐全 \n指纹解锁灵敏 没有磕碰划伤。有想要的联系我\n诚心出售。可以小刀。支持当面交易！\n',
      'goods_price': 2400.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/O1CN011bozqaMHYFb2dEr_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '山东青岛 李沧区', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i2/580/440/580445151842/TB12SeAjQvoK1RjSZPf8qtPKFla.desc%7Cvar%5Edesc%3Bsign%5E10ee1e876a663c14964b4606929ac43b%3Blang%5Egbk%3Bt%5E1540801417'},
     {'goods_id': 580425806992, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '苹果7p黑128g全网通国航',
      'goods_desc': '苹果7p黑色128g全网通国航，无拆无修刚用一年。刚过保了。成色也很好，手机不卡。没有见过水。没有暗病可以小刀。同城可以面交。\n', 'goods_price': 1800.0,
      'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/O1CN011rnC8rLmvPt5MDG_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '江苏苏州 吴中区', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i3/580/420/580425806992/TB17tTZj3HqK1RjSZFE8qwGMXla.desc%7Cvar%5Edesc%3Bsign%5E67151056e9b51117851a2900b20519c8%3Blang%5Egbk%3Bt%5E1540800467'},
     {'goods_id': 580410195169, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '苹果iphone xs max 256g全新', 'goods_desc': '对象送我一个，他不知道我自己也买了一个，多了\n', 'goods_price': 10500.0,
      'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/O1CN011tbrZez5f4gr3Sm_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '江苏南京 雨花台区', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i6/580/410/580410195169/TB18Rx4jSzqK1RjSZPc8qvTepla.desc%7Cvar%5Edesc%3Bsign%5E1eeee1038333b6e0a821e8d559871e8f%3Blang%5Egbk%3Bt%5E1540800531'},
     {'goods_id': 580406494275, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': 'iphone 7 plus', 'goods_desc': '128g黑色港版无拆无修无暗病，机身左上角一点磕碰，可以在图中看到。不刀，诚意出。\n',
      'goods_price': 3100.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i2/O1CN011ks31ni1sgWb6Ed_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '江西南昌 南昌县', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i7/580/400/580406494275/TB1oxcxlyrpK1RjSZFh8qtSdXla.desc%7Cvar%5Edesc%3Bsign%5E4a24f3fa7923fbfc37a7a9faacd0ee4e%3Blang%5Egbk%3Bt%5E1540800755'},
     {'goods_id': 580388031127, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': 'iPhone 6s',
      'goods_desc': '型号：iPhone 6s 16g 三网4g\n成色：底部氧化严重，周围轻微掉漆，指纹摄像头屏幕原装正常，电池健康。\n亮点：iOS 10，不卡顿，比我自己的iPhone X流畅\n',
      'goods_price': 1200.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i2/O1CN011hfjX0qEb6Pc4gV_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '贵州遵义 播州区', 'goods_postage': 0, 'goods_appearance': 1,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i7/580/381/580388031127/TB1ymnojAvoK1RjSZFN8qwxMVla.desc%7Cvar%5Edesc%3Bsign%5E98e807c722e59c799c7a6fc76909ab37%3Blang%5Egbk%3Bt%5E1540800527'},
     {'goods_id': 580269109012, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
      'goods_title': '苹果X 美版64g iPhoneX 无面容 国屏',
      'goods_desc': '苹果X 美版黑/白64G 全原封 仅换国屏 \n纯无锁两网 插卡移动联通4g 无面容解锁\n无id锁 随意刷机升级 无任何问题！\n换的是oled软屏 色温色差全部正常 触摸完美，\n需要拍下备注颜色即可发货 无面容国屏 无锁！\n售后：撕标不退不保 不撕标签保修一个月！\n长期供应X系列 有锁卡贴 国屏 无锁 无面容机子，\n需要拿货欢迎关注 诚寻合作商户！\n',
      'goods_price': 3299.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/O1CN0121uekarhLGLol6e_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '广东深圳 福田区', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i2/580/261/580269109012/TB1I3o1lmrqK1RjSZK98qtyypla.desc%7Cvar%5Edesc%3Bsign%5E0bd4cc283ed18e9afda533cee93adf06%3Blang%5Egbk%3Bt%5E1540800418'},
     {'goods_id': 580132510004, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29), 'goods_title': 'iphone',
      'goods_desc': '转手原因:闲置在家，自己用了两年，电池不久前换新的，其他全部完好，指纹可用，除了换电池没有其他维修，4+12g内存，移动国行版，诚信买卖，要的可以私我，支持自提，同城交易，邮寄，不砍价，谢谢！\n',
      'goods_price': 360.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/O1CN011qWsPcANsOZCCyW_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 4, 'goods_address': '福建厦门 思明区', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i6/580/130/580132510004/TB1p003jOrpK1RjSZFh8qtSdXla.desc%7Cvar%5Edesc%3Bsign%5Ee1abd888f4b8685dca88746b971df81a%3Blang%5Egbk%3Bt%5E1540801419'},
     {'goods_id': 578066415968, 'user_id': 1, 'release_date': datetime.date(2018, 10, 28),
      'goods_title': '转让自用iPhone 8plus 金色 全网通4G 64G',
      'goods_desc': '女孩自用iPhone 8plus金色 全网通4G 64G 转让女生自用iphone 8plus金色全网通4G 国行 转让女孩自用 iphone 8plus 金色 全网通4G\n 手机内存64G 功能都正常使用 原装配件齐全 \n指纹解锁灵敏 没有磕碰划伤。有想要的联系我\n诚心出售。可以小刀。支持当面交易！\n',
      'goods_price': 2400.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/TB2391Kb7voK1RjSZFDXXXY3pXa_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 1, 'goods_address': '山东青岛 李沧区', 'goods_postage': 0, 'goods_appearance': 1,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i6/571/060/578066415968/TB1_7HChpzqK1RjSZFC8qvbxVla.desc%7Cvar%5Edesc%3Bsign%5E64f8d5823f489abc81ba4172d2d66d64%3Blang%5Egbk%3Bt%5E1540801417'},
     {'goods_id': 578012428512, 'user_id': 1, 'release_date': datetime.date(2018, 10, 28), 'goods_title': '苹果6 10系统',
      'goods_desc': '  64 \n\n10系统\n', 'goods_price': 999.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/O1CN011Dmf2f2malyrX9k_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 2, 'goods_address': '福建福州 台江区', 'goods_postage': 0, 'goods_appearance': 3,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i8/571/010/578012428512/TB1FUBrexnaK1RjSZFB8qwW7Vla.desc%7Cvar%5Edesc%3Bsign%5E1a8a91715968bd79baca6705fd5c3875%3Blang%5Egbk%3Bt%5E1540800477'},
     {'goods_id': 577745995551, 'user_id': 1, 'release_date': datetime.date(2018, 10, 28),
      'goods_title': 'iPhoneX 64G深空灰黑色免卡贴有锁苹果X64G',
      'goods_desc': '成色如图\n原装屏幕更换成第三方屏幕了，其它全原装，所有功能正常，面容ID灵敏\n已设置好免卡贴模式，收到后移动联通4G插卡即用，完美稳定和国行一样，可以升级系统。刷机还原了需要配合卡贴重新激活，送备用卡贴和激活教程。\n底部贴有撕毁无效保修标签，可保15天非人为故障，没有标签不保修退换，所以请15天内不要撕掉标签，谢谢配合。\n裸机无配件，邮费顺丰到付，一分钱一分货，感谢您的浏览，欢迎关注。\n',
      'goods_price': 3750.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i4/TB2Dj.OaAvoK1RjSZFDXXXY3pXa_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 1, 'goods_address': '福建泉州 丰泽区', 'goods_postage': 0, 'goods_appearance': 1,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i8/570/740/577745995551/TB1ZugEcVzqK1RjSZFo8qvfcXla.desc%7Cvar%5Edesc%3Bsign%5E57526628d57a1fff547b8b8b65b0a976%3Blang%5Egbk%3Bt%5E1540800490'},
     {'goods_id': 577728295519, 'user_id': 1, 'release_date': datetime.date(2018, 10, 28),
      'goods_title': '苹果7 128 9新二手', 'goods_desc': '东乡当面交易。送数据线\n', 'goods_price': 2388.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i4/TB2CVrBawHqK1RjSZJnXXbNLpXa_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '江西抚州 东乡区', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i8/570/721/577728295519/TB16KfCawHqK1RjSZFk8qt.WFla.desc%7Cvar%5Edesc%3Bsign%5Ea8ae8c6732bd124aee11711f00383540%3Blang%5Egbk%3Bt%5E1540800448'},
     {'goods_id': 577334251061, 'user_id': 1, 'release_date': datetime.date(2018, 10, 27), 'goods_title': '苹果x',
      'goods_desc': '自己用的，买了没多久 ，非常新256GB没有任何划伤，保护的很好\n', 'goods_price': 6500.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/TB2d6psxlsmBKNjSZFFXXcT9VXa_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '北京北京 朝阳区', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i5/570/330/577334251061/TB18vx2ea6qK1RjSZFm8qt0PFla.desc%7Cvar%5Edesc%3Bsign%5Edeeff9f7531b69f65f1f6bbde43d833a%3Blang%5Egbk%3Bt%5E1540801407'},
     {'goods_id': 576869456918, 'user_id': 1, 'release_date': datetime.date(2018, 10, 27),
      'goods_title': 'iPhone X 64G银白色免卡贴靓机有锁X64G',
      'goods_desc': '这台出了，有别的现货咨询客服\n原装屏幕更换成第三方屏幕了，其它全原装，所有功能正常，面容ID灵敏\n已设置好免卡贴模式，收到后移动联通4G插卡即用，完美稳定和国行一样，可以升级系统。不刷机和还原就是无锁机，刷机还原了需要用卡贴重新激活，送备用卡贴和激活教程。\n裸机无配件，邮费顺丰到付，一分钱一分货，感谢您的浏览，欢迎关注。\n',
      'goods_price': 3750.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i2/TB2wAVmwVkoBKNjSZFkXXb4tFXa_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '福建泉州 丰泽区', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i7/570/861/576869456918/TB1OpZEcYPpK1RjSZFF8qu5Ppla.desc%7Cvar%5Edesc%3Bsign%5E25d0617f6841835753d8f6d6a58df255%3Blang%5Egbk%3Bt%5E1540800487'},
     {'goods_id': 576455649956, 'user_id': 1, 'release_date': datetime.date(2018, 10, 27),
      'goods_title': '苹果7代 32G 黑白金粉 全网通4g 无锁机器',
      'goods_desc': '苹果7代 32G 黑白金粉 iPhone7  全网通 苹果7代 \n型号：iphone7（无锁，插卡直接用）\n内存：32 \n支持网络：移动联通电信4g\n屏幕尺寸：4.7\n手机类型：美版三网通\n功能：指纹灵敏 功能一切正常\n外壳：9.5.新 靓机\n手机随意升级还原刷机，指纹灵敏所有功能一切正常。\n有意可以私聊！\n',
      'goods_price': 1850.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i1/TB2qL3duDmWBKNjSZFBXXXxUFXa_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '广东深圳 福田区', 'goods_postage': 0, 'goods_appearance': 1,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i8/570/450/576455649956/TB1ES6cbMDqK1RjSZSy8quxEVla.desc%7Cvar%5Edesc%3Bsign%5Ee929d4f6b88c613c76ea1267a5b1d5c9%3Blang%5Egbk%3Bt%5E1540800532'},
     {'goods_id': 576346305555, 'user_id': 1, 'release_date': datetime.date(2018, 10, 27),
      'goods_title': '苹果/iphone6代全网通64G V版  工作机',
      'goods_desc': ' 苹果/iphone6代全网通64G 美版v版无指纹，三网通移动2g.联通电信4g.插卡即用\n工作室 备用机首选\n本交易支持自提、当面交易、邮寄\n',
      'goods_price': 699.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/TB2Fq8qtWAoBKNjSZSyXXaHAVXa_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 0, 'goods_address': '广东深圳 福田区', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i7/570/340/576346305555/TB1NsjebG6qK1RjSZFm8qt0PFla.desc%7Cvar%5Edesc%3Bsign%5Eb03a6ac2bca0f0f9e81c54ca0919b386%3Blang%5Egbk%3Bt%5E1540800536'},
     {'goods_id': 0, 'user_id': 1, 'release_date': datetime.date(2018, 10, 26),
      'goods_title': '苹果8/苹果iPhone8Plus/X/xs/max美版有锁',
      'goods_desc': '本店诚信经营，以信誉及完美机器换取您对本店满意，以高芝麻信用度及完美评价为依托，为您网购保驾护航！ \n产品简介：\n本款为苹果8/苹果iPhone8Plus/美版有锁机，需要配合卡贴使用，目前完美漏洞已出，完美解锁后和纯无锁机器一样，支持三网4G，信号显示4G，号码簿不用加86，来电可正常显示备注！发货前我们会调试好卡贴，收到货插卡即用，使用简单，操作方便，容易上手！\n\n产品说明：苹果8/X系列支持无线充电，支持NFC，支持3D压力屏，钢化玻璃后盖，手感极佳，带给你不一样的体验！\n\n成色说明：本店主做全新机、99新靓机，绝大多数机器边框都是不存在磕碰刮花这些，后盖轻微刮花，屏幕细微刮花，成色都比较新，激活日期大部分都是在2-6个月之间，电池寿命都处于正常范围，可放心购买！\n\n关于验机：本店所有产品发货前都会经过严格的检测和调试，均通过PP助手验机和爱思助手验机，收到货可自行查询，亦可以拿到专卖店验货，信誉担保，真正做到让顾客买的放心，用的舒心！\n\n关于发货：晚上9点以前下单，最快当天安排发货，9点以后的订单，于第二天晚上发出，本店全部发顺丰到付，顺丰到付，顺丰到付！\n',
      'goods_price': 3599.0, 'goods_category_id': 1,
      'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/TB2OCJXk_mWBKNjSZFBXXXxUFXa_!!0-fleamarket.jpg_728x728.jpg',
      'goods_browse_count': 30, 'goods_address': '河南郑州 中原区', 'goods_postage': 0, 'goods_appearance': 2,
      'goods_state': '0',
      'desc_link': 'https://osdsc.alicdn.com/i8/570/300/573300524974/TB11qKfiYvpK1RjSZPi8qvmwXla.desc%7Cvar%5Edesc%3Bsign%5E7a3aa592bc10b7b6b4d1c6cd96e9bc08%3Blang%5Egbk%3Bt%5E1540801405'}]
[{'order_id': 7, 'release_user_id': 1, 'buy_user_id': 2, 'order_date': '2018-11-05', 'order_goods_id': 578573944299,
  'order_mark': '0', 'state': 0, 'goods_id': 578573944299, 'user_id': 1, 'release_date': datetime.date(2018, 10, 29),
  'goods_title': '紫米新款电源20000毫安',
  'goods_desc': ' 大品牌紫米电源，比小米华为电源便宜好用，大容量双向快充，隐形数显！要的私聊！清仓大甩卖，量大价优！！！本身价格就开的很低了，刀客请绕行，几块钱砍来砍去浪费大家时间！优先同城自提。不出新疆西藏等极偏远地区！京东原装货，一大箱库存，我这只要112，包邮！！！\n',
  'goods_price': 112.0, 'goods_category_id': 1,
  'goods_imgurl': 'https://img.alicdn.com/bao/uploaded/i3/O1CN011RjpDIL3UjuSWL6_!!0-fleamarket.jpg_728x728.jpg',
  'goods_browse_count': 1, 'goods_address': '江苏苏州 虎丘区', 'goods_postage': 0, 'goods_appearance': 4, 'goods_state': '1',
  'desc_link': 'https://osdsc.alicdn.com/i5/571/570/578573944299/TB1DD.ckbrpK1RjSZTE8qwWAVla.desc%7Cvar%5Edesc%3Bsign%5E07f6a0f49816a92bbb98d4a44ec9eb3e%3Blang%5Egbk%3Bt%5E1540800477'}]
# sms = redis.Redis(host="47.100.200.132", port=6379, db=5)
# a=sms.get(17326197619)
# print(a)
cur.execute("select user_name,user_state from t_user where user_name=%s", ["jqlove", ])  # 全表搜索，待建立索引
user_login = cur.fetchone()
print(user_login)
