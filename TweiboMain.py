#coding=utf-8
import datetime
import time
import TweiboParser
import tweibo
import ThriftClient

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

starttime = datetime.datetime.now() - datetime.timedelta(hours =1 )
starttime = int(time.mktime(starttime.timetuple()))
startpage = 1
timestamp = int(time.time())

tweibo = tweibo.Tweibo()		#tencent weibo

keys=['美食','小吃']
thrift_client = ThriftClient.ThriftClient()

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
		tweibo.search(query)
		result = TweiboParser.parse(tweibo.content)
		create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		thrift_client.send(result[0])
		if result[1] == '2' or result[1] == '0':
			print 'hasnext %s ' % (result[1])
			break
		startpage = startpage + 1
		time.sleep(3)
