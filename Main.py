#coding=utf-8
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from tweibo import Tweibo
from JsonGenerator import generate
from MySQLClient import MySQLClient
from ThriftClient import ThriftClient

starttime = datetime.datetime.now() - datetime.timedelta(minutes =15 )
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

while True:
	print startpage
	query = dict(
			keyword='美食',
			page=startpage,
			pagesize=2,
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