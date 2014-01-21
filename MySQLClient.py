#coding=utf-8
from Cfg import *
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class MySQLClient:

	def __init__(self):
		host = cfg('mysql_host')
		user = cfg('mysql_user')
		passwd = cfg('mysql_passwd')
		db_name = cfg('mysql_dbname')
		charset = cfg('mysql_charset')
		self.conn = MySQLdb.connect(host,user,passwd,db_name,charset=charset)
		self.cursor = self.conn.cursor()

	def insert(self,create_time,content_list):
		for content in content_list:
			try:
				sql_str = 'insert signature_message (title,content,create_time,reason,sort_id) values ("%s","%s","%s","%s","%d") ' % ('tweibo',content,create_time,None,1)
				self.cursor.execute(sql_str)
			except Exception, e:
				print e

	def last_record(self):
		return self.cursor.lastrowid

	def __exit__(self,*kw):
		self.conn.commit()

	def __enter__(self):
		pass

	def rollback(self):
		self.conn.rollback()

	def close(self):
		self.cursor.close()
		self.conn.commit()
		self.conn.close()
