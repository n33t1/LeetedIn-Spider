#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEventsCrawler import IEventsCrawler 
from parser import EParser 
from pyquery import PyQuery as pq

class Crawler(IEventsCrawler):
	_URL = ["https://code.google.com/codejam/", "https://code.google.com/codejam/kickstart/"]

	def __init__(self):
		IEventsCrawler.__init__(self, EParser)
		self.run()
	
	def get_response(self, response):
		return response.json()

	def get_and_parse_page(self):
		for _url in self._URL:
			data_api = _url + 'schedule?data=1'
			_json = self.get_page(data_api)['schedules']
			if not _json:
				raise Exception("No Upcoming Event!")
			else:		
				for events in _json:
					title, info = events['event_title'], None
					if 'event_info' in events.keys():
						info = events['event_info']
					_parsed = self.parse_page(events['events'], title, _url, info)
					self.res.extend(_parsed)

cc = Crawler()
