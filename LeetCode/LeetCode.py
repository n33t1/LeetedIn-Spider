#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ContestInfoParser import ContestInfoParser
from pprint import pprint

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

URL = ["https://leetcode.com/contest/"]

def get_page(url):
	res = None
	try:
		print "Requesting with selenium ..."
		driver.get(url)
		xpath = '//*[@id="contest-app"]/div/div/div[2]/div[1]/div/div[1]/div/a/div'
		element = wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
		text = element.text
		res = [text]
	except Exception as e:
		print "Something went wrong! Error: " + e
	finally:
		return res

def parse_page(html, url):
	print "now parsing ..."
	data = ContestInfoParser(html, url).data
	return data

def main():
	try:
		res = []
		for url in URL:
			html = get_page(url)
			if not html:
				continue
			temp = parse_page(html, url)
			res.extend(temp)
		pprint(res)
	except Exception as e:
		print "Something went wrong! Error: " + e
	finally:
		driver.close()
		pass


if __name__ == '__main__':
    main()