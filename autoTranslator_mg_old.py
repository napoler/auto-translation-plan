# -*-coding:utf-8-*-
import os
import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from tkitTranslator import Translator
# import tkitJson
import pymongo
# 引入安装的库
import Bert_clear_title
from albert_pytorch import classify
"""
本脚本用于处理之前的内容


"""








#加载判断质量
tclass = classify(model_name_or_path="/mnt/data/dev/model/classification-text-good-bad/model",num_labels=2,device="cpu") 

#模型下载自https://www.kaggle.com/terrychanorg/bertcleartitlemodel
TClear =Bert_clear_title.Marker(model_path="/mnt/data/dev/model/Bert_clear_title/model/")
TClear.load_model()



client = pymongo.MongoClient("localhost", 27017)
DB = client.hugo
OldDB=client.gpt2Write
items=[]
for i,resp in enumerate(OldDB.content_pet.find({})):
    # print(resp)
    # continue
    # if i >100:
    #     break
    end_time=datetime.datetime.now()
    start_time=datetime.datetime.now() + datetime.timedelta(days=-150) # 当前时间减去3分钟      
    time_post=random_date(start=start_time,end=end_time) 
    qid = resp['_id']
    
    #检查id是否存在，存在则内容已经翻译过跳过。
    if DB.content_pet.find_one({"_id":qid}):
        continue
    #跳过垃圾内容
    if DB.content_pet_bad.find_one({"_id":qid}):
        continue
    print("\n"*2,i)

    p=tclass.pre(resp['content'][:300])
    print("内容质量（0,1）：",p)
    if int(p)==0:
        #低质量
        data=[{"_id":qid,"version":0,"original":resp}]
        DB.content_pet_bad.update_one({'_id':qid},{'$set':data[0]},True)
        continue
    
    # continue
    #清理标题
    one=TClear.pre(resp['title'])

    # print(TClear.get_mark_data(one[0]))
    if len(TClear.get_mark_data(one[0]))==0:
        #判别内容质量提取失败，加入到乎略内容列表
        items.append(resp['title'])
        data=[{"_id":qid,"version":0,"original":resp}]
        DB.content_pet_bad.update_one({'_id':qid},{'$set':data[0]},True)
    else:
        try:
            T = Translator()
            print(resp['title'])
            print(resp['_id'])
            title=T.render(TClear.get_mark_data(one[0])["title"][0])
            content=T.render(resp['content'])
            print(title)
            print(content)
            if content.get("data") and title.get("data"):
                data=[{"title":title,"content":content,"_id":qid,"version":0,"type":"old","pubdate":time_post,"original":resp}]
                #添加数据
                # Tjson.save(data)
                DB.content_pet.update_one({'_id':qid},{'$set':data[0]},True)

        except:
            print("翻译失败")
            pass

print("召回失败的：",len(items))      
print(items)

