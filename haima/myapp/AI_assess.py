# 模型训练，使用scikit-learn里面的LinearRegression类来实现线性回归算法
# #数据导入

from sklearn.datasets import load_boston  # step1:数据导入
from sklearn.model_selection import train_test_split  # step2:数据集划分
from sklearn.linear_model import LinearRegression  # step3:数据模型训练
from sklearn.preprocessing import PolynomialFeatures  # 使用二项式优化
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
import time

boston = load_boston()
X = boston.data
y = boston.target  # (1)数据集分成两份，其中一份是训练集，一份是测试集
# for i in range(100):
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
# print(boston.feature_names)  # 查看特征 #


# 接下来训练模型，获得参数的值
def polynomial_model(degree):
    polynomial_features = PolynomialFeatures(degree=degree, include_bias=False)
    linear_regression = LinearRegression(normalize=True)
    pipeline = Pipeline([("polynomial_features", polynomial_features), ("linear_regreesion", linear_regression)])
    return pipeline


def assess_price(lst):
    model = polynomial_model(2)
    model.fit(X_train, y_train)
    price = model.predict([lst])
    print(len(y_test))
    return price

#     model = polynomial_model(2)
#     model.fit(X_train, y_train)
#     start = time.clock()
#     train_score = model.score(X_train, y_train)
#     cv_score = model.score(X_test, y_test)
#     print('用时:{0:.6f};训练分数:{1:0.6f}; 测验分数:{2:0.6f}'.format(time.clock() - start, train_score, cv_score),i)
# print(len(y_test))
# for i in range(len(y_train)):
#     print(model.predict([X_train[i]]),[y_train[i]])
# test_data= [2, 5, 6, 64, 1, 0, 0, 0, 0]
# print(model.predict([test_data]))

# a = model.predict(X_test)
# price = {}
# for i in range(len(a)):
#     a[i] = round(a[i],2)
#     price[y_test[i]] = a[i]
# print(price)

# print(model.predict(test_data))
