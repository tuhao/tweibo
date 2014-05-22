#coding=utf-8
import urllib
import sys
import urllib2

reload(sys)
sys.setdefaultencoding='utf-8'

key = 'q'
params = {}
params[key]= u'美食'.encode('utf-8')
query =  urllib.urlencode(params)
params[key] = query[len(key) + 1:].encode('utf-8')
query = urllib.urlencode(params)


url = 'http://s.weibo.com/wb/' + query[len(key) + 1:]
print url
headers = {'Referer':'http://weibo.com',
			'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
req = urllib2.Request(url, None, headers)
content = urllib2.urlopen(req).read()
print content