# encoding:utf-8
#获取关键词库https://github.com/summanlp/textrank
from summa import keywords
from summa import summarizer

import os 
import time
import datetime
#html转化为markdown
from markdownify import markdownify
from urllib.parse import quote
import tkitJson
import yaml
import pymongo
client = pymongo.MongoClient("192.168.192.173", 27017)
DB = client.hugo

import  hashlib



def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录,创建目录操作函数
        '''
        os.mkdir(path)与os.makedirs(path)的区别是,当父目录不存在的时候os.mkdir(path)不会创建，os.makedirs(path)则会创建父目录
        '''
        #此处路径最好使用utf-8解码，否则在磁盘中可能会出现乱码的情况
        os.makedirs(path) 
        # print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print (path+' 目录已存在')
        return False





# 重置内容增加这个参数
task=2



#重置
# for i,item in enumerate(DB.content_pet.find({})):
#     print(i)
#     item["version"]=0
#     DB.content_pet.update({'_id':item["_id"]},{'$set':item},True)

for i,item in enumerate(DB.content_pet.find({"version":{ "$lt":int(task) }})):

    if item['title'].get('data') and item['content'].get('data'):

        curr_time = datetime.datetime.now()
        # print(curr_time)
        time_str = curr_time.strftime("%Y-%m-%d")


        # title="哈哈这个是牛逼的调诐" 
        title=markdownify(item['title'].get('data'))
        # main_text=markdownify(item['content'].get('data'))
        main_text= item['content'].get('data')


        kws=keywords.keywords(title+" "+main_text,words=5)
        summary=summarizer.summarize(main_text, words=50, split=True)
        kws=kws.split("\n")[:3]
        print(kws)
        print(summary)
        print("##"*10)

        subtitle=''
        tags=kws
        bigimg=[{"src": "/img/path.jpg", "des": "Path"}]
        # main_text="<h1>Hello, World!</h1>"
        # main_text = markdownify(main_text)

        # print(main_text)
        time_str="2020-12-01"
        
        # url_title = md5(title)
        url_title=str(item["_id"])
        path_name=url_title[:2]
        mkdir(os.path.join(os.getcwd(),'content/post/',path_name))
        # name=f'{time_str}-{url_title[:50]}.md'
        name=f'{url_title}.md'
        file_path=os.path.join(os.getcwd(),'content/post/',path_name,name)
        f1 = open(file_path,'w+')
        # title=title.replace("...",'')
        top_json={
            "title":title,
            "date":time_str,
            "tags":kws,
            "summary":summary,
            "slug":url_title+"" #这个是设置url
        }
        top=yaml.dump(top_json)
        # print(top)
# subtitle: {subtitle}
        head=f"""---
{top}---

{main_text}
        """

        # print(head)
        # 写入文件
        f1.write(head)
        #关闭文件
        f1.close()

        # 更新任务进度
        item["version"]=int(task)
        DB.content_pet.update({'_id':item["_id"]},{'$set':item},True)
