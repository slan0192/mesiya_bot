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
	idx = url.find("dtlrvwlst")
	if idx > 0:
		url = url[0:idx]
	page = requests.get(url)
	if page.status_code != 200:
		return None

	bs = BeautifulSoup(page.text, 'html.parser')
	page.close()

	store = {}

	#店舗名
	store["name"] = bs.find(class_='display-name').find('span').text.strip()
	
	#最寄＆ジャンル
	store["genre"] = [];
	dl_tags = bs.find(class_='rdheader-info-data').findAll('dl', {'class':'rdheader-subinfo__item'})
	for dl_tag in dl_tags:
		dt_tag = dl_tag.find('dt', {'class':'rdheader-subinfo__item-title'}).text.strip()
		if dt_tag == u'最寄り駅：':
			store["station"] = dl_tag.find(class_='linktree__parent-target-text').text.strip()
		if dt_tag == u'ジャンル：':
			span_tags = dl_tag.findAll('span', {'class':'linktree__parent-target-text'})
			for span_tag in span_tags:
				store["genre"].append(span_tag.text.strip())

	#所在地
	store["addr"] = bs.find(class_='rstinfo-table__address').text.strip()
	
	#写真
	store["photo"] = [];
	if bs.find(class_='rstdtl-top-postphoto__list') != None:
		li_tags = bs.find(class_='rstdtl-top-postphoto__list').findAll('li', {'class':'rstdtl-top-postphoto__item'})
		if li_tags == None:
			li_tags = bs.find(class_='p-main-photos__slider').findAll('li', {'class':'p-main-photos__slider-item'})
		n = 0;
		for li_tag in li_tags:
			img_tag = li_tag.find('img')
			tmp = img_tag['src'].split('/')
			filename = store["name"] + "_" + tmp[len(tmp) - 1]
			if downloadImage(img_tag['src'], filename):
				store["photo"].append(filename)
			n += 1
			if (n == 3):
				break

	return store
