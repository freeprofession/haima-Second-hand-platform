import pandas as pd

<<<<<<< HEAD
df = pd.read_csv("C:\\phone_model.csv")

=======
# df = pd.read_csv("C:\\phone_model.csv")
>>>>>>> 001e5c22ba82a3fc8c1b35bc17a7a9c605d9524c
def Phone_model(brand, model):
    a = list(df['0']).index(brand)
    b = list(df.loc[a]).index(model)
    return a + 1, b


# brand, model = Phone_model('苹果', '6')
# print(brand, model)


