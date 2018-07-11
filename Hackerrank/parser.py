#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEParser import IEParser 
import re
from lxml import etree
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import calendar
from pprint import pprint
 
class EParser(IEParser):
	def __init__(self, event, **kwargs):
		IEParser.__init__(self, event)
		if event['archived'] or event['name'] == 'ProjectEuler+':
			raise Exception("Event Not Valid!")
		self.run()

	def event_name_helper(self):
		return self.event['name'].encode('utf-8')

	def event_url_helper(self):
		base_url = 'https://www.hackerrank.com/' 
		slug = self.event['slug']
		return base_url + slug

	def registration_ddl_helper(self):
		pass

	def start_date_helper(self):
		self.start_time = self.event['epoch_starttime']
		return int(self.start_time)

	def event_length_helper(self):
		end_time = int(self.event['epoch_endtime'])
		delta = end_time - self.start_time
		minutes = delta / 60
		return minutes
	
	def event_info_helper(self):
		return self.event['description'].encode('utf-8')
