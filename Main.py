#coding=utf-8
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from Tweibo import Tweibo
from JsonGenerator import generate
from MySQLClient import MySQLClient
from ThriftClient import ThriftClient

starttime = datetime.datetime.now() - datetime.timedelta(hours =1 )
starttime = int(time.mktime(starttime.timetuple()))
startpage = 1
timestamp = int(time.time())
weibo = Tweibo()


def thrift_send(content):
	thrift_client = ThriftClient()
	thrift_client.send(content)

def mysql_save(create_time,content):
	mysql_client = MySQLClient()
	with mysql_client:
		mysql_client.insert(create_time,content)

keys=['美食','小吃']

for key in keys:
	while True:
		print startpage
		print key
		query = dict(
				keyword=key,
				page=startpage,
				pagesize=30,
				starttime=starttime,
				endtime=timestamp,)
		weibo.search(query)
		result = generate(weibo.content)
		create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		#mysql_save(create_time,result[0])
		thrift_send(result[0])
		if result[1] == '2' or result[1] == '0':
			print 'hasnext %s ' % (result[1])
			break
		startpage = startpage + 1
		time.sleep(2)