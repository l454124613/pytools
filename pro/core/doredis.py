# -*- coding:utf-8 -*-
# Author:lixuecheng

import redis
from pro.core.logger import log, logger
from pro.core.baseClass import base_class
from pro.util.parse_msg import p_to_uri
import chardet

class DoRedis(base_class):
    @log
    def __init__(self, ip,  port=6379,password=None,need_res=True):
        try:
            self.ip = ip
            self.port = port
            
            self.db = redis.Redis(host=ip, port=port,password=password)
            self.string = self.ip + ':' + str(
                self.port) 
            self.status = 0
            self.need_res=need_res
            logger.info('redis连接成功，-----' + self.string)
        except Exception as e:
            self.db = None
            self.string = str(e)
            self.status = 1
            raise Exception('数据库连接失败：' + str(e))

    def __str__(self):
        try:
            return 'redis_' + self.string
        except Exception as e:

            # logger.warn('mysql字符串转化失败，' + str(e))
            return 'redis,无字符串初始化，获取是日志获取中发生,' + str(e)
            # raise Exception('mysql字符串转化失败，' + str(e))
    
    def get(self,name,encoding='utf8'):
        # TODO
        ret = self.db.get(name)
        print(ret)
        ret=ret.lstrip(b'\xac\xed\x00\x05sr\x00\x13')  #.lstrip(b'\xac\xed\x00\x05sr\x00\x13')
        
        return ret.decode(encoding)
        
    def set(self,k,v):
        self.db.set(k,v)
        
    def append(self,k,v):
        self.db.append(k,v)
        
    def list_keys(self):
        return self.db.keys()
    
        

    

    def close(self):
        try:

            self.db.close()
        except:
            pass
        self.status = 2
        # logger.info('数据库断开连接')






    def __del__(self):
        self.close()
        
    

# aa=DoRedis('172.16.9.131',password='AAAaaa123')
# print(aa.list_keys())
# print(aa.get('15800707121:noRepetition'))

# print(aa.get('15800707121:userInfo'))

# try:
#     aa = DoMysql('172.16.9.28', 'root', 'a111111', 'gtobusinessdb')
#     aa.run('UPDATE am_resign set modified_by=\'d15\' where  resign_id =1')
#     # raise Exception('')
#     aa.commit()
# except:
#     aa.rollback()
# aa = DoMysql('172.16.9.28', 'root', 'a111111', 'gtobusinessdb')
# a=aa.run('SELECT * from am_resign ')
# print(a)

