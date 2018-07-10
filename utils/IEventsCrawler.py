#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

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
	
	def request_page(self, _url):
		import requests 

		response = requests.get(_url, headers=self.headers, timeout=2)
		if response.status_code == 200:
			return self.get_response(response)

	def get_page(self, _url):
		res = None
		try:
			print "downloading %s" % _url
			res = self.request_page(_url)
		except Exception as e:
			print "Something went wrong with get_page! Error: {}".format(repr(e))
			traceback.print_exc()
			raise
		finally:
			return res

	def parse_page(self, resp, _url=None):
		print "now parsing ..."
		data = []
		try:
			data = EventsParser(self.eParser, resp, self.title, _url).data
		except Exception as e:
			print "parse_page failed! Error: {}".format(repr(e))
			traceback.print_exc()
		finally:
			return data
