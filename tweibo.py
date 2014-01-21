#coding=utf-8

import urllib
import urllib2
from Cfg import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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