from aip import AipImageSearch
import json
APP_ID = '14640597'
API_KEY = '6pT1zsnXTY7Ywkx5OuOZjEFg'
SECRET_KEY = 'gIG4esr46GPbTTVOLGcbfDnYtiLxyISh'

client = AipImageSearch(APP_ID, API_KEY, SECRET_KEY)

# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()


# image = get_file_content('example.jpg')
#
# """ 调用商品检索—入库, 图片参数为本地图片 """
# client.productAdd(image);
#
# """ 如果有可选参数 """
# options = {}
# options["brief"] = "{\"name\":\"手机\", \"id\":\"666\"}"
# options["class_id1"] = 1
# options["class_id2"] = 1
#
# """ 带参数调用商品检索—入库, 图片参数为本地图片 """
# client.productAdd(image, options)

url = "http://pgwecu7z4.bkt.clouddn.com/FscJv6t1uO8IZR9Bvpj09kBm68UX"

""" 调用商品检索—入库, 图片参数为远程url图片 """
options = {}
options["brief"] = "{\"url\":\"" + url + "\"}"
# print(client.productAddUrl(url, options))
js = client.productSearchUrl(url)['result'][0]['brief']
js_img = json.loads(js)
print(client.productSearchUrl(url)['result'][0]['brief'])
