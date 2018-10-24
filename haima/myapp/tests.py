import pymysql
import redis
from django.test import TestCase
import json

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
a=tt.format('ddddd', 'jqlopv', 'wwweq')
print(a)
