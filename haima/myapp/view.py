from django.shortcuts import HttpResponse, render
import pymysql
import redis

r = redis.Redis(host='47.100.200.132', port='6379')
con = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='item', charset='utf8')
cursor = con.cursor(pymysql.cursors.DictCursor)


def homepage(request):
    sql = "select * from goods_test limit 0,10"
    cursor.execute(sql)
    goods_list = cursor.fetchall()
    for goods in goods_list:
        goods['img_url'] = r.srandmember(goods['goods_id'], 1)[0].decode('utf-8')
    print(goods_list)
    return render(request, 'homepage.html',{'goods_list':goods_list})


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def user_center_info(request):
    return render(request, 'user_center_info.html')
