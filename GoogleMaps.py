# -*- coding: utf-8 -*-

import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import json

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

def getGeocodePage(addr):
	url = "https://www.geocoding.jp/api/?q=" + addr
	page = requests.get(url)
	if page.status_code != 200:
		return None
	return page.text
		
#とにかく一番近い駅を探す
def getStation(addr):
	page = getGeocodePage(addr)
	if page == None:
		return None
	bs = BeautifulSoup(page, "xml")
	if bs.find('error'):
		page = getGeocodePage(addr)
		if page == None:
			return None
		bs = BeautifulSoup(page, "xml")
		if bs.find('error'):
			return None

	lat = bs.find("lat").text
	lng = bs.find("lng").text

	header = {
		'User-Agent': 'CreateRestaurantsSummarySite (Mac)'
	}
	res = requests.get('https://station.ic731.net/api/nearest?lon={lng}&lat={lat}'.format(lng=lng, lat=lat), headers=header)
	if (res.status_code != 200):
		return None
	
	d = json.loads(res.text)
	station_data = d['data'][0]
	return station_data['station_name'] + '駅'

def getInfo(url):
	options = Options()
	options.add_argument('--headless')
	driver = webdriver.Chrome(options=options)

	try:
		driver.get(url)
		WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located)	

		bs = BeautifulSoup(driver.page_source, 'html.parser')
	finally:
		driver.quit()

	store = {}

	#店舗名
	if bs.find(class_='tAiQdd') == None:
		return None
	span_tag = bs.find(class_='tAiQdd').find('h1').find('span')
	store["name"] = span_tag.text.strip()
		
	#ジャンル
	bt_tag = bs.find(class_='skqShb').find(class_='DkEaL u6ijk')
	store["genre"] = [bt_tag.text.strip()]
	
	#所在地
	store["addr"] = bs.find(class_='Io6YTe fontBodyMedium').text.strip()
	
	#写真
	store["photo"] = [];
	img_tag = bs.find(class_='RZ66Rb FgCUCc').find('img')
	tmp = img_tag['src'].split('/')
	filename = store["name"] + "_" + tmp[len(tmp) - 1]
	if downloadImage(img_tag['src'], filename):
		store["photo"].append(filename)

	#最寄
	station = getStation(store["addr"])
	if station != None:
		store["station"] = station
	
	return store
