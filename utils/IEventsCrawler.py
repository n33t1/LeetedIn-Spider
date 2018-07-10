#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import RequestException
import re
import json
from pyquery import PyQuery as pq
from pprint import pprint
from EventsParser import EventsParser  
import traceback 

class IEventsCrawler:
	headers={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36" 
	}

	def __init__(self, _URL, eParser, title, **kwargs):
		self._URL = _URL
		self.eParser = eParser
		self.title = title
		self.headers = kwargs['headers'] if 'headers' in kwargs else self.headers
		self.res = []

	def run(self):
		self.get_and_parse_page()
		pprint(self.res)

	def get_and_parse_page(self):
		pass 

	def get_response(self, response):
		return response.text

	def get_page(self, _url):
		res = None
		try:
			print "downloading %s" % _url
			response=requests.get(_url, headers=self.headers, timeout=2)
			if response.status_code==200:
				res = self.get_response(response)
		except Exception as e:
			print "Something went wrong with get_page! Error: {}".format(repr(e))
			traceback.print_exc()
		finally:
			return res

	def parse_page(self, resp):
		print "now parsing ..."
		data = []
		try:
			data = EventsParser(self.eParser, resp, self.title).data
		except Exception as e:
			print "parse_page failed! Error: {}".format(repr(e))
			traceback.print_exc()
		finally:
			return data
