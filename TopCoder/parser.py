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
from pprint import pprint

class EParser(IEParser):
	BASE_URL = 'https://www.topcoder.com/'

	def __init__(self, event, url=None):
		# print event
		IEParser.__init__(self, event, url)
		# self.duration = None
		self.run()

	def event_name_helper(self):
		return self.event('div._1u9jzQ > div._1wy0wX > a').text()

	def event_url_helper(self):
		token = self.event('div._1u9jzQ > div._1wy0wX > a').attr('href')
		return self.BASE_URL + token
	
	def registration_ddl_helper(self):
		pass

	def start_date_helper(self):
		pass
	
	def end_date_helper(self):
		# end date was given in the link...
		ts = self.event('div._1u9jzQ > div._1wy0wX > div > span.JV6Mui')
		print ts

	def strToMillisec(self, dt):
		pass

	def event_length_helper(self):
		pass
		
	def event_info_helper(self):
		pass
