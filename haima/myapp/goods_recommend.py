import numpy as np
import math
import pymysql
import redis
import re
from collections import Counter
import json
import time
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect


def goods_recommend(requset):
    user_id = requset.POST.get('user_id')
    r = redis.Redis(host="47.100.200.132", port=6379, db=10)
    conn = pymysql.connect(host='47.100.200.132', user='user', password='123456', database='haima', charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    uid_score_bid = []
    keys_dict = {}
    keys = r.keys()
    for key in keys:
        key = key.decode('utf-8')
        keys_dict[key] = r.llen(key)
        key = re.findall(r"\d+\.?\d*", key)[0]
        user_list = r.lrange(key, 0, -1)
        Count = dict(Counter(user_list))
        for users_id in Count.keys():
            count = Count[users_id]
            users_id = users_id.decode('utf-8')
            cur.execute("select collection_user_id from t_user_collection where collection_goods_id=%s", [key, ])
            result = cur.fetchall()
            if users_id in result:
                count = count * 2
            data = users_id + ',' + str(count) + ',' + key
            uid_score_bid.append(data)
    keys_dict = sorted(keys_dict.items(), key=lambda x: x[1], reverse=True)[0:5]

    # print(uid_score_bid)

    # uid_score_bid = ['A,1,a', 'A,1,b', 'A,1,d', 'B,1,b', 'B,1,c', 'B,1,e', 'C,1,c', 'C,1,d', 'D,1,b', 'D,1,c', 'D,1,d',
    #                  'E,1,a', 'E,1,d']

    class ItemBasedCF:
        def __init__(self, train_file):
            self.train_file = train_file
            self.readData()

        def readData(self):
            # 读取文件，并生成数据集（用户，兴趣程度，物品）
            self.train = dict()
            for line in self.train_file:
                user, score, item = line.strip().split(",")
                self.train.setdefault(user, {})
                self.train[user][item] = int(float(score))
            # print(self.train)  # 输出数据集

        def ItemSimilarity(self):
            C = dict()  # 物品-物品的共现矩阵
            N = dict()  # 物品被多少个不同用户浏览
            for user, items in self.train.items():
                for i in items.keys():
                    N.setdefault(i, 0)
                    N[i] += 1  # 物品i出现一次就计数加一
                    C.setdefault(i, {})
                    for j in items.keys():
                        if i == j:
                            continue
                        C[i].setdefault(j, 0)
                        C[i][j] += 1 / math.log(1 + len(items) * 1.0)

            # print('N:', N)
            # print('C:', C)

            # 计算相似度矩阵
            self.W = dict()
            self.W_max = dict()  # 记录每一列的最大值
            for i, related_items in C.items():
                self.W.setdefault(i, {})
                for j, cij in related_items.items():
                    self.W_max.setdefault(j, 0.0)
                    self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))  # jaccard系数
                    if self.W[i][j] > self.W_max[j]:
                        self.W_max[j] = self.W[i][j]  # 记录第j列的最大值，按列归一化
            # print('W:', self.W)
            for i, related_items in C.items():
                for j, cij in related_items.items():
                    self.W[i][j] = self.W[i][j] / self.W_max[j]
            # print('W_max:', self.W_max)
            # for k, v in self.W.items():
            #     print(k + ':' + str(v))
            return self.W

        # 给用户user推荐前N个最感兴趣的物品
        def Recommend(self, user):
            rank = dict()  # 记录user的推荐物品（没有历史行为的物品）和兴趣程度
            action_item = self.train[user]  # 用户user浏览的物品和兴趣评分r_ui
            for item, score in action_item.items():
                for j, wj in sorted(self.W[item].items(), key=lambda x: x[1], reverse=True)[
                             0:10]:  # 使用与物品item最相似的10个物品进行计算
                    if j in action_item.keys():  # 如果物品j已经浏览过，则不进行推荐
                        continue
                    rank.setdefault(j, 0)
                    rank[j] += score * wj  # 如果物品j没有浏览过，则累计物品j与item的相似度*兴趣评分，作为user对物品j的兴趣程度
            return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:10])

    # 声明一个ItemBased推荐的对象
    goods_list = []
    if user_id == 'visitor':
        res = list(keys_dict)[0:5]
    else:
        Item = ItemBasedCF(uid_score_bid)
        Item.ItemSimilarity()
        recommedDic = Item.Recommend(user_id)  # 计算给用户A的推荐列表
        res = list(recommedDic.items())
    if len(res) < 5:
        for i in range(5 - len(res)):
            res.append((keys_dict[i][0], 1))
    for k, v in res:
        cur.execute("select goods_title,goods_id,goods_imgurl,goods_price from t_goods where goods_id=%s", [k, ])
        goods_list.append(cur.fetchone())
    a = ''
    c = 0
    for item in goods_list:
        if item == None:
            continue
        else:
            rr = """<ul>
                                    <li>
                                        <a href="/goods_detail/?goods={0}"><img src="{1}"class="goods_pic"></a>
                                        <h4><a href="/goods_detail/?goods={2}"title="{3}">{4}</a></h4>
                                        <div class="prize">¥ {5}</div>
                                    </li>
                            </ul>"""
            b = rr.format(item['goods_id'], item['goods_imgurl'], item['goods_id'], item['goods_title'],
                          item['goods_title'], item['goods_price'])
            a += b
            c += 1
            if c == 5:
                break
    return HttpResponse(json.dumps({'rr': a}))

# a = [0, 1, 1, 1, 0, 0]
# b = [1, 1, 1, 1, 1, 1]
#
# v1 = np.array(a)
# v2 = np.array(b)
#
# d = np.linalg.norm(v1 - v2)
# print(d)
# print(goods_recommend(1))
