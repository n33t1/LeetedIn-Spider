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
	def __init__(self, events, url):
		self.events = events
		self.url = url
		self.data = []
		self.run()
	
	def run(self):
		for ee in self.events:
			res_events = {}
			res_events['event_title'] = ee['event_title']
			if 'event_info' in ee.keys():
				res_events['event_info'] = ee['event_info']
			res_events['events'] = []
		
			for e in ee['events']:
				res_events['events'].append(EventParser(e, self.url).res)
			
			self.data.append(res_events)

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
			self.res['url'] = self.url
			if self.event['name'] == 'Registration':
				# duration is in minutes
				startDateTime, duration = self.event['startDateTime'], self.event['duration']
				startDateTime = datetime.strptime(startDateTime.split('+')[0], '%Y-%m-%dT%H:%M:%S')
				utc_dt = startDateTime + timedelta(minutes=duration)
				self.reg_ddl_millisec = calendar.timegm(utc_dt.timetuple())					
			else:
				self.res['name'] = self.event['name']
				self.res['startDateTime'] = self.strToMillisec(self.event['startDateTime'])
				self.res['duration'] = int(self.event['duration'])

				if self.event['name'] == 'Practice Session':
					self.res['prerequisite'] = ""
				else:
					self.res['prerequisite'] = "You have to pass previous rounds!"

				if self.event['name'] == 'Qualification Round':
					self.res['registrationDeadline'] = self.reg_ddl_millisec
				else:
					self.res['registrationDeadline'] = self.res['startDateTime']
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