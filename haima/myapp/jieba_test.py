import jieba
import pymysql
import redis

r = redis.Redis(host='47.100.200.132', port=6379, db=1)
conn = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='item', charset='utf8')
cur = conn.cursor()

sql = "select goods_id,goods_title from goods_test"
cur.execute(sql)
goods = cur.fetchall()
for i, j in goods:
    data = jieba.cut(j)
    for word in data:
        key = word
        r.sadd(key, i)
