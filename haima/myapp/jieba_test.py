import jieba
import pymysql
import redis

r1 = redis.Redis(host='47.100.200.132', port=6379, db=1)
r = redis.Redis(host='47.100.200.132', port=6379)
conn = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='item', charset='utf8')
cur = conn.cursor()

# sql = "select goods_id,goods_title from goods_test"
# cur.execute(sql)
# goods = cur.fetchall()
# for i, j in goods:
#     data = jieba.cut(j)
#     for word in data:
#         key = word
#         r.sadd(key, i)
# val_list = []
# bval_list = list(r.smembers("和"))
# for i in bval_list:
#     i = int(i.decode('utf-8'))
#     val_list.append(i)
# print(val_list)
ls = []
a = r.keys()
for i in a:
    i = i.decode('utf-8')
    r1.sadd(64, i)

