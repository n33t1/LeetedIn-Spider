#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IEventsCrawler import IEventsCrawler

class IEventsCrawlerDP(IEventsCrawler):
	driver = webdriver.Chrome()
	wait = WebDriverWait(driver, 10)

	def __init__(self, url, eParser, title, flagEleXPath):
		IEventsCrawler.__init__(self, url, eParser, title)
		self.flagEleXPath = flagEleXPath # can be done better

	def request_page(self, _url):
		res = []
		try:
			self.driver.get(_url)

			element = self.wait.until(
				EC.presence_of_element_located((By.XPATH, self.flagEleXPath))
			)

			html = element.text
			# html = html.decode('utf-8')
			# html = str(html)

			res = [html]
		except Exception as e:
			print "Something went wrong with get_page! Error: {}".format(repr(e))
			raise
		else:
			self.driver.close()
			return res
			
