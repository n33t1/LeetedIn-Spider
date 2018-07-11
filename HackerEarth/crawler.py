'https://clients6.google.com/calendar/v3/calendars/hackerearth.com_73f0o8kl62rb5v1htv19p607e4@group.calendar.google.com/events?calendarId=hackerearth.com_73f0o8kl62rb5v1htv19p607e4%40group.calendar.google.com&singleEvents=true&timeZone=Asia%2FCalcutta&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin=2018-07-01T00%3A00%3A00%2B05%3A30&timeMax=2018-08-05T00%3A00%3A00%2B05%3A30&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs'

#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEventsCrawler import IEventsCrawler 
from parser import EParser 
from pyquery import PyQuery as pq
import requests
import json    
from requests.exceptions import RequestException

class Crawler(IEventsCrawler):
	_URL = ['https://clients6.google.com/calendar/v3/calendars/hackerearth.com_73f0o8kl62rb5v1htv19p607e4@group.calendar.google.com/events?calendarId=hackerearth.com_73f0o8kl62rb5v1htv19p607e4%40group.calendar.google.com&singleEvents=true&timeZone=Asia%2FCalcutta&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin=2018-07-01T00%3A00%3A00%2B05%3A30&timeMax=2018-08-05T00%3A00%3A00%2B05%3A30&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs']
	title = "CodeChef"

	def __init__(self):
		IEventsCrawler.__init__(self, EParser)
		self.run()

	def get_and_parse_page(self):
		for _url in self._URL:
			response = self.get_page(_url)
			if not response:
				continue
			_json = json.loads(response)['items']
			_parsed = self.parse_page(_json, self.title)
			self.res.extend(_parsed)

cc = Crawler()
