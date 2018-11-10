# from sklearn.datasets import  load_boston
# from sklearn.linear_model import  LinearRegression, SGDRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# def Linear():
#     '''
#     线性回归算法预测房子价格
#     :return:
#     '''
#     #获取数据
#     lb = load_boston()
#     #分割数据集到训练集和测试集
#     x_train, x_test,y_train, y_test = train_test_split(lb.data, lb.target, test_size= 0.25)
#     #进行标准化处理,目标值处理
#     std_x = StandardScaler()
#     x_train = std_x.fit_transform(x_train)
#     x_test = std_x.transform(x_test)
#     #目标值
#     std_y = StandardScaler()
#     y_train = std_y.fit_transform(y_train.reshape(-1,1))
#     y_test = std_y.transform(y_test.reshape(-1,1))
#     #正规方程求解方式预测结果
#     lineRg = LinearRegression()
#     lineRg.fit(x_train, y_train)
#     print(lineRg.coef_)  #回归系数，即权重
#     #测试集:x_test ,预测的价格 y_predict
#     y_predict = std_y.inverse_transform(lineRg.predict(x_test))
#     print("测试集里每个房子的预测价格:",y_predict)
# if __name__ == "__main__":
#     Linear()

