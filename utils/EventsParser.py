#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

class EventsParser:
	def __init__(self, eParser, events, title, url=None, info=None):
		self.data = []
		self.run(eParser, title, events, url, info)
	
	def __repr__(self):
		print "Events parsed: "
		from pprint import pformat
		return pformat(self.data, indent=4, width=1)

	def run(self, eParser, title, events, url, event_info):
		info = {}
		info['event_title'] = title
		info['events'] = []
		for event in events:
			try:
				temp = eParser(event, url, event_info).res
			except Exception:
				continue
			else:
				info['events'].append(temp)
		self.data.append(info)
