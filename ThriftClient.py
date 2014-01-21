#coding=utf-8
import DataService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from ttypes import *
from Cfg import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ThriftClient:

	def __init__(self):
		self.host = cfg('thrift_host')
		self.port = 9090
		self.socket = TSocket.TSocket(self.host,self.port)
		self.transport = TTransport.TFramedTransport(self.socket)
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = DataService.Client(self.protocol)
		self.msg = list()

	def send(self,content_list):
		for content in content_list:
			message = Message(title='tweibo',content=content)
			self.msg.append(message)

		if len(self.msg) > 0:
			for message in self.msg:
				print message.content
				print '\n*****************************\n'
			self.transport.open()
			print self.client.pushMsg(self.msg)
			self.transport.close()
			self.msg = list()