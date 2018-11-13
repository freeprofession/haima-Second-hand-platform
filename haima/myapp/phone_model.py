import pandas as pd

<<<<<<< HEAD
df = pd.read_csv("myapp/phone_model.csv", encoding='utf-8')

=======
# df = pd.read_csv("myapp/phone_model.csv", encoding='utf-8')
# df = pd.read_csv("C:\\phone_model.csv")
>>>>>>> 089b6140d99308d47e8445e919f5fa3bd3c8e67e
def Phone_model(brand, model):
    a = list(df['0']).index(brand)
    b = list(df.loc[a]).index(model)
    return a + 1, b

# brand, model = Phone_model('苹果', '6')
# print(brand, model)
