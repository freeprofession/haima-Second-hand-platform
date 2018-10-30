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
tt = [{'second_message_id': 1, 'parent_user_id': '6', 'second_desc': '爱你哦', 'second_goods_id': '1',
       'second_date': '2018-10-26 11:05:07', 'child_user_id': '1', 'to_rid': '1', 'user_id': 1, 'user_name': 'jqlove',
       'user_password': '123456',
       'user_imgurl': 'http://img.crawler.qq.com/lolwebvideo/20170802165439/c91a5a13e7bff101a4a75aecc191b075/0',
       'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': '2018-10-22', 'user_money': 100.0,
       'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
      {'second_message_id': 2, 'parent_user_id': '1', 'second_desc': '爱我的哇啊切 ', 'second_goods_id': '1',
       'second_date': '2018-10-26 11:16:11', 'child_user_id': '1', 'to_rid': '1', 'user_id': 1, 'user_name': 'jqlove',
       'user_password': '123456',
       'user_imgurl': 'http://img.crawler.qq.com/lolwebvideo/20170802165439/c91a5a13e7bff101a4a75aecc191b075/0',
       'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': '2018-10-22', 'user_money': 100.0,
       'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
      {'second_message_id': 3, 'parent_user_id': '2', 'second_desc': '挨打的而且', 'second_goods_id': '1',
       'second_date': '2018-10-26 11:16:19', 'child_user_id': '1', 'to_rid': '2', 'user_id': 1, 'user_name': 'jqlove',
       'user_password': '123456',
       'user_imgurl': 'http://img.crawler.qq.com/lolwebvideo/20170802165439/c91a5a13e7bff101a4a75aecc191b075/0',
       'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': '2018-10-22', 'user_money': 100.0,
       'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
      {'second_message_id': 4, 'parent_user_id': '1', 'second_desc': '回复jqlovejqlovejqlovejqlove:nmsl',
       'second_goods_id': '1', 'second_date': '2018-10-26 11:17:02', 'child_user_id': '2', 'to_rid': '1', 'user_id': 2,
       'user_name': 'clearlove', 'user_password': '123456',
       'user_imgurl': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540203476459&di=4e89eef785b6e15ddc965e80e15fcdfb&imgtype=0&src=http%3A%2F%2Fwww.gamemei.com%2Fbackground%2Fuploads%2Fallimg%2F20160525%2F1464153091927021.jpg',
       'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': ' 2018-10-22', 'user_money': 100.0,
       'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
      {'second_message_id': 5, 'parent_user_id': '2', 'second_desc': '?W?Das\nD  as a ', 'second_goods_id': '1',
       'second_date': '2018-10-26 11:17:31', 'child_user_id': '2', 'to_rid': '2', 'user_id': 2,
       'user_name': 'clearlove', 'user_password': '123456',
       'user_imgurl': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540203476459&di=4e89eef785b6e15ddc965e80e15fcdfb&imgtype=0&src=http%3A%2F%2Fwww.gamemei.com%2Fbackground%2Fuploads%2Fallimg%2F20160525%2F1464153091927021.jpg',
       'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': ' 2018-10-22', 'user_money': 100.0,
       'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
      {'second_message_id': 6, 'parent_user_id': '3', 'second_desc': 'ada qrqqerqtq', 'second_goods_id': '1',
       'second_date': '2018-10-26 11:17:36', 'child_user_id': '2', 'to_rid': '3', 'user_id': 2,
       'user_name': 'clearlove', 'user_password': '123456',
       'user_imgurl': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540203476459&di=4e89eef785b6e15ddc965e80e15fcdfb&imgtype=0&src=http%3A%2F%2Fwww.gamemei.com%2Fbackground%2Fuploads%2Fallimg%2F20160525%2F1464153091927021.jpg',
       'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': ' 2018-10-22', 'user_money': 100.0,
       'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'},
      {'second_message_id': 7, 'parent_user_id': '1', 'second_desc': 'sxada  dasdas ', 'second_goods_id': '1',
       'second_date': '2018-10-26 11:18:05', 'child_user_id': '2', 'to_rid': '1', 'user_id': 2,
       'user_name': 'clearlove', 'user_password': '123456',
       'user_imgurl': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540203476459&di=4e89eef785b6e15ddc965e80e15fcdfb&imgtype=0&src=http%3A%2F%2Fwww.gamemei.com%2Fbackground%2Fuploads%2Fallimg%2F20160525%2F1464153091927021.jpg',
       'user_phone': '17779137404', 'user_nickname': '0', 'user_startdate': ' 2018-10-22', 'user_money': 100.0,
       'user_state': 0, 'user_credit': 0, 'user_address': '灵石路'}]

cur.execute("select * from t_second_message right join t_user on child_user_id=user_id where  second_goods_id=%s",
            [1, ])
b = cur.fetchall()
c_comment_dict = {}
for d in b:
    id = d.get('second_message_id')
    c_comment_dict[id] = d
lst = []
for j in c_comment_dict:
    lst.append(c_comment_dict[j])
print(c_comment_dict)

