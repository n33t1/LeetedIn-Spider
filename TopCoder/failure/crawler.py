#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-
#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEventsCrawler import IEventsCrawler 
from parser import EParser 
import xml.etree.ElementTree as ET
import requests
from requests.exceptions import RequestException

class Crawler(IEventsCrawler):
	_URL = ['http://feeds.topcoder.com/challenges/feed?list=active&contestType=all']
	TITLE = "TopCoder"

	def __init__(self):
		IEventsCrawler.__init__(self, self._URL, EParser, self.TITLE)
		self.run()

	def get_and_parse_page(self):
		for _url in self._URL:
			response = self.get_page(_url).encode('utf-8')
			if not response:
				continue
			# print response
			# response = response.encode('utf-8')
			# print response
			root = ET.fromstring(response)
			events = root.findall('.//item')
			# print events
			# root = tree.getroot()
			# events = root.finall('item')
			# print events
			# for e in events:
			# 	s = e.find('./title')
			# 	print ET.tostring(sys).decode()
			# events = selector.xpath('//div')
			# print "events"
			# print events
			_parsed = self.parse_page(events)
			self.res.extend(_parsed)

cc = Crawler()
