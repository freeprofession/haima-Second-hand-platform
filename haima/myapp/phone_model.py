import pandas as pd

df = pd.read_csv("C:\\phone_model.csv")
<<<<<<< HEAD


=======
>>>>>>> d1841869d6fbac3aeda718188489ee8db3c4bc35
def Phone_model(brand, model):
    a = list(df['0']).index(brand)
    b = list(df.loc[a]).index(model)
    return a + 1, b


# brand, model = Phone_model('苹果', '6')
# print(brand, model)


