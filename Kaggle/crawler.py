#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEventsCrawlerDP import IEventsCrawlerDP  
from parser import EParser 

class Crawler(IEventsCrawlerDP):
	_URL = ['YOUR URL']
	title = "YOUR TITLE"
	XPATH = 'YOUR XPATH'

	def __init__(self):
		IEventsCrawlerDP.__init__(self, EParser)
		self.run()

	def decode_page(self, element):
		return element.text

	def get_and_parse_page(self):
		for _url in self._URL:
			response = self.get_page(_url, self.XPATH) 
			if not response:
				continue
			_parsed = self.parse_page([response], self.title, _url) 
			self.res.extend(_parsed)
		
		self.driver.close()

cc = Crawler()
