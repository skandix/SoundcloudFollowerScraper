#!/usr/bin/python
# -*- coding: utf-8 -*-
from pprint import pprint
import jsonpickle
import requests
import urllib
import re
import os

os.path.exists("scrape.sh") and os.remove("scrape.sh")

cli_id = "02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea"
artist = [ ]
sscrape = "soundscrape -f -n 100 "

def get_sc_uid(username):
	requid = requests.get('http://api.soundcloud.com/resolve.json?url=http://soundcloud.com/%s&client_id=%s' % (username, cli_id), stream=True)
	uid = requid.text.replace(',', '').replace('kind', '').replace('"', '')
	uinfo = uid.split(":")
	
	return uinfo[1]

def follower_scrape():
	url =  'https://api.soundcloud.com/users/%s/followings?client_id=%s&limit=1000' % (get_sc_uid("bendyr"), cli_id)
	spoon = urllib.urlopen(url)
	frozen = jsonpickle.encode(spoon)

	find_username = re.compile(ur'"username\\":\\"[a-zA-Z0-9 ]{3,}')
	regex_magic = re.findall(find_username, frozen)
	
	for i in regex_magic:
		artist.append(i.replace('"', "").replace('username', "").replace('\:', "").replace('\\', ""))
	
	pprint(artist)
	print "Count:", len(artist)

def soundscrape_generate():

	file = open('scrape.sh', "wb+")
	for j in artist:
		dmp = sscrape + j
		file.write(dmp)
		file.write("\n")


follower_scrape()
# if you want to generate a bash script to download songs from all the artist you are following
# soundscrape_generate()
