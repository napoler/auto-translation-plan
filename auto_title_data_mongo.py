# -*-coding:utf-8-*-
import os

import pymongo
client = pymongo.MongoClient("localhost", 27017)
DB = client.gpt2Write

# 以写的方式打开文件，如果文件不存在，就会自动创建
f= open("data/pet/title.txt", 'w')
for i, it in  enumerate(DB.content_pet.find({})):

    print("-"*20)
    # kw=it['entity']+it['value']
    # if len(it['data'])>1:
    print(it["title"])
    f.writelines(it['title'])
    f.writelines("\n")
    f.writelines("\n")
    if i%50==0 and i !=0:
        name=f"data/pet/title{i}.txt"
        f= open(name, 'w')
f.close()

# for i,resp in enumerate( scanResp):
#     qid = resp['_id']
#     print(resp)
# print(111)
#     print(resp['_source']['title'])
#     f.writelines(resp['_source']['title'])
#     f.writelines("\n")
#     f.writelines("\n")
#     if i%10==0 and i !=0:
#         name=f"data/title{i}.txt"
#         f= open(name, 'w')
# f.close()
