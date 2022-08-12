# -*- coding: utf-8 -*-

import sqlite3

class StoreDB:
	def __init__(self):
		self.conn = sqlite3.connect('store.db')
		self.cur = self.conn.cursor()
		self._create_table()
		self.conn.commit()

	def _is_exists_table(self, tb_name):
		self.cur.execute("select name from sqlite_master where type='table';")
		exists = False
		for tb in self.cur.fetchall():
			if tb_name == tb[0]:
				exists = True
				break
		return exists

	def _create_table(self):
		if not self._is_exists_table("discord"):
			self.cur.execute("create table discord(ID integer primary key autoincrement, Channel text, LastMessageID text)")
		if not self._is_exists_table("restaurants"):
			self.cur.execute("create table restaurants(ID integer primary key autoincrement, Url text, Name text, Address text, Station text, Genre text, Photo text)")
		if not self._is_exists_table("tavern"):
			self.cur.execute("create table tavern(ID integer primary key autoincrement, Url text, Name text, Address text, Station text, Genre text, Photo text)")

	def close(self):
		self.cur.close()
		self.conn.close()

	def getDiscordLastMessage(self, channel):
		self.cur.execute("select LastMessageID from discord where Channel='" + channel + "';")
		data = self.cur.fetchone()
		if data == None:
			return None
		return data[0]

	def insertDiscordData(self, channel, messageId):
		sql_str = "insert into discord (Channel,LastMessageID) values('{channel}','{id}');".format(channel=channel, id=messageId)
		self.cur.execute(sql_str)
		self.conn.commit()

	def updateDiscordData(self, channel, messageId):
		sql_str = "update discord set LastMessageID='{id}' where Channel='{channel}';".format(id=messageId, channel=channel)
		print(sql_str)
		self.cur.execute(sql_str)
		self.conn.commit()

	def existsStoreData(self, url, table):
		self.cur.execute("select url from " + table + " where url='" + url + "';")
		if self.cur.fetchone() == None:
			return False
		return True

	def addStoreData(self, url, data, table):
		if data == None:
			self.cur.execute("insert into " + table + "(Url) values('" + url + "')")
		else:
			sql_items = "(Url, Name"
			sql_values = "values('" + url + "', '" + data["name"].replace("'", "''") + "'"
			if "addr" in data:
				sql_items += ", Address"
				sql_values += ", '" + data["addr"] + "'"
			if "station" in data:
				sql_items += ", Station"
				sql_values += ", '" + data["station"] + "'"
			if "genre" in data:
				sql_items += ", Genre"
				sql_values += ", '" + ":".join(data["genre"]) + "'"
			if "photo" in data:
				sql_items += ", Photo"
				sql_values += ", '" + ":".join(data["photo"]).replace("'", "''") + "'"
			sql_items += ")"
			sql_values += ")"
			sql_str = "insert into " + table + sql_items + " " + sql_values
			self.cur.execute(sql_str)

	def getStoreData(self, table):
		jp_states = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]
		storeData = {}
		self.cur.execute("select * from " + table + ";");
		for row in self.cur:
			data = {"url":row[1], "name":row[2], "address":row[3], "station":row[4], "genre":row[5], "photo":row[6]}
			if data["address"] == None:
				if not "その他" in storeData:
					storeData["その他"] = []
				storeData["その他"].append(data)
			else:
				for st in jp_states:
					if data["address"].find(st) >= 0:
						if not st in storeData:
							storeData[st] = []
						storeData[st].append(data);
						break

		return storeData

	def commit(self):
		self.conn.commit()
