#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import re
from pyquery import PyQuery as pq
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar
from pyquery import PyQuery as pq

DATE_HASH = {'days': 1, 'day': 1, 'weeks': 7, 'week': 7}

class ContestInfoParser:
	def __init__(self, events, url=None):
		self.events = events
		self.data = []
		self.url = url
		self.run()
	
	def run(self):
		res = {}
		res['event_title'] = 'CodeForces'
		res['events'] = []
		for tr in self.events.items():
			event_id = tr.attr('data-contestid')
			event_info = EventParser(tr).res
			event_info['url'] = "http://codeforces.com/contests/" + event_id
			res['events'].append(event_info)
		self.data.append(res)

class EventParser:
	def __init__(self, tr):
		self.tr = tr
		self.res = {}
		self.utc_dt, self.millisec = None, None 
		self.run()

	def __repr__(self):
		from pprint import pformat
		return pformat(self.res, indent=4, width=1)
	
	def run(self):
		# parse for contest name
		try:
			self.res['name'] = self.event_name_helper()
			self.res['registrationDeadline'] = self.registration_ddl_helper()
			self.res['startDateTime'] = self.start_date_helper()
			self.res['duratoin'] = self.event_length_helper()
		except Exception as e:
			print e
			print "ContestInfo parse failed!"
		finally:
			return self.res

	def event_name_helper(self):
		return self.tr("td:nth-child(1)").text()

	def registration_ddl_helper(self):
		td = self.tr("td:nth-child(6)")
		reg_ddl_str = td.text()
		if re.search(r'Before registration', reg_ddl_str) or re.search(r'Until closing', reg_ddl_str):
			timestamp = datetime.utcnow()
			reg_ddl = re.findall("(\d+):(\d+):(\d+)", reg_ddl_str) or re.findall("(\d+)\s(.*?)$", reg_ddl_str)
		# if the event starts in less than 1 day, CF website will show
		# a live countdown.
		try:
			reg_ddl = reg_ddl[0]
		except Exception:
			# need to shift time here 
			print "something went wrong!"
			return 
		
		if len(reg_ddl) == 3:
			h, m, s = map(int, list(reg_ddl))
			seconds = h*60*60+m*60+s
		elif len(reg_ddl) == 2:
			seconds = int(reg_ddl[0]) * DATE_HASH[reg_ddl[1]] * 24 * 60 * 60

		# shift now
		reg_ddl_dt = timestamp + timedelta(seconds=seconds)
		# formated reg ddl datetime obj
		reg_ddl_dt = reg_ddl_dt.replace(microsecond=0)
		# conver to milli sec 
		millisec = calendar.timegm(reg_ddl_dt.timetuple())
		# # convert back to formated string to verify
		# print(datetime.utcfromtimestamp(float(registration_ddl_millisec)))
		return millisec

	def start_date_helper(self):
		# parse start date to utc millisec
		start = self.tr("td:nth-child(3)")
		href = start("a").attr("href")
		pattern = re.compile(".*?day=(.*?)&month=(.*?)&year=(.*?)&hour=(.*?)&min=(.*?)&sec=(.*?)&p1=(.*?)?$", re.S)
		items = re.findall(pattern, href)
		date_info = map(int, list(items[0]))
		utc = pytz.utc
		moscow_tz = timezone('Europe/Moscow')
		moscow_dt = moscow_tz.localize(datetime(date_info[2], date_info[1], date_info[0], date_info[3], date_info[4], 0))
		# utc time in "Y-M-D H:M:S Z" format
		self.utc_dt = moscow_dt.astimezone(utc)
		# utc_dt in millisec format
		self.millisec = calendar.timegm(self.utc_dt.timetuple())
		# # convert back to "Y-M-D H:M:S Z" format to verify
		# print(datetime.utcfromtimestamp(float(d)))
		return self.millisec
	
	def event_length_helper(self):
		td = self.tr("td:nth-child(4)")
		length = td.text()
		dt = length.split(':')
		if len(dt) == 3: # days
			d, h, m = map(int, list(dt))
			minutes = d*24*60+h*60+m
		elif len(dt) == 2: # hours
			h, m = map(int, list(dt))
			minutes = h*60+m
		return minutes