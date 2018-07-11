#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEventsCrawler import IEventsCrawler 
from parser import EParser
from pyquery import PyQuery as pq

class Crawler(IEventsCrawler):
	_URL = ["http://codeforces.com/contests"]
	title = "CodeChef"

	def __init__(self):
		IEventsCrawler.__init__(self, self._URL, EParser, self.title)
		self.run()

	def get_and_parse_page(self):
		for _url in self._URL:
			response = self.get_page(_url)
			if not response:
				continue
			doc = pq(response)
			dataTable = doc("#pageContent > div > div.datatable > div > table > tr:gt(0)")
			if not dataTable or len(dataTable) == 0:
				raise Exception("No Upcoming Event!")
			else:
				_parsed = self.parse_page(dataTable.items())
				self.res.extend(_parsed)

cc = Crawler()
