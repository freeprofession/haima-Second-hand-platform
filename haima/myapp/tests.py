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
a=get_eva.hgetall('110')
print(a)
