# -*- coding: utf-8 -*-

import sqlite3

import Tabelog
import Hotpepper
import Gurunavi
import Retty
import GoogleMaps
import Google
import DataBase

class Store:
	def __init__(self, cbGetInfoDone):
		self.db = DataBase.StoreDB()
		self.getInfoDoneCallback = cbGetInfoDone

	def _getInfo(self, url):
		if url.find("tabelog.com") >= 0:
			storeInfo = Tabelog.getInfo(url)
			#写真がなぜか取れないことがあるので、その場合は１回だけリトライする。本当なら同期とった方が良いけど面倒そうなのでw
			if storeInfo["photo"] == None or len(storeInfo["photo"]) == 0:
				storeInfo = Tabelog.getInfo(url)
		elif url.find("hotpepper.jp") >= 0:
			storeInfo = Hotpepper.getInfo(url)
		elif url.find("gnavi.co.jp") >= 0:
			storeInfo = Gurunavi.getInfo(url)
		elif url.find("retty.me") >= 0:
			storeInfo = Retty.getInfo(url)
		elif url.find("goo.gl/maps") >= 0:
			storeInfo = GoogleMaps.getInfo(url)
		else:
			storeInfo = Google.searchByTitle(url)
	
		return storeInfo

	def _addDataToDataBase(self, urls, tp):
		for url in urls:
			if not self.db.existsStoreData(url, tp):
				storeInfo = self._getInfo(url)
				if storeInfo == None:
					self.db.addStoreData(url, None, tp)
				else:
					self.db.addStoreData(url, storeInfo, tp)
				self.db.commit();
				self.getInfoDoneCallback(url)
		self.getInfoDoneCallback(None)

	def createWebPage(self, urls, tp):
		if tp != "restaurants" and tp != "tavern":
			print("Please specify restaurants or tavern to tp (type)")
			return
		self._addDataToDataBase(urls, tp)
		datas = self.db.getStoreData(tp)
		self.db.close();

		html = '''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja-JP">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <link rel="stylesheet" href="main.css" type="text/css" />
  <title>Void</title>
</head>
<body>
  <h1 class="title">Void</h1>
  <div class="contents">
  	<div class="update"><a href="update.py?type={type}">お店情報更新</a></div>
'''.format(type=("meshiya" if tp == "restaurants" else "sakaya"))

		jp_states = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]

		html += "    <p>\n"
		for st in jp_states:
			if not st in datas:
				continue
			html += '      <a href="#{state}" class="jp_state_list">{state}</a>\n'.format(state=st)
		html += '    </p>\n'

		for st in jp_states:
			if not st in datas:
				continue
			html += '''
    <h2 id="{state}" class="jp_state">{state}</h2>
    <div class="card-grid">
'''.format(state=st)
			for d in datas[st]:
				html += '      <section class="card">\n'
				if d["photo"] != None:
					photos = d["photo"].split(":")
					html += '        <img class="card-img" src="img/{photo}" alt="" />'.format(photo=photos[0])
				if d["station"] == None:
					d["station"] = ""
				html += '''
        <div class="card-content">
          <a href="{url}" target="_blank"><h1 class="card-title">{name}</h1></a>
          <p class="card-text">
            <div>{genre}</div>
            <div>住所：{address}</div>
            <div>最寄：{station}</div>
          </p>
        </div>
      </section>
'''.format(url=d["url"], name=d["name"], genre=d["genre"].replace(":", ","), address=d["address"], station=d["station"])
			html += "    </div>\n"

		html += '''
  </div>
</body>
</html>
'''

		with open(tp + ".html", mode="w") as f:
			print(html, file=f)
