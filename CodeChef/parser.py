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

	# <td>JULY18</td>
	# <td><a href="/JULY18">July Challenge 2018</a></td>
	# <td data-starttime="2018-07-06T15:00:00+05:30" class="start_date">06 Jul 2018 <br /> 15:00:00</td>
	# <td data-endtime="2018-07-16T15:00:00+05:30" class="end_date">16 Jul 2018 <br /> 15:00:00</td>

	def event_name_helper(self):
		return self.event('tr td:nth-child(2)').text()

	def event_url_helper(self):
		base_url = 'https://www.codechef.com/' 
		code = self.event('tr td:nth-child(1)').text()
		return base_url + code
	
	# 2015-11-05T00:00:00+05:30
	def end_date_helper(self):
		temp = self.event('tr td:nth-child(4)').attr('data-endtime')
		if re.search(r'\d+:\d+\d+\+\d+:\d+', temp):
			end_dt = datetime.strptime(temp[:-6], '%Y-%m-%dT%H:%M:%S')
			hours, minutes = map(int, re.findall(r'\+(\d+):(\d+)', temp)[0])
			utc_dt = end_dt + timedelta(hours=hours, minutes=minutes)
			end_millisec = calendar.timegm(utc_dt.timetuple())
			self.end_milli = end_millisec
			return end_millisec
		elif re.search(r'\d+:\d+\d+\-\d+:\d+', temp):
			end_dt = datetime.strptime(temp[:-6], '%Y-%m-%dT%H:%M:%S')
			hours, minutes = map(int, re.findall(r'\+(\d+):(\d+)', temp)[0])
			utc_dt = end_dt - timedelta(hours=hours, minutes=minutes)
			end_millisec = calendar.timegm(utc_dt.timetuple())
			self.end_milli = end_millisec
			return end_millisec

	def registration_ddl_helper(self):
		pass

	def start_date_helper(self):
		temp = self.event('tr td:nth-child(3)').attr('data-starttime')
		if re.search(r'\d+:\d+\d+\+\d+:\d+', temp):
			start_dt = datetime.strptime(temp[:-6], '%Y-%m-%dT%H:%M:%S')
			hours, minutes = map(int, re.findall(r'\+(\d+):(\d+)', temp)[0])
			utc_dt = start_dt + timedelta(hours=hours, minutes=minutes)
			start_millisec = calendar.timegm(utc_dt.timetuple())	
			self.start_milli= start_millisec
			return start_millisec
		elif re.search(r'\d+:\d+\d+\-\d+:\d+', temp):
			start_dt = datetime.strptime(temp[:-6], '%Y-%m-%dT%H:%M:%S')
			hours, minutes = map(int, re.findall(r'\+(\d+):(\d+)', temp)[0])
			utc_dt = start_dt - timedelta(hours=hours, minutes=minutes)
			start_millisec = calendar.timegm(utc_dt.timetuple())	
			self.start_milli = start_millisec
			return start_millisec

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
