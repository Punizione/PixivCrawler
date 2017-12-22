# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import configparser
import sys

loginHeaders = {
	"Accept":"application/json, text/javascript, */*; q=0.01",
	"Accept-Encoding":"gzip, deflate, br",
	"Accept-Language":"zh-CN,zh;q=0.9",
	"Connection":"keep-alive",
	"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
	#"Host":"accounts.pixiv.net",
	"Origin":"https://accounts.pixiv.net",
	"Referer":"https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"X-Requested-With":"XMLHttpRequest"
}

imgaeHeaders = {
	"Host": "i.pximg.net",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"Referer":"https://www.pixiv.net"
}

collectionHeaders = {
	"Host" : "www.pixiv.net",
	"Referer": "https://www.pixiv.net/",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
}

loginUrl = 'https://accounts.pixiv.net/api/login?lang=zh'
collectionsUrl = "https://www.pixiv.net/bookmark.php"
painterUrl = "https://www.pixiv.net/member_illust.php"
userIdUrl = "https://www.pixiv.net/"
pageDataUrl = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
tokenUrl = "https://www.pixiv.net/ranking.php?mode=daily&content=illust"
hotSpotUrl = "https://www.pixiv.net/ranking.php"



def savePath(path=os.getcwd()):
	cf = configparser.ConfigParser()
	cf.read('config.conf')
	if not cf.has_section('path'):
		cf.add_section('path')
		cf.write(open('config.conf', 'w'))
		cf.write(sys.stdout)
	cf.set('path', 'savepath', path)
	cf.write(open('config.conf', 'w'))
	cf.write(sys.stdout)

def getPath():
	cf = configparser.ConfigParser()
	cf.read('config.conf')
	if not cf.has_section('path'):
		savePath()
	if not cf.has_option('path', 'savepath'):
		savePath()
	cf.read('config.conf')
	return cf.get('path', 'savepath')

def getProxy():
	cf = configparser.ConfigParser()
	cf.read('config.conf')
	if not cf.has_section('proxy'):
		saveProxy()
	if not cf.has_option('proxy', 'type'):
		saveProxy()
	cf.read('config.conf')
	proxyType = cf.get('proxy', 'type')
	if proxyType == 'none':
		return None
	else:
		port = cf.get('proxy', 'port')
		return {
			'http': proxyType+'://localhost:'+port,
			'https': proxyType+'://localhost:'+port
			}

def saveProxy(proxy=None):
	cf = configparser.ConfigParser()
	cf.read('config.conf')
	if not cf.has_section('proxy'):
		cf.add_section('proxy')
		cf.write(open('config.conf', 'w'))
		cf.write(sys.stdout)
	if proxy:
		proxyType = proxy['type']
		cf.set('proxy', 'type', proxyType)
		cf.write(open('config.conf', 'w'))
		cf.write(sys.stdout)
		port = proxy['port']
		cf.set('proxy', 'port', port)
		cf.write(open('config.conf','w'))
		cf.write(sys.stdout)
	else:
		cf.set('proxy', 'type', 'none')
		cf.write(open('config.conf','w'))
		cf.write(sys.stdout)

def getProxySetting():
	cf = configparser.ConfigParser()
	cf.read('config.conf')
	if not cf.has_section('proxy'):
		saveProxy()
	if not cf.has_option('proxy', 'type'):
		saveProxy()
	cf.read('config.conf')
	proxyType = cf.get('proxy', 'type')
	if proxyType == 'none':
		return {"type" :"none"}
	else:
		port = cf.get('proxy', 'port')
		return { "type": proxyType, "port": port }


def hasPath(path):
	if path=="":
		savePath()	
		return True
	if not os.path.exists(path):
		return False
	else:
		savePath(path)
		return True


def Logout():
	path = os.getcwd()
	if os.path.isfile(path+"\\cookies"):
		os.remove(path+"\\cookies")
		return { "flag":"scuccess" }
	else:
		return { "flag":"fail" }