#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

from websocket_server import WebsocketServer

DEBUG = False
WS_SERVER = "localhost"
WS_PORT = 9001

def dbgLog(msg):
	if DEBUG == True:
		with open("server.log", mode="a") as f:
			print(msg, file=f)

class Server:
	def __init__(self, host, port):
		self.wsServer = WebsocketServer(host=host, port=port)
		self.wsServer.set_fn_new_client(self.newClient)
		self.wsServer.set_fn_client_left(self.clientLeft)
		self.wsServer.set_fn_message_received(self.messageReceived)
		self.clientList = []
		self.workerClient = None

	def newClient(self, client, server):
		dbgLog("connect client: {client}".format(client=client['id']))
		self.clientList.append(client)

	def clientLeft(self, client, server):
		dbgLog("disconnect client: {client}".format(client=client['id']))
		if self.workerClient == client:
			dbgLog("\t remove worker client")
			self.workerClient = None
		else:
			dbgLog("\t remove client")
			self.clientList.remove(client)
		
		if self.workerClient == None and len(self.clientList) == 0:
			dbgLog("all client disconnected")
			self.wsServer.shutdown()


	def messageReceived(self, client, server, message):
		dbgLog("recv: {msg}".format(msg=message))
		if message == "worker":
			if self.workerClient == None:
				self.clientList.remove(client)
				self.workerClient = client
				self.wsServer.send_message(client, "worker: OK")
				dbgLog("set worker: {client}".format(client=client['id']))
			else:
				self.wsServer.send_message(client, "worker: NO")
			return

		for c in self.clientList:
			self.wsServer.send_message(c, message)
			dbgLog("send (pass to {client}): {msg}".format(client=c['id'], msg=message))
			
	def run(self):
		dbgLog("run server")
		self.wsServer.run_forever()

server = Server(WS_SERVER, PORT)	
server.run()
