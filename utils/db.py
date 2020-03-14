'''
数据库操作
'''
import os
import re
import pymysql
import logging

def parse_db_url(db_url):
    try:
        db_type,user,password,host,port,db = re.split(r'://|:|@|/',db_url)
    except ValueError:
        raise ValueError(f'db_url:{db_url}-格式不正确，应为完整的 mysql://root:password@localhost:3306/test 形式')
    if 'mysql' not in db_type:
        raise TypeError('暂时只支持mysql数据库')

    db_conf = dict(host=host,port=int(port),db=db,user=user,password=password)
    return db_conf 

class DB:
    def __init__(self,db_conf=None):
        if db_conf is None:
            db_url = os.getenv('DB_URI')
            print(db_url,type(db_url))
            if db_url is None:
                raise ValueError('DB_URL环境变量未配置, 格式为DB_CONF=mysql://root:password@localhost:3306/test')
            db_conf = parse_db_url(os.getenv('DB_URI'))
        db_conf.setdefault('charset','utf8')
        self.conn = pymysql.connect(**db_conf,autocommit=True)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

    #执行sql
    def query(self,sql):
        logging.debug(f'查询sql: {sql}')
        self.cur.execute(sql)
        result = self.cur.fetchall()
        logging.debug(f'查询数据：{result}')
        return result

    def change_db(self,sql):
        logging.debug(f'执行sql:{sql}')
        self.cur.execute(sql)

    def close(self):
        self.cur.close()
        self.conn.close()
        


if __name__ == '__main__':
    db = DB()
