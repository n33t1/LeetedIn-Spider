#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import traceback
import re
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar

class IEParser:
	SIX_MONTH_IN_MINUTES = 262800
	DATE_HASH = {'days': 1, 'day': 1, 'weeks': 7, 'week': 7}

	def __init__(self, event, url=None, event_info=None):
		self.event = event
		self.url = url
		self.event_info = event_info
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
			self.res['endDateTime'] = self.end_date_helper()
		except Exception as e:
			print "IEParser parse failed! Error: {}".format(repr(e))
			traceback.print_exc()
			raise
		else:
			return self.res 
			
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

	def end_date_helper(self):
		return self.res['startDateTime'] + self.res['duratoin'] * 60

	def calc_event_length(self, start_milli=None, end_milli=None):
		minutes = (end_milli - start_milli) / 60
		if minutes > self.SIX_MONTH_IN_MINUTES:
			raise Exception('Event Not Valid! Eventname: ' + self.res['name'])
		else:
			return minutes
	
	def event_info_helper(self):
		raise NotImplementedError
	
	def _localize(self, dt, tz=None):
		utc = pytz.utc
		local_tz = timezone('Asia/Calcutta')
		local_dt = local_tz.localize(dt)
		utc_dt = local_dt.astimezone(utc)
		return utc_dt

	def url_to_dt(self, pattern, href):
		items = re.findall(pattern, href)
		date_info = map(int, list(items[0]))
		utc_dt = self._localize(date_info)
		# print local_dt
		# utc time in "Y-M-D H:M:S Z" format
		# utc_dt in millisec format
		millisec = calendar.timegm(utc_dt.timetuple())
		# # convert back to "Y-M-D H:M:S Z" format to verify
		# print(datetime.utcfromtimestamp(float(millisec)))
		return millisec

	def IOS_to_dt(self, ios):
		dt = datetime.strptime(ios[:-6], '%Y-%m-%dT%H:%M:%S')
		utc_dt = self._localize(dt)
		millisec = calendar.timegm(utc_dt.timetuple())	
		return millisec
	
	def dt_to_IOS(self, millisec):
		return datetime.utcfromtimestamp(float(millisec))