# -*- coding:utf-8 -*-
# Author:lixuecheng

import pymysql
from pro.core.logger import log, logger
from pro.core.baseClass import base_class
from pro.util.parse_msg import p_to_uri


class DoMysql(base_class):
    @log
    def __init__(self, ip, user, password, dbname, port=3306,need_res=True):
        try:
            self.ip = ip
            self.port = port
            self.user = user
            self.password = password
            self.dbname = dbname
            self.db = pymysql.connect(host=self.ip, port=int(self.port), user=self.user, password=self.password,
                                      database=self.dbname,
                                      charset='utf8',
                                      autocommit=False)
            self.string = self.ip + ':' + str(
                self.port) + ',user=' + self.user + ',password=' + self.password + ',database=' + self.dbname
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            self.status = 0
            self.need_res=need_res
            logger.info('mysql连接成功，-----' + self.string)
        except Exception as e:
            self.db = None
            self.cursor = False
            self.e = e
            self.string = str(e)
            self.status = 1
            raise Exception('数据库连接失败：' + str(e))

    def __str__(self):
        try:
            return 'mysql_' + self.string
        except Exception as e:

            # logger.warn('mysql字符串转化失败，' + str(e))
            return 'mysql,无字符串初始化，获取是日志获取中发生,' + str(e)
            # raise Exception('mysql字符串转化失败，' + str(e))

    '''
    sql,sql语句
    name,运行目的
    gg,全局变量
    '''

    @log
    def run(self, sql):
        try:
            if self.status == 2:
                self.db = pymysql.connect(host=self.ip, port=int(self.port), user=self.user, password=self.password,
                                          database=self.dbname,
                                          charset='utf8',
                                          autocommit=False)
                self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
                self.status = 0
                self.e = ''
                self.res=None
        except Exception as e:
            self.e = e
            raise Exception('数据库链接失败，' + p_to_uri(e.__str__()))

        if self.cursor:
            try:
                self.sql=sql
                self.cursor.execute(sql)
                self.res = self.cursor.fetchall()
              
                return self.cursor.rowcount, self.res
            except Exception as e:
                self.e = e
                raise Exception(sql+',执行sql失败，' + p_to_uri(e.__str__()))

        else:
            raise Exception('数据库链接失败')

    def close(self):
        try:
            self.cursor.close()
            self.db.close()
        except:
            pass
        self.status = 2
        # logger.info('数据库断开连接')

    def commit(self):
        logger.info('执行数据库提交')
        self.db.commit()
        self.close()

    def rollback(self):
        logger.info('执行数据库回滚,' + str(p_to_uri(self.e)))
        self.db.rollback()
        self.close()

    @log
    def check(self, fn):
        fn(self.res)
    def __del__(self):
        self.close()
        
    



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

