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
	def __init__(self, event, url=None, info=None):
		IEParser.__init__(self, event, url, info)
		# print "self.event_info", info
		# print self.event
		if self.event['name'] == 'Registration':
			raise Exception('Invalid event!')
		self.run()

	def event_name_helper(self):
		return self.event['name']

	def event_url_helper(self):
		return self.url

	def registration_ddl_helper(self):
		pass

	def _localize(self, dt, tz=None):
		return dt

	def start_date_helper(self):
		dt = self.event['startDateTime']
		millisec = self.IOS_to_dt(dt)
		
		if self.event['name'] == 'Registration':
			t_0 = dt
			delta = self.event_length_helper()
			t_1 = t_0 + delta * 60
			self.reg_ddl = t_1
		return millisec
		
	def event_length_helper(self):
		return int(self.event['duration'])
		
	def event_info_helper(self):
		if self.event_info:
			return self.event_info
		elif not self.event['name'] == 'Practice Session' \
			and not self.event['name'] == 'Qualification Round':
			return "You have to pass previous rounds!"


