#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

from AbstractEventsParser import AbstractEventsParser, AbstractEParser 

class EParser(AbstractEParser):
	def __init__(self, event, url=None):
		AbstractEParser.__init__(self, event, url)
		# self.event_url_helper()
		self.run()

	def event_url_helper(self):
		return 1

class EventParser(AbstractEventsParser):
	def __init__(self, eParser, events, title, url=None):
		AbstractEventsParser.__init__(self, eParser, events, title, url)

# e = EventParser(EParser, [1], 2 ,3)
# print e

if __name__ == '__main__' and __package__ is None:
	from os import sys, path
	sys.path.append(path.dirname(path.abspath(__file__)))
