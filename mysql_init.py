#!/usr/bin/python3.6.4¬
import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
					 passwd='public',
					 db='Lianjia')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

sql = """CREATE TABLE ErshoufangBasic(
       houseid char(20) NOT NULL,
       region  char(20) NOT NULL,
       house_type char(15) NOT NULL,
       area char(10) NOT NULL,
       total_price char(16) NOT NULL,
       unit_price char(10),
       orientation char(10),
       design char(6),
       follow char(32) NOT NULL,
       watch char(32) NOT NULL,
       querytime char(16) NOT NULL,
	   PRIMARY KEY(houseid))"""

cursor.execute(sql)

db.close()
