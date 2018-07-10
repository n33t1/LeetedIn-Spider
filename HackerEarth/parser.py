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
from pyquery import PyQuery as pq
from pprint import pprint
 
class EParser(IEParser):
	SIX_MONTH_IN_MINUTES = 262800
	def __init__(self, event, url=None):
		IEParser.__init__(self, event, url)
		self.start_milli, self.end_milli = None, None
		# print self.event
		self.run()

	def event_name_helper(self):
		return self.event['summary']

	def event_url_helper(self):
		return self.event['location']

	def registration_ddl_helper(self):
		pass

	def start_date_helper(self):
		ts = self.event['start']['dateTime']
		self.start_milli = self.IOS_to_dt(ts)
		return self.start_milli
	
	def end_date_helper(self):
		ts = self.event['end']['dateTime']
		self.end_milli = self.IOS_to_dt(ts)
		return self.end_milli

	def event_length_helper(self):
		if not self.start_milli:
			self.start_date_helper()

		if not self.end_milli:
			self.end_date_helper()
			
		minutes = self.calc_event_length(self.start_milli, self.end_milli)
		return minutes
		
	def event_info_helper(self):
		pass
