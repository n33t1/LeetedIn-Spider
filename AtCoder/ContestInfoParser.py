#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import re
from lxml import etree
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar
from pprint import pprint

DATE_HASH = {'days': 1, 'day': 1, 'weeks': 7, 'week': 7}

class ContestInfoParser:
	def __init__(self, events, url=None):
		self.events = events
		self.url = url
		self.data = []
		self.run()
	
	def run(self):
		res_events = {}
		res_events['event_title'] = "AtCoder"
		res_events['events'] = []

		for e in self.events:
			if e.xpath('./td[2]/a/text()')[0] == 'practice contest':
				continue
			
			event = e.xpath('./td')
			res_events['events'].append(EventParser(event).res)
		self.data.append(res_events)

class EventParser:
	def __init__(self, event, url=None):
		self.event = event
		self.url = url
		self.res = {}
		self.run()

	# def __repr__(self):
	# 	from pprint import pformat
	# 	return pformat(self.res, indent=4, width=1)
	
	def run(self):	
		try:
			self.res['addtionalInfo'] = self.event_info_helper()
			self.res['name'] = self.event_name_helper()
			self.res['url'] = self.event_url_helper()
			self.res['startDateTime'] = self.start_date_helper()
			self.res['registrationDeadline'] = self.res['startDateTime']
			self.res['duratoin'] = self.event_length_helper()
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
		name = self.event[1].xpath('./a/text()')[0]
		return name

	def event_url_helper(self):
		url = self.event[1].xpath('./a/@href')[0]
		return url

	def registration_ddl_helper(self):
		pass

	def start_date_helper(self):
		# parse start date to utc millisec
		href = self.event[0].xpath('./a/@href')[0]
		pattern = re.compile("iso=(\d\d\d\d)(\d\d)(\d\d)T(\d\d)(\d\d)&p1", re.S)
		items = re.findall(pattern, href)
		date_info = map(int, list(items[0]))
		utc = pytz.utc
		tokyo_tz = timezone('Asia/Tokyo')
		tokyo_dt = tokyo_tz.localize(datetime(date_info[0], date_info[1], date_info[2], date_info[3], date_info[4], 0))
		# # utc time in "Y-M-D H:M:S Z" format
		utc_dt = tokyo_dt.astimezone(utc)
		# utc_dt in millisec format
		millisec = calendar.timegm(utc_dt.timetuple())
		# # convert back to "Y-M-D H:M:S Z" format to verify
		# print(datetime.utcfromtimestamp(float(d)))
		return millisec
	
	def event_length_helper(self):
		length = self.event[2].xpath('./text()')[0]
		try:
			length = length.decode('utf-8')
			dt = length.split(':')
			if len(dt) == 3: # days
				d, h, m = map(int, list(dt))
				minutes = d*24*60+h*60+m
			elif len(dt) == 2: # hours
				h, m = map(int, list(dt))
				minutes = h*60+m
		except Exception:
			minutes = 'infinity'
		finally:
			return minutes
	
	def event_info_helper(self):
		res = []
		info = self.event[3].xpath('./table/tr')
		for tr in info:
			td = tr.xpath('./td/text() | ./td/b/text()')
			try:
				td[1] = td[1].decode('utf-8')
			except Exception:
				td[1] = 'None'
			res.append(td[0] + ': ' + td[1])
		return ' ; '.join(res)