#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEParser import IEParser 

from pyquery import PyQuery as pq
from pprint import pprint
 
class EParser(IEParser):
	def __init__(self, event, **kwargs):
		IEParser.__init__(self, event)
		self.start_milli, self.end_milli = None, None
		self.run()

	def event_name_helper(self):
		return self.event('tr td:nth-child(2)').text()

	def event_url_helper(self):
		base_url = 'https://www.codechef.com/' 
		code = self.event('tr td:nth-child(1)').text()
		return base_url + code
	
	def end_date_helper(self):
		ios = self.event('tr td:nth-child(4)').attr('data-endtime')
		self.end_milli = self.IOS_to_dt(ios) 
		return self.end_milli

	def registration_ddl_helper(self):
		pass

	def start_date_helper(self):
		ios = self.event('tr td:nth-child(3)').attr('data-starttime')
		self.start_milli = self.IOS_to_dt(ios)
		return self.start_milli

	def event_length_helper(self):
		if not self.start_milli:
			self.start_date_helper()
		if not self.end_milli:
			self.end_date_helper()

		if self.start_milli and self.end_milli:
			minutes = (self.end_milli - self.start_milli) / 60
			if minutes > self.SIX_MONTH_IN_MINUTES:
				raise Exception('Event Not Valid! Eventname: ' + self.res['name'])
			else:
				return minutes
		
	def event_info_helper(self):
		pass
