import pandas as pd

<<<<<<< HEAD
# df = pd.read_csv("C:\\Users\\Administrator\\Desktop\\phone_model.csv")
=======
df = pd.read_csv("C:\\phone_model.csv")
>>>>>>> 1026a71912a8ff0b3533af031d7b99e5a3bcbc3b


def Phone_model(brand, model):
    a = list(df['0']).index(brand)
    b = list(df.loc[a]).index(model)
    return a + 1, b


# brand, model = Phone_model('苹果', '6')
# print(brand, model)


# C:\\Users\\Administrator\\Desktop\\phone_model.csv