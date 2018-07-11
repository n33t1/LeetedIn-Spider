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
	def __init__(self, event, **kwars):
		IEParser.__init__(self, event)
		self.run()

	def event_name_helper(self):
		return self.event("td:nth-child(1)").text()

	def event_url_helper(self):
		pass

	def registration_ddl_helper(self):
		td = self.event("td:nth-child(6)").text()
		if re.search(r'Before registration', td) or re.search(r'Until closing', td):
			timestamp = datetime.utcnow()
			reg_ddl = re.findall(r'(\d+):(\d+):(\d+)', td) or re.findall(r'(\d+)\s(.*?)$', td)

		try:
			reg_ddl = reg_ddl[0]
		except Exception:
			print "No registration deadline info!"
			return
		# if the event starts in less than 1 day, CF website will show
		# a live countdown.

		if len(reg_ddl) == 3:
			h, m, s = map(int, list(reg_ddl))
			seconds = h*60*60+m*60+s
		elif len(reg_ddl) == 2:
			seconds = int(reg_ddl[0]) * self.DATE_HASH[reg_ddl[1]] * 24 * 60 * 60
		# shift now
		reg_ddl_dt = timestamp + timedelta(seconds=seconds)
		# formated reg ddl datetime obj
		reg_ddl_dt = reg_ddl_dt.replace(microsecond=0)
		# conver to milli sec 
		millisec = calendar.timegm(reg_ddl_dt.timetuple())
		# # convert back to formated string to verify
		# print(datetime.utcfromtimestamp(float(millisec)))
		return millisec

	def _localize(self, dateinfo, tz=None):
		moscow_tz = timezone('Europe/Moscow')
		moscow_dt = moscow_tz.localize(datetime(dateinfo[2], dateinfo[1], dateinfo[0], dateinfo[3], dateinfo[4], 0))
		return moscow_dt

	def start_date_helper(self):
		start = self.event("td:nth-child(3)")
		href = start("a").attr("href")
		pattern = re.compile(".*?day=(.*?)&month=(.*?)&year=(.*?)&hour=(.*?)&min=(.*?)&sec=(.*?)&p1=(.*?)?$", re.S)
		
		millisec = self.url_to_dt(pattern, href) 
		return millisec

	def event_length_helper(self):
		td = self.event("td:nth-child(4)")
		length = td.text()
		dt = length.split(':')
		if len(dt) == 3: # days
			d, h, m = map(int, list(dt))
			minutes = d*24*60+h*60+m
		elif len(dt) == 2: # hours
			h, m = map(int, list(dt))
			minutes = h*60+m
		return minutes
		
	def event_info_helper(self):
		pass
