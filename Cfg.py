#coding=utf-8
import ConfigParser
import os

CFG_FILE = os.path.dirname(__file__) + '/conf/conf.ini'
CFG_SESSION = 'tweibo'

config = ConfigParser.ConfigParser()
with open(CFG_FILE,'r') as cfg:
	config.readfp(cfg)

cfg = lambda name:config.get(CFG_SESSION,name)
