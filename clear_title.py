# -*-coding:utf-8-*-
import os

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from tkitTranslator import Translator

# 引入安装的库
import Bert_clear_title
#模型下载自https://www.kaggle.com/terrychanorg/bertcleartitlemodel
TClear =Bert_clear_title.Marker(model_path="/mnt/data/dev/model/Bert_clear_title/model/")
TClear.load_model()


es = Elasticsearch('127.0.0.1:9200')
index_v="terry-index"
index_v="scrapy_search-2020-11"
doc_type_v="items"
query={"query" : {"match_all" : {}}} 
scanResp= helpers.scan(client= es, query=query, scroll= "10m", index= index_v , doc_type=doc_type_v , timeout="10m")

items=[]
for i,resp in enumerate( scanResp):
    print("\n"*2)
    qid = resp['_id']
    # print(resp)
    # print(resp['_source']['title'])
    one=TClear.pre(resp['_source']['title'])

    # print(TClear.get_mark_data(one[0]))
    if len(TClear.get_mark_data(one[0]))==0:
        items.append(resp['_source']['title'])
    else:
        T = Translator()
        print(resp['_source']['title'])
        print(T.render(TClear.get_mark_data(one[0])["title"][0]))
        print(T.render(resp['_source']['content']))      

print("召回失败的：",len(items))      
print(items)

