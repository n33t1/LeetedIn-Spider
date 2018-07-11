#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEventsCrawler import IEventsCrawler 
from parser import EParser

import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq

class HackerrankCrawler(IEventsCrawler):
	_URL = ['https://www.hackerrank.com/rest/contests/upcoming?offset=0&limit=10&contest_slug=active']
	title = 'Hackerrank'

	def __init__(self):
		IEventsCrawler.__init__(self, EParser)
		self.run()

	def get_response(self, response):
		return response.json()

	def get_and_parse_page(self):
		for _url in self._URL:
			_json = self.get_page(_url)['models']
			if not _json:
				raise Exception("No Upcoming Event!")
			else:		
				_parsed = self.parse_page(_json, self.title)
				self.res.extend(_parsed)

hr = HackerrankCrawler()
