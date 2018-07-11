#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEventsCrawler import IEventsCrawler 
from parser import EParser
from lxml import etree

class Crawler(IEventsCrawler):
	_URL = ["https://atcoder.jp/contest"]
	title = "AtCoder"

	def __init__(self):
		IEventsCrawler.__init__(self, EParser)
		self.run()

	def get_and_parse_page(self):
		for _url in self._URL:
			html = self.get_page(_url)
			if not html:
				continue
			selector = etree.HTML(html)
			active_contests = selector.xpath('//*[@id="main-div"]/div/div/div[2]/h3[1]/parent::*/div[1]/table/tbody/tr')
			upcoming_contests = selector.xpath('//*[@id="main-div"]/div/div/div[2]/h3[2]/parent::*/div[2]/table/tbody/tr')

			contests = active_contests + upcoming_contests
			
			if not contests:
				raise Exception("No Upcoming Event!")
			else:		
				_parsed = self.parse_page(contests, self.title)
				self.res.extend(_parsed)

cc = Crawler()
