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
	store["name"] = bs.find(class_='restaurant-summary__display-name').text.strip()
	
	#最寄＆ジャンル
	store["genre"] = [];
	div_tags = bs.find(class_='restaurant-summary__footer').findAll('div', {'class': 'information-list__item'})
	for div_tag in div_tags:
		if div_tag.find('dt').text.strip() == u'最寄駅':
			store["station"] = div_tag.find('dd').text.strip()
		if div_tag.find('dt').text.strip() == u'ジャンル':
			store["genre"].extend(div_tag.find('dd').text.strip().split(" "))
			
	#所在地
	store["addr"] = bs.find(class_='restaurant-info-table__map').find('a').text.strip()

	#写真
	store["photo"] = [];
	n = 0
	div_tags = bs.findAll(class_='restaurant-images__image')
	for div_tag in div_tags:
		img_tag = div_tag.find('img')
		tmp = img_tag['data-src'].split('/')
		filename = store["name"] + "_" + tmp[len(tmp) - 1]
		
		if downloadImage(img_tag['data-src'], filename):
			store["photo"].append(filename)
		n += 1
		if (n == 3):
			break

	return store
