#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import re
from pyquery import PyQuery as pq
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar
from pprint import pprint

DATE_HASH = {'days': 1, 'day': 1, 'weeks': 7, 'week': 7}

class ContestInfoParser:
	def __init__(self, events):
		self.events = events
		self.data = []
		self.run()
	
	def run(self):
		for e in self.events:
			res = {}
			res['events'] = EventParser(e['events']).res
			res['event_title'] = e['event_title']
			if 'event_info' in e.keys():
				res['event_info'] = e['event_info']
			self.data.append(res)

class EventParser:
	def __init__(self, events):
		self.events = events
		self.res = []
		self.reg_ddl_millisec = None 
		self.run()

	# def __repr__(self):
	# 	from pprint import pformat
	# 	return pformat(self.res, indent=4, width=1)
	
	def run(self):	
		try:
			for e in self.events:
				temp = {}
				temp['url'] = 'https://code.google.com/codejam/'
				if e['name'] == 'Registration':
					# duration is in minutes
					startDateTime, duration = e['startDateTime'], e['duration']
					startDateTime = datetime.strptime(startDateTime.split('+')[0], '%Y-%m-%dT%H:%M:%S')
					utc_dt = startDateTime + timedelta(minutes=duration)
					self.reg_ddl_millisec = calendar.timegm(utc_dt.timetuple())					
				else:
					temp['name'] = e['name']
					temp['startDateTime'] = self.strToMillisec(e['startDateTime'])
					temp['duration'] = int(e['duration'])

					if e['name'] == 'Practice Session':
						temp['prerequisite'] = ""
					else:
						temp['prerequisite'] = "You have to pass previous rounds!"

					if e['name'] == 'Qualification Round':
						temp['registrationDeadline'] = self.reg_ddl_millisec
					else:
						temp['registrationDeadline'] = temp['startDateTime']
				self.res.append(temp)
		except Exception as e:
			print e
			print "ContestInfo parse failed!"
		finally:
			return self.res
	
	def strToMillisec(self, dt):
		dt = datetime.strptime(dt.split('+')[0], '%Y-%m-%dT%H:%M:%S')
		millisec = calendar.timegm(dt.timetuple())
		return millisec

	
	def event_name_helper(self):
		pass

	def registration_ddl_helper(self):
		pass

	def start_date_helper(self):
		pass
	
	def event_length_helper(self):
		pass