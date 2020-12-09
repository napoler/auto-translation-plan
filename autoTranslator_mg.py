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
from .fun import md5
#模型下载自https://www.kaggle.com/terrychanorg/bertcleartitlemodel
TClear =Bert_clear_title.Marker(model_path="/mnt/data/dev/model/Bert_clear_title/model/")
TClear.load_model()



client = pymongo.MongoClient("localhost", 27017)
DB = client.hugo




es = Elasticsearch('127.0.0.1:9200')
index_v="terry-index"
index_v="scrapy_search-2020-11"
doc_type_v="items"
query={"query" : {"match_all" : {}}} 
scanResp= helpers.scan(client= es, query=query, scroll= "10m", index= index_v , doc_type=doc_type_v , timeout="10m")
# Tjson=tkitJson.Json("data/data.json")
items=[]
for i,resp in enumerate(scanResp):
    end_time=datetime.datetime.now()
    start_time=datetime.datetime.now() + datetime.timedelta(days=-150) # 当前时间减去3分钟      
    time_post=random_date(start=start_time,end=end_time) 
    qid = resp['_id']
    #尝试兼容旧的出重复
    md5id=md5(resp['_source']['title']+resp['_source']['content'])   
    #检查id是否存在，存在则内容已经翻译过跳过。
    if DB.content_pet.find_one({"_id":qid}) or DB.content_pet.find_one({"_id":md5id}):
        continue
    #跳过垃圾内容
    if DB.content_pet_bad.find_one({"_id":qid}):
        continue
 
    print("\n"*2,i)

    
    # print(resp)
    # print(resp['_source']['title'])
    one=TClear.pre(resp['_source']['title'])

    # print(TClear.get_mark_data(one[0]))
    if len(TClear.get_mark_data(one[0]))==0:
        #判别内容质量提取失败，加入到乎略内容列表
        items.append(resp['_source']['title'])
        data=[{"_id":qid,"version":0,"original":resp}]
        DB.content_pet_bad.update({'_id':qid},{'$set':data[0]},True)
    else:
        try:
            T = Translator()
            print(resp['_source']['title'])
            title=T.render(TClear.get_mark_data(one[0])["title"][0])
            content=T.render(resp['_source']['content'])
            print(title)
            print(content)
            if content.get("data") and title.get("data"):
                data=[{"title":title,"content":content,"_id":qid,"version":0,"type":"new","pubdate":time_post,"original":resp}]
                #添加数据
                # Tjson.save(data)
                DB.content_pet.update({'_id':qid},{'$set':data[0]},True)

        except:
            print("翻译失败")
            pass

print("召回失败的：",len(items))      
print(items)

