# -*- coding: utf-8 -*-
import discord
import DataBase

class MyClient(discord.Client):
	def __init__(self, server, channel):
		super().__init__()
		self.ServerName = server
		self.ChannelName = channel
		self.urls = []

	def getURL(self, msg):
		lines = msg.splitlines()
		for l in lines:
			if l.find("https://") >= 0:
				self.urls.append(l)

	async def on_ready(self):
		guild = discord.utils.get(super().guilds, name=self.ServerName)
		channel = discord.utils.get(guild.text_channels, name=self.ChannelName)

		db = DataBase.StoreDB()
		savedLastMessageId = db.getDiscordLastMessage(self.ChannelName)
		lastMessageId = savedLastMessageId
		if savedLastMessageId == None:
			async for msg in channel.history(oldest_first=True):
				self.getURL(msg.content)
				lastMessageId = msg.id
		else:
			savedLastMessage = await channel.fetch_message(savedLastMessageId)
			async for msg in channel.history(after=savedLastMessage.created_at):
				self.getURL(msg.content)
				lastMessageId = msg.id

		if lastMessageId != savedLastMessageId:
			if savedLastMessageId == None:
				db.insertDiscordData(self.ChannelName, lastMessageId)
			else:
				db.updateDiscordData(self.ChannelName, lastMessageId)

		await self.close()

	def getURLs(self):
		return self.urls