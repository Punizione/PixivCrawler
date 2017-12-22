# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json
import os
import re
import time
import queue
from collections import deque
import threading

import ConfigManager as CM
from LoginManager import accountSingleton as account
import base64
import copy


def download(data):
	extra = data['extra']
	typeNow = extra['type']

	path = CM.getPath()+"\\"+typeNow
	if not os.path.exists(path):
		os.mkdir(path)
	if typeNow=="hotspot":
		path = path+"\\"+extra['mode']
		if not os.path.exists(path):
			os.mkdir(path)
		path = path+"\\"+extra['date']
		if not os.path.exists(path):
			os.mkdir(path)
	else:
		path = path+"\\"+extra['user']
		if not os.path.exists(path):
			os.mkdir(path)
	imageUrl = data['image_src']
	illust_id = data['illust_id']
	s.headers.update(CM.imgaeHeaders)
	pattern = re.compile(r"[^\.]\w*$", re.S)
	fileType = re.findall(pattern, imageUrl)[0]
	fileName = str(illust_id)+'.'+fileType
	if os.path.isfile(os.path.join(path, fileName)):
		return 
	try:
		newImage =  s.get(imageUrl)
	except Exception as e:
		print(e)
		time.sleep(2)
		newImage =  s.get(imageUrl)
	with open(path+'\\'+fileName,'wb') as imageFile:
			imageFile.write(newImage.content)
	if os.path.getsize(os.path.join(path, fileName)) < 200:
		os.remove(str(os.path.join(path, fileName)))
		fileName = fileName.replace('.jpg', '.png')
		if os.path.isfile(os.path.join(path, fileName)):
			return
		imageUrl = imageUrl.replace('.jpg', '.png')
		with open(path+'\\'+fileName, 'wb') as imageFile:
			imageFile.write(s.get(imageUrl).content)




def processDownload(downloadList):
	while not exitFlag:
		queueLock.acquire()
		if len(downloadList):
			data = downloadList.popleft()
			queueLock.release()
			download(data)
		else:
			queueLock.release()
		time.sleep(1)

class downloadThread(threading.Thread):
	def __init__(self, q):
		threading.Thread.__init__(self)
		self.q = q
	def run(self):
		print("Donwload Thread Start")
		processDownload(self.q)
		print("Download Thread Stop")




queueLock = threading.Lock()
downloadList = deque()
exitFlag = False
#s = account.getSession()
s = requests.Session()
s.cookies = account.getSession().cookies
s.proxies = account.getSession().proxies
s.headers.update(CM.imgaeHeaders)
#s = copy.deepcopy(account.getSession())
down = downloadThread(downloadList)
down.start()




def addToDownloadList(dataSet):
	try:
		queueLock.acquire()
		for data in dataSet:
			downloadList.append(data)
		statu = True
	except Exception as e:
		print(e)
		statu = False
	finally:
		queueLock.release()
		return { "statu": statu }

def getDownloadList():
	dataSet = []
	try:
		for data in downloadList:
			dataSet.append({'illust_id': data['illust_id']})
		return {"statu": True, "data": dataSet }
	except Exception as e:
		print(e)
		return {"statu": False }

def getThumbnail(image_src):
	s = account.getSession()
	image = s.get(image_src).content
	#print(type(image))
	#bytes.decode(image)
	str(base64.b64encode(image).decode("utf-8"))
	baseData = str(base64.b64encode(image).decode("utf-8"))
	return baseData



if __name__ == '__main__':
	print("This is a download tool")