# -*- coding: utf-8 -*-

import DiscordBot
import StoreInfoWeb

TOKEN = "DISCORD-TOKEN"
ServerName = "DISCORD-SERVER"
ChannelName = "DISCORD-CHANNEL"

class MeshiyaUpdate:
	def __init__(self, statusCallbackFunc):
		self.cbStatus = statusCallbackFunc

	def cbGetStoreInfoDone(self, url):
		if url == None:
			self.cbStatus("Get all store info ... done")
			self.cbStatus("Updating html")
		else:	
			self.cbStatus("{url} ... done".format(url=url))

	def update(self):
		self.cbStatus("Getting store list from {ch} channel of discord".format(ch=ChannelName))
		client = DiscordBot.MyClient(ServerName, ChannelName)
		client.run(TOKEN)
		urlList = client.getURLs()
		self.cbStatus("Get store list ... done")
		self.cbStatus("Getting store information from URLs...")
		store = StoreInfoWeb.Store(self.cbGetStoreInfoDone)
		store.createWebPage(urlList, "restaurants")
		self.cbStatus("Update html ... done")
		self.cbStatus("finished")
