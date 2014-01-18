#coding=utf-8
import ConfigParser
import urllib
import urllib2
import json
import datetime
import time
from ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import DataService
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

CFG_FILE = 'conf/conf.ini'
CFG_SESSION = 'tweibo'

config = ConfigParser.ConfigParser()
with open(CFG_FILE,'r') as cfg:
	config.readfp(cfg)

cfg = lambda name:config.get(CFG_SESSION,name)

class Tweibo:

	def __init__(self):
		self.base_url = 'http://open.t.qq.com/api/search/t'
		self.hasnext = 0
		self.params = dict(
			format='json',
			contenttype=4,
			sorttype=4,
			msgtype=0,
			searchtype=0,
			needdup=1,
			oauth_version='2.a',
			access_token= cfg('access_token'),
			oauth_consumer_key=cfg('oauth_consumer_key'),
			openid=cfg('openid'),
			)
		self.content = None
	
	def search(self,query):
		self.params.update(query)
		
		headers = {
			'ContentType':'application/x-www-form-urlencoded',
			'Accept':'text/%s' % (self.params['format']),
			'User-Agent':'Chrome: mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/27.0.1453.94',
			}
		body = urllib.urlencode(self.params)
		req = urllib2.Request( self.base_url + '?' + body, None, headers)
		f=urllib2.urlopen(req)
		self.content = f.read()

class ThriftClient:

	def __init__(self):
		self.host = cfg('thrift_host')
		self.port = 9090
		self.socket = TSocket.TSocket(self.host,self.port)
		self.transport = TTransport.TFramedTransport(self.socket)
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = DataService.Client(self.protocol)
		self.msg = list()


	def generate(self,str_json):
		ret = json.loads(str_json)
		data = ret.get('data',{})
		if data is None:
			print ret
		else:
			self.hasnext = str(data.get('hasnext',None))
			items = data.get('info',[])
			for item in items:
				pics = item.get('pic',None)
				image_url = None
				if pics is not None:
					for image in pics['info']:
						image_url = ''.join(image['url']) + '/460.jpg'
						break
					if image_url is not None:
						content = str(item['text'] + image_url).encode('utf-8')
						message = Message(title='tweibo',content=content)
						self.msg.append(message)



	def send(self):
		if len(self.msg) > 0:
			for message in self.msg:
				print message.content
				print '\n*****************************\n'
			self.transport.open()
			print self.client.pushMsg(self.msg)
			self.transport.close()
			self.msg = list()
	

starttime = datetime.datetime.now() - datetime.timedelta(hours =1 )
starttime = int(time.mktime(starttime.timetuple()))
startpage = 1
timestamp = int(time.time())
weibo = Tweibo()
thrift_client = ThriftClient()

while True:
	print startpage
	query = dict(
			keyword='美食',
			page=startpage,
			pagesize=30,
			starttime=starttime,
			endtime=timestamp,)
	weibo.search(query)
	thrift_client.generate(weibo.content)
	thrift_client.send()

	startpage = startpage + 1
	if weibo.hasnext == '2' or weibo.hasnext == '0':
		print 'weibo.hasnext %s ' % (weibo.hasnext)
		break
	break
