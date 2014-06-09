#coding=utf-8
import sys
import weiboParser
import weibo
import time
import ThriftClient

reload(sys)
sys.setdefaultencoding='utf-8'

keys=['美食','小吃']
instance = weibo.Weibo()			#sina weibo
thrift_client = ThriftClient.ThriftClient()

for key in keys:
	instance.search(key)
	if instance.result:
		dp = weiboParser.DataParser()
		dp.feed(instance.result)
		dp.close()
		parser = weiboParser.WeiboParser(dp.data)
		parser.parse()
		thrift_client.send(parser.result)
		time.sleep(3)