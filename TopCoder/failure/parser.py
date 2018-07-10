#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(__file__ + "/../../"))

from utils.IEParser import IEParser 

import re
from datetime import datetime, timedelta
from pytz import timezone
import xml.etree.ElementTree as ET
from lxml import etree
import pytz
import calendar
from pprint import pprint

class EParser(IEParser):
	def __init__(self, event, url=None):
		IEParser.__init__(self, event, url)
		# print ET.tostring(event).decode()
		self.selector = None
		self.run()

	def event_name_helper(self):
		pass
		# try:
		# 	s = self.event.find('./title')
		# 	return s.text
		# except Exception as e:
		# 	print "Cannot parse event name! Error: {}".format(repr(e))
		# 	raise Exception('Invalid Event!')

	def event_url_helper(self):
		# s = self.event.find('./description')
		# print ET.tostring(s).decode()
		try:
			s = self.event.find('./description')
			html = s.text
			parser = etree.HTMLParser(encoding="utf-8")
			self.selector = etree.HTML(html, parser)
			a = self.selector.xpath('./div')
			print etree.tostring(a)
		except Exception as e:
			print "Cannot parse event name! Error: {}".format(repr(e))
			raise Exception('Invalid Event!')
	
	def registration_ddl_helper(self):
		pass

	def start_date_helper(self):
		pass 

	def strToMillisec(self, dt):
		pass
	
	def end_date_helper(self):
		pass

	def event_length_helper(self):
		pass
		
	def event_info_helper(self):
		pass
