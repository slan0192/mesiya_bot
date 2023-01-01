#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

import sys
import websocket
import Meshiya
import Sakaya

DEBUG = False
WS_SERVER = "ws://localhost:9001/"

def dbgLog(msg):
	if DEBUG == True:
		with open("client.log", mode="a") as f:
			print(msg, file=f)

class updateClient:
	def __init__(self, _tp):
		dbgLog("client init (type={tp})".format(tp=_tp))
		self.tp = _tp
		self.ws = websocket.WebSocketApp(WS_SERVER,
			on_open = self.onOpen,
			on_message = self.onMessage,
			on_error = self.onError,
			on_close = self.onClose)

	def sendMessage(self, ws, msg):
		dbgLog(msg)
		ws.send(msg)

	def onOpen(self, ws):
		dbgLog("open: send msg: worker")
		ws.send("worker")

	def statusCallback(self, msg):
		self.sendMessage(self.ws, msg)

	def onMessage(self, ws, message):
		if message == "worker: OK":
			if self.tp == "meshiya":
				meshiya = Meshiya.MeshiyaUpdate(self.statusCallback)
				meshiya.update()
			elif self.tp == "sakaya":
				sakaya = Sakaya.SakayaUpdate(self.statusCallback)
				sakaya.update()
		ws.close()

	def onError(self, ws, error):
		dbgLog(error)
	
	def onClose(self, ws, close_status_code, close_msg):
		dbgLog("closed")
	
	def run(self):
		dbgLog("client run")
		self.ws.run_forever()

args = sys.argv
if len(sys.argv) < 2:
	tp = "meshiya"
else:
	tp = sys.argv[1]
client = updateClient(tp)
client.run()
