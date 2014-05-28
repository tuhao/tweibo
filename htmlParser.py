#coding=utf-8
from HTMLParser import HTMLParser
import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")


class DataParser(HTMLParser):

	def __init__(self):
		self.links = []
		HTMLParser.__init__(self)

	def handle_starttag(self,tag,attrs):
		if tag == 'a':
			for (variable,value) in attrs:
				if variable == 'href':
					self.links.append(value)

	def handle_data(self,data):
		print data


contentPath = os.path.dirname(__file__) + '/search.html'
with open(contentPath,'r') as f:
	content = f.read() 
	dp = DataParser()
	dp.feed(content)
	dp.close()
	print dp.links