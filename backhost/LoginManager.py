# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json
import os
import time
import http.cookiejar as cookielib

import ConfigManager as CM


class AccountManager(object):
	"""
	this is a account login in Pixiv
	it keeps a Session with cookie
	"""
	def __init__(self, loginUrl):
		super(AccountManager, self).__init__()
		self.accountSession = requests.Session()
		self.accountSession.proxies = CM.getProxy()
		self.accountSession.headers.update(CM.loginHeaders)
		self.accountSession.cookies = cookielib.LWPCookieJar(filename='cookies')
		self.loginUrl = loginUrl


	def getSession(self):
		return self.accountSession

	def loginWithCookies(self):
		try:
			self.accountSession.cookies.load(ignore_discard=True)
			print('Login Success')
			return {"success": True}
		except:
			print('Login Statu has lapsed')
			return {"success": False}

	def login(self, userId, password):
		userData = {"pixiv_id":userId, "password":password}
		pageData = self.getPageData()
		postData=dict(pageData, **userData)
		response = self.accountSession.post(self.loginUrl, data=postData)
		response.encoding = 'utf-8'
		#print(response)
		result = response.json()['body']
		print(result)
		loginSuccess = {'success': {'return_to': 'https://www.pixiv.net/'}}
		if result == loginSuccess:
			print('Login Success')
			self.accountSession.cookies.save()
			return {'success': True}
		else:
			print("Login Fail")
			return {'success': False}

	def getToken(self):
		'''
			You have to login first, then call this function.
			It will return a token which can be used in downloading. 

		'''
		illustUrl = CM.tokenUrl
		illustResponse = self.accountSession.get(illustUrl)
		illustResponse.encoding = 'utf-8'
		soup = BeautifulSoup(illustResponse.text,"html5lib")
		ul = soup.find('ul',class_='languages')
		li = ul.find_all('li')[0]
		form = li.find('form',attrs={'name':'setja'})
		inp = form.find_all('input')
		token = inp[1]['value']
		
		return token

	def getPageData(self):
		pageUrl = CM.pageDataUrl
		pageResponse = self.accountSession.get(pageUrl)
		pageResponse.encoding = 'utf-8'
		#print(pageResponse.text)
		soup = BeautifulSoup(pageResponse.text, "html5lib")
		div = soup.find('div',attrs={'id':'old-login'})
		#print(div)
		inp = div.find_all('input')
		#print("Get Input TextField Success:"+str(len(inp)))

		post_key = inp[0]['value']
		return_to = inp[1]['value']
		lang = inp[2]['value']
		source = inp[3]['value']

		ret = { "post_key":post_key,
				"return_to":return_to,
				"lang":lang,
				"source":source,
				"ref":"wwtop_accounts_index",
				"captcha":"",
				"g_recaptcha_response":""
				}
		return ret

	def getCookie(self):
		coo = self.getSession().cookies
		cookieData = []
		for c in coo:
			cookieData.append( { 
				"name": c.name, 
				"value": c.value,
				"domain": c.domain,
				"url": c.domain
			} )
		return cookieData


		


accountSingleton = AccountManager(CM.loginUrl)