# -*- coding:utf-8 -*-
# Author:lixuecheng

import pymongo
from pro.core.baseClass import base_class
from dateutil import parser
from pro.core.logger import log, logger

class DoMongo(base_class):
    def __init__(self, ips, user, password, dbname,need_res=True):
        try:
            self.ip = ips
            self.user = user
            self.password = password
            self.dbname = dbname
            
            self.string = 'mongodb://'+self.user+':'+self.password+'@'+self.ip+'/'
            self.client =  pymongo.MongoClient(self.string)
            self.db=self.client[self.dbname]
     
            self.status = 0
            self.need_res=need_res
            logger.info('mongo连接成功，-----' + self.string)
        except Exception as e:
            self.db = None
            self.cursor = False
            self.e = e
            self.string = str(e)
            self.status = 1
            self.need_res=need_res
            raise Exception('数据库连接失败：' + str(e))

    def __str__(self):
        try:
            return 'mongo_' + self.string
        except Exception as e:

            return 'mongo,无字符串初始化，获取是日志获取中发生,' + str(e)

    def insert(self, site,data):
        try:
            if self.status == 2:
                self.client =  pymongo.MongoClient(self.string)
                self.db=self.client[self.dbname]
                self.status = 0
                self.e = ''
        except Exception as e:
            self.e = e
            raise Exception('数据库链接失败，' + e.__str__())


        mydict=self.db[site]
        x=mydict.insert_one(data)
    
    def select(self, site,value=None):
        try:
            if self.status == 2:
                self.client =  pymongo.MongoClient(self.string)
                self.db=self.client[self.dbname]
                self.status = 0
                self.e = ''
        except Exception as e:
            self.e = e
            raise Exception('数据库链接失败，' + e.__str__())


        mydict=self.db[site]
        if value is None:
            x=mydict.find({})
        else:
            x=mydict.find(value)
        return x
        

    def close(self):
        try:
            self.db.close()
            self.client.close()
        except:
            pass
        self.status = 2
        # print('数据库断开连接')
    def __del__(self):
        self.close()



# dm=DoMongo('172.16.9.139:20000,172.16.9.140:20000,172.16.9.141:20000','ciicsh','AAAaaa1234','ciic_salary')


# a=dm.select('test',{'yyyy':1234567890})

# for i in a:
#     print(i)
# print(a.collection)
# print(a.comment)
# print(a.count)
# print(a.cursor_id)

    


