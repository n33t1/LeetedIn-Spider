#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import re
from lxml import etree
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar

class AbstractEventsParser:
	def __init__(self, eParser, events, title, url=None):
		self.data = []
		self.run(eParser, title, events, url)
	
	def __repr__(self):
		print "Events parsed: "
		from pprint import pformat
		return pformat(self.data, indent=4, width=1)

	def run(self, eParser, title, events, url):
		info = {}
		info['event_title'] = "AtCoder"
		info['events'] = []

		for event in events:
			info['events'].append(eParser(event).res)
		self.data.append(info)

class AbstractEParser:
	DATE_HASH = {'days': 1, 'day': 1, 'weeks': 7, 'week': 7}

	def __init__(self, event, url=None):
		self.event = event
		self.url = url
		self.res = {}

	def __repr__(self):
		from pprint import pformat
		return pformat(self.res, indent=4, width=1)
	
	def run(self):	
		try:
			self.res['addtionalInfo'] = self.event_info_helper()
			self.res['name'] = self.event_name_helper()
			self.res['url'] = self.event_url_helper()
			self.res['startDateTime'] = self.start_date_helper()
			self.res['registrationDeadline'] = self.registration_ddl_helper() or self.res['startDateTime']
			self.res['duratoin'] = self.event_length_helper()
		except Exception as e:
			print 'ContestInfo parse failed! Error: {}'.format(repr(e))
		finally:
			return self.res
	
	# def strToMillisec(self, dt):
	# 	dt = datetime.strptime(dt.split('+')[0], '%Y-%m-%dT%H:%M:%S')
	# 	millisec = calendar.timegm(dt.timetuple())
	# 	return millisec

	def event_name_helper(self):
		raise NotImplementedError

	def event_url_helper(self):
		raise NotImplementedError

	def registration_ddl_helper(self):
		raise NotImplementedError

	def start_date_helper(self):
		raise NotImplementedError

	def event_length_helper(self):
		raise NotImplementedError
	
	def event_info_helper(self):
		raise NotImplementedError