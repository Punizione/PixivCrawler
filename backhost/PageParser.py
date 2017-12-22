# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import re
import json

def parseCollections(text):
	soup = BeautifulSoup(text, "html5lib")
	imageItems = soup.find_all("li", class_="image-item")
	collectionDataSet = []
	if imageItems:
		for item in imageItems:
			img = item.find('img')
			image_thumbnail_src = img['data-src']#.replace('/150x150', '/240x480')
			image_src = img['data-src'].replace('c/150x150/img-master', 'img-original').replace('_master1200', '')
			illust_id = img['data-id']
			user_id = img['data-user-id']
			collectionDataSet.append( { "image_thumbnail_src": image_thumbnail_src,
										"image_src": image_src,
										"illust_id": illust_id,
										"user_id": user_id } )
	return collectionDataSet


def parseOperatorFromCollections(text):
	soup = BeautifulSoup(text, "html5lib")
	pageContainer = soup.find('div', class_='pager-container')
	if pageContainer:
		prevPage = pageContainer.find("span", class_="prev").find("a")
		#print(prevPage)
		nextPage = pageContainer.find("span", class_="next").find("a")
		#print(nextPage)
		prev_page = ""
		next_page = ""
		pageNow = pageContainer.find("li",class_="current").get_text()
		if prevPage:
			prev_page = "%d" %(int(pageNow)-1)
		if nextPage:
			next_page = "%d" %(int(pageNow)+1)
		operatorInfo = {
			"prev_page": prev_page,
			"next_page": next_page,
			"pageNow": pageNow
		}
		return { "statu": True, "operatorInfo": operatorInfo }
	else:
		return { "statu": True }


def parsePainter(text):
	soup = BeautifulSoup(text, "html5lib")
	imageItems = soup.find_all("li", class_="image-item")
	painterDataSet = []
	if imageItems:
		for item in imageItems:
			img = item.find('img')
			image_thumbnail_src = img['data-src']#.replace('/150x150', '/240x480')
			image_src = img['data-src'].replace('c/150x150/img-master', 'img-original').replace('_master1200', '')
			illust_id = img['data-id']
			user_id = img['data-user-id']
			painterDataSet.append( { "image_thumbnail_src": image_thumbnail_src,
										"image_src": image_src,
										"illust_id": illust_id,
										"user_id": user_id } )
	return painterDataSet


def parseOperatorFromPainter(text):
	soup = BeautifulSoup(text, "html5lib")
	pageContainer = soup.find('div', class_='pager-container')
	if pageContainer:
		prevPage = pageContainer.find("span", class_="prev").find("a")
		#print(prevPage)
		nextPage = pageContainer.find("span", class_="next").find("a")
		#print(nextPage)
		prev_page = ""
		next_page = ""
		pageNow = pageContainer.find("li",class_="current").get_text()
		if prevPage:
			prev_page = "%d" %(int(pageNow)-1)
		if nextPage:
			next_page = "%d" %(int(pageNow)+1)
		operatorInfo = {
			"prev_page": prev_page,
			"next_page": next_page,
			"pageNow": pageNow
		}
		return { "statu": True, "operatorInfo": operatorInfo }
	else:
		return { "statu": True }

def parseUserId(text):
	soup = BeautifulSoup(text, "html5lib")
	profile = soup.find('div', class_="_profile-menu-unit")
	#print(profile)
	if profile:
		data = profile.find('li').find('a')
		#print(data['href'])
		pattern = re.compile(r"/member\.php\?id=(.+)", re.S)
		userId = pattern.findall(data['href'])[0]
		print(userId)
		return { "statu": True, "userId": userId }
	else:
		return { "statu": False }


def parseOperatorFromHotSpot(dataJson):
	next_date = ""
	prev_page = ""
	next_page = ""
	prev_date = ""
	modeNow = dataJson['mode']
	pageNow = dataJson['page']
	dateNow = dataJson['date']
	if dataJson['prev_date'] : 
		prev_date = dataJson['prev_date']
	if dataJson['next_date'] :
		next_date = dataJson['next_date']
	if dataJson['prev']:
		prev_page = dataJson['prev']
	if dataJson['next']:
		next_page = dataJson['next']

	operatorInfo = {
		"next_date": next_date,
		"prev_page": prev_page,
		"next_page": next_page,
		"prev_date": prev_date,
		"modeNow": modeNow,
		"pageNow": pageNow,
		"dateNow": dateNow
	}
	#print(operatorInfo)
	return operatorInfo


def parseHotSpot(dataJson):
	#print(dataJson['page'])
	illustDataSet = []
	contents = dataJson['contents']
	for item in contents:
		illust_id = item['illust_id']
		user_id = item['user_id']
		image_src = item['url'].replace('c/240x480/img-master', 'img-original').replace('_master1200', '')
		image_thumbnail_src = item['url']
		illustDataSet.append( { "illust_id":illust_id, 
								"user_id":user_id, 
								"image_src":image_src, 
								"image_thumbnail_src":image_thumbnail_src } )
	return illustDataSet









