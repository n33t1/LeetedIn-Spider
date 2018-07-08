#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar
from pprint import pprint

DATE_HASH = {'days': 1, 'day': 1, 'weeks': 7, 'week': 7}

class ContestInfoParser:
	def __init__(self, events, url):
		self.events = events
		self.url = url
		self.data = []
		self.run()
	
	def run(self):
		for e in self.events:
			e = e.decode('utf-8')
			e = str(e)

			res = {}
			res['events'] = EventParser(e, self.url).res
			res['event_title'] = "Leetcode Weekly Contest"
			self.data.append(res)

class EventParser:
	def __init__(self, event, url):
		self.event = event
		self.url = url
		self.res = {}
		self.reg_ddl_millisec = None 
		self.run()

	# def __repr__(self):
	# 	from pprint import pformat
	# 	return pformat(self.res, indent=4, width=1)
	
	def run(self):	
		try:
			self.res['name'] = self.event_name_helper()
			self.res['registrationDeadline'] = self.start_date_helper()
			self.res['startDateTime'] = self.res['registrationDeadline']
			self.res['duratoin'] = self.duration
		except Exception as e:
			print e
			print "ContestInfo parse failed!"
		finally:
			return self.res

	def event_name_helper(self):
		dt = re.findall('Weekly\sContest\s\d+', self.event)
		try:
			res = dt[0]
			return 'LeetCode ' + res
		except Exception as e:
			print "Cannot parse event name! Error: " + e

	def start_date_helper(self):
		pattern = re.compile("(\w+\s\d+\,\s\d+.*?)\-\s(\d+:\d+.*\w+)", re.S)
		dt = re.findall(pattern, self.event)
		try:
			dt = dt[0]
			return self.strToMillisec(dt)
		except Exception as e:
			print "Cannot parse registration deadline! Error: " + e

	def strToMillisec(self, dt):
		def timeHelper(time):
			time = re.findall('(\d+):(\d+).*(\w+\w+)', time)
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

	def registration_ddl_helper(self):
		pass
	
	def event_length_helper(self):
		pass