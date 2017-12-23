# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json
import os
import re
import time
import http.cookiejar as cookielib

import DownloadManager as DM

from LoginManager import accountSingleton as account

import ConfigManager as CM

import PageParser as PP





def getHotSpotView(mode, date, page):
	s = account.getSession()
	content = 'illust'
	fmt = 'json'
	token = account.getToken()
	IllustDataSetUrl = CM.hotSpotUrl
	data = {
		"mode": mode,
		"content": "illust",
		"format": "json",
		"token": token,
		"p": page,
		"date": date
	}
	try:
		r = s.get(IllustDataSetUrl, params=data)
		IllustDataJson = r.json()
		#print(IllustDataJson)
		operatorInfo = PP.parseOperatorFromHotSpot(IllustDataJson)
		illustDataSet = PP.parseHotSpot(IllustDataJson)
		result = {
			"statu": True,
			"res": illustDataSet,
			"operatorInfo": operatorInfo
		}
	except Exception as e:
		#print(e)
		result = {
			"statu": False
		}
	finally:
		return result

def getCollectionsView(userId, page):
	s = account.getSession()
	data = {
		"id": userId,
		"rest": "show",
		"p": page
	}
	s.headers.update(CM.collectionHeaders)
	url = CM.collectionsUrl
	try:
		r = s.get(url, params=data)
		res = PP.parseOperatorFromCollections(r.text)
		if res["statu"]:
			collectionDataSet = PP.parseCollections(r.text)
			for cData in collectionDataSet:
				cData['image_thumbnail_src'] = "data:image/jpeg;base64,"+DM.getThumbnail(cData['image_thumbnail_src'])
			#cookieData = account.getCookie()
			result = {
				"statu": True,
				"res": collectionDataSet,
				"operatorInfo": res["operatorInfo"],
				"userNow": userId
				#"cookie": cookieData
			}
		else:
			result = {
				"statu": False,
				"userNow": userId
			}
	except Exception as e:
		print(e)
		result = {
			"statu": False,
			"userNow": userId
		}
	finally:
		return result

def getPainterView(userId, page):
	s = account.getSession()
	data  = {
		"id": userId,
		"type": "illust",
		"p": page
	}
	s.headers.update(CM.collectionHeaders)
	url = CM.painterUrl
	try:
		r = s.get(url, params=data)
		res = PP.parseOperatorFromPainter(r.text)
		if res['statu']:
			painterDataSet = PP.parsePainter(r.text)
			for pData in painterDataSet:
				pData['image_thumbnail_src'] = "data:image/jpeg;base64,"+DM.getThumbnail(pData['image_thumbnail_src'])
			result = {
				"statu": True,
				"res": painterDataSet,
				"operatorInfo": res["operatorInfo"],
				"userNow": userId			
			}
		else:
			result = {
				"statu": False,
				"userNow": userId			
			}
	except Exception as e:
		print(e)
		result = {
			"statu": False,
			"userNow": userId
		}
	finally:
		return result



def getMyUserId():
	s = account.getSession()
	url = CM.userIdUrl
	s.headers.update(CM.loginHeaders)
	try:
		r = s.get(url)
		res = PP.parseUserId(r.text)
		#print(res)
		if res["statu"]:
			result = {
				"statu": True,
				"userId": res["userId"]
			}
		else:
			result = {
				"statu": False
			}
	except Exception as e:
		print(e)
		result = {
			"statu": False
		}
	finally:
		return result


def addToDownloadList(data):
	return DM.addToDownloadList(data)

def getDownloadList():
	res = DM.getDownloadList()
	if(res['statu']):
		return { "statu": True, "res": res['data'] }
	else:
		return { "statu": False }




if __name__ == '__main__':
	print("Pixiv")
