import pandas as pd


df = pd.read_csv("myapp/phone_model.csv", encoding='utf-8')


def Phone_model(brand, model):
    a = list(df['0']).index(brand)
    b = list(df.loc[a]).index(model)
    return a + 1, b

# brand, model = Phone_model('苹果', '6')
# print(brand, model)
