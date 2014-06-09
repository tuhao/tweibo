#coding=utf-8
from HTMLParser import HTMLParser
import sys,os
import re
reload(sys)
sys.setdefaultencoding("utf-8")

def enum(**enums):
	return type('Enum',(),enums)

PROCESS = enum(INIT = -1,START = 0,ON = 1,END = 2)

TAG_S_CONTENT = '<content>'
TAG_S_IMG = '<img>'
TAG_E_CONTENT = '</content>'
TAG_E_IMG = '</img>'
WEIBO_REGEX = re.compile(TAG_S_CONTENT + r'.*?' + TAG_E_IMG)
CONTENT_REGEX = re.compile(TAG_S_CONTENT + r'.*?' + TAG_E_CONTENT)
IMG_REGEX = re.compile(TAG_S_IMG + r'.*?' +TAG_E_IMG)
THUMBIMG_REGEX = 'thumbnail'
BIGIMG_REGEX = 'bmiddle'

class DataParser(HTMLParser):

	def __init__(self):
		self.links = []
		self.data = ''
		self.img = None
		self.process = PROCESS.INIT
		HTMLParser.__init__(self)

	def handle_starttag(self,tag,attrs):

		if tag == 'p':
			for variable,value in attrs:
				if variable == 'node-type':
					if value == 'feed_list_content':
						self.process = PROCESS.START

		
		if tag == 'img':
			for variable,value in attrs:
				if variable == 'class' and value == 'bigcursor':
					self.img = True
					continue
				if self.img:
					if variable == 'src':
						self.links.append(value)
						self.data += TAG_S_IMG
						self.data += value
						self.data += TAG_E_IMG
						self.img = None
						break

	def handle_data(self,data):
		if self.process == PROCESS.START:
			self.data += TAG_S_CONTENT
			self.process = PROCESS.ON
		elif self.process == PROCESS.ON:
			self.data += data



	def handle_endtag(self,tag):
		if tag == 'p':
			if self.process == PROCESS.ON:
				self.data += TAG_E_CONTENT
			self.process = PROCESS.END


class WeiboParser:

	def __init__(self,data):
		self.data = data
		self.result = []

	def parse(self):
		for item in WEIBO_REGEX.findall(self.data.replace('\n', '')):
			weibos = []
			imgs = []
			for line in CONTENT_REGEX.findall(item):
				weibos.append(line)
			for line in IMG_REGEX.findall(item):
				imgs.append(line.replace(THUMBIMG_REGEX,BIGIMG_REGEX))
			weibo = (weibos[-1] + imgs[0]).replace(TAG_S_IMG,'').replace(TAG_E_IMG,'').replace(TAG_S_CONTENT,'').replace(TAG_E_CONTENT,'')
			self.result.append(weibo)


if __name__ ==  '__main__':
	contentPath = os.path.dirname(__file__) + '/search.html'
	with open(contentPath,'r') as f:
		content = f.read() 
		dp = DataParser()
		dp.feed(content)
		dp.close()
		parser = WeiboParser(dp.data)
		parser.parse()
		for weibo in parser.result:
			print weibo