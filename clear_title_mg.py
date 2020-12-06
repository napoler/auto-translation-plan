# -*-coding:utf-8-*-
import os

import pymongo
client = pymongo.MongoClient("localhost", 27017)
DB = client.gpt2Write

# 引入安装的库
import Bert_clear_title
#模型下载自https://www.kaggle.com/terrychanorg/bertcleartitlemodel
TClear =Bert_clear_title.Marker(model_path="/mnt/data/dev/model/Bert_clear_title/model/")
TClear.load_model()

n=0
# 以写的方式打开文件，如果文件不存在，就会自动创建
f= open("data/new/title.txt", 'w')
for i, it in  enumerate(DB.content_pet.find({})):

    
    # kw=it['entity']+it['value']
    # if len(it['data'])>1:
    # if "|" in it["title"] or "-" in it["title"] or "_" in it["title"] or "|" in it["title"] or "~" in it["title"] :
    # print("-"*20)
    one=TClear.pre(it['title'])
    # print(TClear.get_mark_data(one[0]))
    if len(TClear.get_mark_data(one[0]))==0:
        print("-"*20)
        # items.append(resp['_source']['title'])
        print(it["title"])
        f.writelines(it['title'])
        f.writelines("\n")
        f.writelines("\n")
        n=n+1
        print(n,i)

f.close()
