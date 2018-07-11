#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEventsCrawler import IEventsCrawler 
from parser import EParser 
from pyquery import PyQuery as pq

class Crawler(IEventsCrawler):
	_URL = ['https://www.codechef.com/contests']
	title = "CodeChef"

	def __init__(self):
		IEventsCrawler.__init__(self, EParser)
		self.run()

	def get_and_parse_page(self):
		for _url in self._URL:
			response = self.get_page(_url)
			if not response:
				continue
			# print response
			doc = pq(response)
			events = doc('selector')
			_parsed = self.parse_page(events.items(), self.title)
			self.res.extend(_parsed)

cc = Crawler()
