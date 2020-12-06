# -*-coding:utf-8-*-
import os
import Bert_clear_title
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from tkitTranslator import Translator

#模型下载自https://www.kaggle.com/terrychanorg/bertcleartitlemodel
Demo =Bert_clear_title.Marker(model_path="/mnt/data/dev/model/Bert_clear_title/model/")
Demo.load_model()

es = Elasticsearch('127.0.0.1:9200')

index_v="terry-index"
# index_v="scrapy_search-2020-11"
doc_type_v="items"

query={"query" : {"match_all" : {}}} 

scanResp= helpers.scan(client= es, query=query, scroll= "10m", index= index_v , doc_type=doc_type_v , timeout="10m")



# 以写的方式打开文件，如果文件不存在，就会自动创建
# f= open("data/title.txt", 'w')

for i,resp in enumerate( scanResp):
#     qid = resp['_id']
#     print(resp)
# print(111)
    print(resp['_source']['title'])
#     f.writelines(resp['_source']['title'])
#     f.writelines("\n")
#     f.writelines("\n")
#     if i%10==0 and i !=0:
#         name=f"data/title{i}.txt"
#         f= open(name, 'w')
# f.close()
