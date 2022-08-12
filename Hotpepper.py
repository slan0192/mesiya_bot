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

	bs = BeautifulSoup(page.text, 'html.parser')
	page.close()

	store = {}

	#店舗名
	store["name"] = bs.find(class_='shopName').text.strip()
	
	#最寄＆ジャンル
	store["genre"] = [];
	dl_tags = bs.findAll('dl', {'class':'shopInfoInnerSectionBlock'})
	for dl_tag in dl_tags:
		if dl_tag.find('dt').text.strip() == u'ジャンル':
			p_tags = dl_tag.findAll('p')
			for p_tag in p_tags:
				store["genre"].append(p_tag.text.strip());
		if dl_tag.find('dt').text.strip() == u'エリア':
			store["station"] = dl_tag.find('p').text.strip()

	#所在地
	tr_tags = bs.find(class_='shopInfoDetail').findAll('tr')
	for tr_tag in tr_tags:
		if tr_tag.find('th').text.strip() == u'住所':
			store["addr"] = tr_tag.find('td').text.strip()
			break

	#写真
	store["photo"] = [];
	p_tags = bs.findAll('p', {'class':'slideShow'})
	n = 0;
	for p_tag in p_tags:
		img_tag = p_tag.find('img')
		tmp = img_tag['src'].split('/')
		filename = store["name"] + "_" + tmp[len(tmp) - 1]
		if downloadImage(img_tag['src'], filename):
			store["photo"].append(filename)
		n += 1
		if (n == 3):
			break

	return store
