#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEventsCrawlerDP import IEventsCrawlerDP 
from parser import EParser 
from pyquery import PyQuery as pq

class Crawler(IEventsCrawlerDP):
	_URL = ['https://www.topcoder.com/challenges?bucket=ongoing', 'https://www.topcoder.com/challenges?bucket=openForRegistration']
	TITLE = "LeetCode"
	XPATH = ['//*[@id="challengeFilterContainer"]/div[3]/div[2]/div/div[1]/h1','//*[@id="challengeFilterContainer"]/div[3]/div[2]/div/div[1]/h1']

	def __init__(self):
		IEventsCrawlerDP.__init__(self, self._URL, EParser, self.TITLE)
		self.run()

	def get_and_parse_page(self):
		html = open('challengeFilterContainer.html', 'r').read()
		doc = pq(html)
		#challengeFilterContainer > div:nth-child(3) > div._3p0GeZ > div > div:nth-child(2)
		events = doc('#challengeFilterContainer > div:nth-child(3) > div._3p0GeZ > div > div:gt(1)')
		# print len(events)
		_parsed = self.parse_page(events.items()) 
		
		# challengeFilterContainer = doc('#challengeFilterContainer').outerHtml().encode('utf-8')
		# self.export_html(challengeFilterContainer, 'challengeFilterContainer')
		# events = challengeFilterContainer('div')
		# print events
		# for i in range(len(self._URL[:1])):
		# 	_url = self._URL[i]
		# 	_xpath = self.XPATH[i]
		# 	html = self.get_page(_url, _xpath)
		# 	print type(html)
		# 	self.export_html(html, 'topcoder')

			# doc = pq(html)
			# print doc
			# events = doc('#challengeFilterContainer > div:nth-child(3) > div._3p0GeZ > div > div')
			# print response
			# if not response:
			# 	continue
			# _parsed = self.parse_page(response, _url) 
			# self.res.extend(_parsed)
		
		# self.driver.close()

cc = Crawler()
