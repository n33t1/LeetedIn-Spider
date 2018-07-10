#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import traceback

class IEParser:
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
	
	def end_date_helper(self):
		return self.res['startDateTime'] + self.res['duratoin'] * 60

	def event_length_helper(self):
		raise NotImplementedError
	
	def event_info_helper(self):
		raise NotImplementedError