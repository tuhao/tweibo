#coding=utf-8
import ConfigParser
import urllib
import sys
import urllib2
import json
import datetime
import time
reload(sys)
sys.setdefaultencoding("utf-8")

CFG_FILE = 'conf/conf.ini'
CFG_SESSION = 'tweibo'

config = ConfigParser.ConfigParser()
with open(CFG_FILE,'r') as cfg:
	config.readfp(cfg)

cfg = lambda name:config.get(CFG_SESSION,name)

class Tweibo:

	def __init__(self,timestamp):
		self.base_url = 'http://open.t.qq.com/api/search/t'
		self.hasnext = 0
		self.timestamp = timestamp
		self.stop = False
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
		self.generate(f.read())
	
	def generate(self,content):
		ret = json.loads(content)
		data = ret.get('data',{})
		self.hasnext = int(data.get('hasnext',None))
		items = data.get('info',[])
		with open('food.txt','w') as f:
			for item in items:
				if int(item['timestamp']) >= self.timestamp:
					print item['text'].encode('utf-8')
					f.write(item['text'].encode('utf-8') + '\n')
					for pic in item['pic']['info']:
						print ''.join(pic['url']) + '/460.jpg'
						f.write(''.join(pic['url']) + '/460.jpg' + '\n')
				else:
					self.stop = True
					break

starttime = datetime.datetime.now() - datetime.timedelta(hours=1 )
starttime = int(time.mktime(starttime.timetuple()))
weibo = Tweibo(starttime)

while True:
	timestamp = int(time.time())
	startpage = 0
	query = dict(
			keyword='美食',
			page=startpage,
			pagesize=30,
			starttime=starttime,
			endtime=timestamp,)
	weibo.search(query)
	startpage = startpage + 1
	if weibo.hasnext < 1 or weibo.stop:
		print 'weibo.hasnext %d ,weibo.stop %s' % (weibo.hasnext,weibo.stop)
		break
	time.sleep(3)
