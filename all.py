from elasticsearch import Elasticsearch
from elasticsearch import helpers
from tkitTranslator import Translator
es = Elasticsearch('127.0.0.1:9200')

index_v="scrapy_search-2020-11"
doc_type_v="items"

query={"query" : {"match_all" : {}}}

scanResp= helpers.scan(client= es, query=query, scroll= "10m", index= index_v , doc_type=doc_type_v , timeout="10m")

for resp in scanResp:
    qid = resp['_id']
    print(qid)
    # print(resp)
    t=Translator()
    print(resp['_source']['title'])
    print(t.render(resp['_source']['title']))
    print(resp['_source']['content'])
    print(t.render(resp['_source']['content']))
