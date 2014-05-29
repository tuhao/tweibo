#coding=utf-8
from HTMLParser import HTMLParser
import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")

def enum(**enums):
	return type('Enum',(),enums)

PROCESS = enum(INIT = -1,START = 0,ON = 1,END = 2)

class DataParser(HTMLParser):

	def __init__(self):
		self.links = []
		self.data = []
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
						self.data.append('<img>')
						self.data.append(value)
						self.data.append('</img>')
						self.img = None
						break

	def handle_data(self,data):
		if self.process == PROCESS.START:
			self.data.append('<content>')
			self.process = PROCESS.ON
		elif self.process == PROCESS.ON:
			self.data.append(data)



	def handle_endtag(self,tag):
		if tag == 'p':
			if self.process == PROCESS.ON:
				self.data.append('</content>')
			self.process = PROCESS.END
			


contentPath = os.path.dirname(__file__) + '/search.html'
with open(contentPath,'r') as f:
	content = f.read() 
	dp = DataParser()
	dp.feed(content)
	dp.close()
	#print dp.links
	for item in dp.data:
		print item