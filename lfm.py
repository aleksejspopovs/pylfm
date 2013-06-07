#!/usr/bin/env python3
import io
import requests
from lxml import etree

API_ROOT = 'http://ws.audioscrobbler.com/2.0/'
API_USERAGENT = 'Popovs\' Analyzer 1.0'
API_PER_PAGE = 1000

def try_really_hard(what):
	while True:
		try:
			return what()
		except:
			pass

def magically_parse_bs_xml(text):
	# i have no fucking idea either.
	magical_parser = etree.XMLParser(encoding='utf-8', recover=True)
	return etree.parse(io.BytesIO(bytes(text, 'UTF-8')), magical_parser).getroot()

class LastFM:
	def __init__(self, api_key):
		self.api_key = api_key
		self.session = requests.Session()
		self.session.params = {'api_key': self.api_key}
		self.session.headers = {'User-Agent': API_USERAGENT}

	def get_user_artists(self, username):
		def parse_artists(data):
			res = []
			for a in data[0].iter('artist'):
				res.append((a.find('name').text, int(a.find('playcount').text)))
			return res

		def get_page(page):
			r = self.session.get(API_ROOT, params={
				'method': 'user.gettopartists',
				'period': 'overall',
				'user': username,
				'limit': API_PER_PAGE,
				'page': page
			})
			xml = magically_parse_bs_xml(r.text)
			assert(xml.get('status') == 'ok')
			return xml

		first = get_page(1)

		res = parse_artists(first)

		for pg in range(2, int(first[0].get('totalPages')) + 1):
			res += parse_artists(get_page(pg))

		return res

	def get_group_members(self, groupname):
		def parse_members(data):
			res = []
			for a in data[0].iter('user'):
				res.append(a.find('name').text)
			return res

		def get_page(page):
			r = self.session.get(API_ROOT, params={
				'method': 'group.getmembers',
				'group': groupname,
				'limit': API_PER_PAGE,
				'page': page
			})
			xml = magically_parse_bs_xml(r.text)
			assert(xml.get('status') == 'ok')
			return xml

		first = get_page(1)

		res = parse_members(first)

		for pg in range(2, int(first[0].get('totalPages')) + 1):
			res += parse_members(get_page(pg))

		return res

	def get_user_friends(self, username):
		def parse_friends(data):
			res = []
			for a in data[0].iter('user'):
				res.append(a.find('name').text)
			return res

		def get_page(page):
			r = self.session.get(API_ROOT, params={
				'method': 'user.getfriends',
				'user': username,
				'limit': API_PER_PAGE,
				'page': page
			})
			xml = magically_parse_bs_xml(r.text)
			assert(xml.get('status') == 'ok')
			return xml

		first = get_page(1)

		res = parse_friends(first)

		for pg in range(2, int(first[0].get('totalPages')) + 1):
			res += parse_friends(get_page(pg))

		return res

	def get_user_info(self, username):
		def get_page():
			r = self.session.get(API_ROOT, params={
				'method': 'user.getinfo',
				'user': username
			})
			xml = magically_parse_bs_xml(r.text)
			assert(xml.get('status') == 'ok')
			return xml

		page = get_page()
		res = {}
		for k in page[0].getchildren():
			res[k.tag] = k.text
		return res
