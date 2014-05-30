#coding=utf-8
import urllib
import sys
import urllib2

reload(sys)
sys.setdefaultencoding='utf-8'

class Weibo:

	def __init__(self):
		self.key = 'q'
		self.url = 'http://s.weibo.com/wb/'
		self.params = dict()
		self.content = None

	def search(self,keyword):
		self.params.update({self.key:keyword})
		query = urllib.urlencode(self.params)
		self.params[self.key] = query[len(self.key) + 1:].encode('utf-8')
		query = urllib.urlencode(self.params)
		self.url += query[len(self.key) + 1:]
		print self.url
		headers = {'Referer':'http://weibo.com',
					'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
		req = urllib2.Request(self.url, None, headers)
		self.content = urllib2.urlopen(req).read()
