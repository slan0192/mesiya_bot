# -*- coding: utf-8 -*-

import sys
import os
import requests
from bs4 import BeautifulSoup
import base64

def getBS4Data(title):
	page = requests.get("https://www.google.com/search?q={word}".format(word=title))
	if page.status_code != 200:
		return None

	bs = BeautifulSoup(page.text, 'html.parser')
	page.close()

	div_tag = bs.find(class_='Gx5Zad xpd EtOod pkphOe')
	a_tag = div_tag.find('a', {'class':'tHmfQe'})
	if a_tag != None:
		page = requests.get("https://www.google.com/" + a_tag.get('href'))
		if page.status_code != 200:
			return None

		bs = BeautifulSoup(page.text, 'html.parser')
		page.close()
		return bs

	return bs

def downloadImage(url, filename):
	path = "img/" + filename
	if os.path.exists(path):
		return True
	if url.find("//") == 0:
		url = "https:" + url
	jpg = requests.get(url)
	if jpg.status_code != 200:
		return False

	with open(path, "wb") as fout:
		fout.write(jpg.content)
		
	return True

def searchByTitle(url):
	page = requests.get(url)
	if page.status_code != 200:
		return None
	
	bs_org = BeautifulSoup(page.text, 'html.parser')
	page.close()
	
	title = bs_org.find('title').text	
	bs = getBS4Data(title)
	if bs == None:
		return None

	store = {}
	if bs.find(class_='BNeawe deIvCb AP7Wnd') == None:
		return None
	store["name"] = bs.find(class_='BNeawe deIvCb AP7Wnd').text.strip()
	tags = bs.findAll(class_='BNeawe tAd8D AP7Wnd')
	temp = tags[0].text.split("\n")
	store["genre"] = []
	store["genre"].append(temp[1].strip())
	temp = tags[1].text.split(" ")
	store["addr"] = temp[1].strip()

	for img_tag in bs_org.findAll('img'):
		if 'jpg' in img_tag['src']:
			tmp = img_tag['src'].split('/')
			filename = store["name"] + "_" + tmp[len(tmp) - 1]
			if downloadImage(img_tag['src'], filename):
				store["photo"] = [filename]
			break

	return store
