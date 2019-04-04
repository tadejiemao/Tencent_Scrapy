# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
from Tencent.items import TencentItem
from scrapy.conf import settings


# 写json文件
class TencentPipeline(object):
    def __init__(self):
        self.filename = open('tencent.json','w')
        
    def process_item(self,item,spider):
        text = json.dumps(dict(item),ensure_ascii=False) + ',\n'
        self.filename.write(text)
        return item
    
    def close_spider(self,spider):
        self.filename.close()

# 写数据库
class MysqlPipeline(object):
    
    def process_item(self,item,spider):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        password = settings['MYSQL_PASSWORD']
        database = settings['MYSQL_DATABASE']
        c = settings['MYSQL_CHARSET']
        port = settings['MYSQL_PORT']
        
        con=pymysql.connect(host=host,user=user,passwd=password,db=database,charset=c,port=port,use_unicode=True)
        
        cue=con.cursor()
        print("mysql connect succes")
        
        try:
            cue.execute("insert into positions(positionname, positionlink, positiontype, peoplenum, worklocation, publishtime) VALUES (%s, %s, %s, %s, %s, %s)",[item['positionname'],item['positionlink'],item['positiontype'],item['peoplenum'],item['worklocation'],item['publishtime']])
        except Exception as e:
            print('Insert Error',e)
            con.rollback()
        else:
            con.commit()
        con.close()        
        return item    
            