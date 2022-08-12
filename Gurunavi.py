# -*- coding: utf-8 -*-

import sys
import os
import requests
from bs4 import BeautifulSoup

def downloadImage(url, filename):
	path = "img/" + filename
	if os.path.exists(path):
		return True
	jpg = requests.get(url)
	if jpg.status_code != 200:
		return False

	with open(path, "wb") as fout:
		fout.write(jpg.content)
	return True

def getInfo(url):
	page = requests.get(url)
	if page.status_code != 200:
		return None

	bs = BeautifulSoup(page.content, 'html.parser')
	page.close()

	store = {}

	#店舗名
	store["name"] = bs.find(class_='shop-info__name').find('a').text.strip()
	
	#最寄＆ジャンル
	store["station"] = bs.find('dd', {'id':'header-meta-sta-desc'}).find('li').find('a').text.strip()

	store["genre"] = [];
	li_tags = bs.find('dd', {'id':'header-meta-gen-desc'}).findAll('li')
	for li_tag in li_tags:
		store["genre"].append(li_tag.find('a').text.strip())

	#所在地
	tr_tags = bs.find('div', {'id':'info-table'}).findAll('tr')
	for tr_tag in tr_tags:
		if tr_tag.find('th').text.strip() == u'住所':
			store["addr"] = tr_tag.find('td').find('p').find('span').text.strip()
			break

	#写真
	store["photo"] = [];
	n = 0
	img_tags = bs.find('div', {'id': 'pickup'}).findAll('img')
	for img_tag in img_tags:
		tmp = img_tag['src'].split('/')
		filename = store["name"] + "_" + tmp[len(tmp) - 1]
		if (filename.find("?") > 0):			
			filename = filename[0:filename.rindex("?")]
		
		if downloadImage(img_tag['src'], filename):
			store["photo"].append(filename)
		n += 1
		if (n == 3):
			break

	return store
