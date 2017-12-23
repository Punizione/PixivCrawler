# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tornado import ioloop
import tornado.web
from tornado import httpserver
import json
import os.path
import tornado.escape
import ConfigManager as CM
import Pixiv
import os
from LoginManager import accountSingleton as account

class HotSpotViewHandler(tornado.web.RequestHandler):
	def post(self, *args, **kwargs):
		print(self.request.body)
		data = json.loads(self.request.body)
		#json.loads
		mode = data['mode']
		date = data['date']
		page = data['page']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		result = Pixiv.getHotSpotView(mode, date, page)
		#print(result)
		if result['statu']:
			self.write(json.dumps( {"ret": True, "data": result['res'], "operatorInfo":result['operatorInfo'] } ))
		else:
			self.write(json.dumps( {"ret": False } ))
	def get(self):
		result = Pixiv.getHotSpotView('daily', '20171212', '1')
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		if result['statu']:
			self.write(json.dumps( {"ret": True, "data": result['res'],"operatorInfo":result['operatorInfo'] } ))
		else:
			self.write(json.dumps( {"ret": False } ))

class LoginHandler(tornado.web.RequestHandler):
	def post(self, *args, **kwargs):
		print(self.request.body)
		data = json.loads(self.request.body)
		userId = data['userId']
		password = data['password']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		result = account.login(userId, password)
		if result['success']:
			self.write(json.dumps({'ret': True}))
		else:
			self.write(json.dumps({'ret': False}))

	def get(self):
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		result = account.loginWithCookies()
		if result['success']:
			self.write(json.dumps({'ret': True}))
		else:
			self.write(json.dumps({'ret': False}))

class UserIdHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		result = Pixiv.getMyUserId()
		if result['statu']:
			self.write(json.dumps({'ret': True, 'userId': result['userId'] } ))
		else:
			self.write(json.dumps({'ret': False } ))


class CollectionViewHandler(tornado.web.RequestHandler):
	def post(self, *args, **kwargs):
		print(self.request.body)
		data = json.loads(self.request.body)
		userId = data['userId']
		page = data['page']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		result = Pixiv.getCollectionsView(userId, page)
		if result['statu']:
			self.write(json.dumps( {"ret": True, "data": result['res'], "operatorInfo":result['operatorInfo'], "userNow":result['userNow'] } ))
		else:
			self.write(json.dumps( {"ret": False, "userNow":result['userNow'] } ))
	def get(self):
		result = Pixiv.getCollectionsView("", "1")
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		if result['statu']:
			self.write(json.dumps( {"ret": True, "data": result['res'], "operatorInfo":result['operatorInfo'], "userNow":result['userNow'] } ))
		else:
			self.write(json.dumps( {"ret": False, "userNow":result['userNow'] } ))

class PainterViewHandler(tornado.web.RequestHandler):
	def post(self, *args, **kwargs):
		print(self.request.body)
		data = json.loads(self.request.body)
		userId = data['userId']
		page = data['page']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		result = Pixiv.getPainterView(userId, page)
		if result['statu']:
			self.write(json.dumps( {"ret": True, "data": result['res'], "operatorInfo":result['operatorInfo'], "userNow":result['userNow'] } ))
		else:
			self.write(json.dumps( {"ret": False, "userNow":result['userNow'] } ))
	def get(self):
		result = Pixiv.getPainterView("", "1")
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		if result['statu']:
			self.write(json.dumps( {"ret": True, "data": result['res'], "operatorInfo":result['operatorInfo'], "userNow":result['userNow'] } ))
		else:
			self.write(json.dumps( {"ret": False, "userNow":result['userNow'] } ))

class DownloadHandler(tornado.web.RequestHandler):
	def post(self, *args, **kwargs):
		data = json.loads(self.request.body)
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		data = data['data']
		result = Pixiv.addToDownloadList(data)
		if result['statu']:
			self.write(json.dumps( {"ret": True } ))
		else:
			self.write(json.dumps( {"ret": False } ))
	def get(self):
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		result = Pixiv.getDownloadList()
		if result['statu']:
			self.write(json.dumps( {"ret": True, "data": result['res'] } ))
		else:
			self.write(json.dumps( {"ret": False } ))

class SettingHandler(tornado.web.RequestHandler):
	def post(self, *args, **kwargs):
		data = json.loads(self.request.body)
		typ = data['type']
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		if typ=="proxy":
			if not data['proxyType']=="none":
				CM.saveProxy({ 'type': data['proxyType'], 'port':data['port'] })
			else:
				CM.saveProxy()
			account.accountSession.proxies = CM.getProxy()
			self.write(json.dumps( {"ret": True } ))
		else:

			if CM.hasPath(data['path']):
				CM.savePath(data['path'])
				self.write(json.dumps( {"ret": True } ))
			else:
				self.write(json.dumps( {"ret": False } ))
		#self.write(json.dumps( {"ret": True } ))

	def get(self):
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		proxyData = CM.getProxySetting()
		pathData = CM.getPath()
		self.write(json.dumps({"ret": True, "proxyData":proxyData, "pathData":pathData }))


class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Content-Type', 'application/json; charset=UTF-8')
		data = CM.Logout()
		self.write(json.dumps({"ret": True, "data":data }))

class CloseHandler(tornado.web.RequestHandler):
		def get(self):
			os._exit(0)

def main():
	application = tornado.web.Application([
		(r"/hot", HotSpotViewHandler),
		(r"/login", LoginHandler),
		(r"/collections", CollectionViewHandler),
		(r"/user", UserIdHandler),
		(r"/painter", PainterViewHandler),
		(r"/download", DownloadHandler),
		(r"/setting", SettingHandler),
		(r"/logout", LogoutHandler),
		(r"/close", CloseHandler)
	])
	application.add_handlers(r"^localhost/hot$", [(r"/hot",HotSpotViewHandler)])
	application.add_handlers(r"^localhost/login$", [(r"/login", LoginHandler)])
	application.add_handlers(r"^localhost/collections$", [(r"/collections", CollectionViewHandler)])
	application.add_handlers(r"^localhost/user$", [(r"/user", UserIdHandler)])
	application.add_handlers(r"^localhost/painter$", [(r"/painter", PainterViewHandler)])
	application.add_handlers(r"^localhost/download$", [(r"/download", DownloadHandler)])
	application.add_handlers(r"^localhost/setting$", [(r"/setting", SettingHandler) ])
	application.add_handlers(r"^localhost/logout$", [(r"/logout", LogoutHandler) ])
	application.add_handlers(r"^localhost/close$", [(r"/close", CloseHandler) ])
	server = httpserver.HTTPServer(application)
	server.listen(7493)
	try:
		ioloop.IOLoop.current().start()
	except KeyboardInterrupt:
		ioloop.IOLoop.current().stop()

if __name__ == '__main__':
	main()
