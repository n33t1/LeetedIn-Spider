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
from pprint import pprint

class EParser(IEParser):
	def __init__(self, event, **kwargs):
		event = event.decode('utf-8')
		event = str(event)
		IEParser.__init__(self, event)
		self.url = kwargs['url']
		self.duration = None
		self.run()

	def event_name_helper(self):
		dt = re.findall(r'Weekly\sContest\s\d+', self.event)
		try:
			res = dt[0]
			return 'LeetCode ' + res
		except Exception as e:
			print "Cannot parse event name! Error: " + e

	def event_url_helper(self):
		return self.url
	
	def registration_ddl_helper(self):
		pass

	def start_date_helper(self):
		pattern = re.compile(r'(\w+\s\d+\,\s\d+.*?)\-\s(\d+:\d+.*\w+)', re.S)
		dt = re.findall(pattern, self.event)
		try:
			dt = dt[0]
			return self.strToMillisec(dt)
		except Exception as e:
			print "Cannot parse registration deadline! Error: " + e

	def strToMillisec(self, dt):
		def timeHelper(time):
			time = re.findall(r'(\d+):(\d+).*(\w+\w+)', time)
			time = time[0]
			hour, minutes, locale = int(time[0]), int(time[1]), time[2]
			if locale == "PM":
				hour += 12
				if hour == 24:
					hour = 0
			return hour, minutes

		start_dt, end_time = dt[0], dt[1]
		date, time = start_dt.split('@')
		hour, minutes = timeHelper(time)
		end_hour, end_minutes = timeHelper(end_time)
		dt = datetime.strptime(date, '%b %d, %Y ')
		dt = dt.replace(hour=hour, minute=minutes)
		end_dt = dt.replace(hour=end_hour, minute=end_minutes)
		millisec = calendar.timegm(dt.timetuple())
		end_millisec = calendar.timegm(end_dt.timetuple())
		delta = end_millisec - millisec
		delta = delta // 60
		self.duration = delta
		return millisec

	def event_length_helper(self):
		return self.duration
		
	def event_info_helper(self):
		pass
