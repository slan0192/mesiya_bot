#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

import DiscordBot
import StoreInfoWeb
import exLock

TOKEN = "DISCORD-TOKEN"
ServerName = "DISCORD-SERVER"
ChannelName = "DISCORD-CHANNEL"

lock = exLock.exLock("./lock")
lock_success = lock.lock()
if lock_success == True:
	client = DiscordBot.MyClient(ServerName, ChannelName)
	client.run(TOKEN)
	urlList = client.getURLs()
	store = StoreInfoWeb.Store()
	store.createWebPage(urlList, "tavern")
	lock.unlock()

print("Content-type: text/html;\n")
print("<meta http-equiv=\"refresh\" content=\"0;URL=http://homeskill.zenno.info/zatsukai/nomikui/tavern.html\">")
