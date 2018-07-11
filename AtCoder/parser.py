#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEParser import IEParser 

import re
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar
from lxml import etree
from pprint import pprint
 
class EParser(IEParser):
	def __init__(self, event, **kwargs):
		IEParser.__init__(self, event)

		if self.event.xpath('./td[2]/a/text()')[0] == 'practice contest':
			raise Exception('Invalid event!')
		
		self.event = self.event.xpath('./td')
		self.run()

	def event_name_helper(self):
		name = self.event[1].xpath('./a/text()')[0]
		return name

	def event_url_helper(self):
		url = self.event[1].xpath('./a/@href')[0]
		return url

	def registration_ddl_helper(self):
		pass

	def _localize(self, date_info, tz=None):
		tokyo_tz = timezone('Asia/Tokyo')
		tokyo_dt = tokyo_tz.localize(datetime(date_info[0], date_info[1], date_info[2], date_info[3], date_info[4], 0))
		return tokyo_dt

	def start_date_helper(self):
		href = self.event[0].xpath('./a/@href')[0]
		pattern = re.compile(r'iso=(\d\d\d\d)(\d\d)(\d\d)T(\d\d)(\d\d)&p1', re.S)

		millisec = self.url_to_dt(pattern, href)
		return millisec

	def event_length_helper(self):
		length = self.event[2].xpath('./text()')[0]
		try:
			length = length.decode('utf-8')
			dt = length.split(':')
			if len(dt) == 3: # days
				d, h, m = map(int, list(dt))
				minutes = d*24*60+h*60+m
			elif len(dt) == 2: # hours
				h, m = map(int, list(dt))
				minutes = h*60+m
		except Exception:
			minutes = 'infinity'
		finally:
			return minutes
		
	def event_info_helper(self):
		res = []
		info = self.event[3].xpath('./table/tr')
		for tr in info:
			td = tr.xpath('./td/text() | ./td/b/text()')
			try:
				td[1] = td[1].decode('utf-8')
			except Exception:
				td[1] = 'None'
			res.append(td[0] + ': ' + td[1])
		return ' ; '.join(res)
