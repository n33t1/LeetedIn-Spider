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

	def __init__(self, eParser):
		IEventsCrawler.__init__(self, eParser)

	def decode_page(self, element):
		return self.driver.page_source

	def request_page(self, _url, xpath):
		print "requesting with selenium..."
		html = None
		try:
			self.driver.get(_url)

			element = self.wait.until(
				EC.presence_of_element_located((By.XPATH, xpath))
			)
			
			html = self.decode_page(element)
		except Exception as e:
			print "Something went wrong with get_page! Error: {}".format(repr(e))
			self.driver.close()
			raise
		else:
			return html.encode('utf-8')
			
