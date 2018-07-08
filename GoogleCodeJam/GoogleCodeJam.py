#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

from lxml import etree
import requests
from requests.exceptions import RequestException
import re
import json
from pprint import pprint
from ContestInfoParser import ContestInfoParser 

URL = ["https://code.google.com/codejam/", "https://code.google.com/codejam/kickstart/"]

def get_page(url):
	headers={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36" 
	}
	res = None

	try:
		print "downloading %s" % url
		response=requests.get(url, headers=headers, timeout=2)
		if response.status_code==200:
			res = response.text
	except RequestException as e:
		print "Something went wrong! Error: " + e
	finally:
		return res

def parse_page(html, url):
	print "now parsing ..."
	temp = eval(html)
	schedules = temp['schedules']
	data = ContestInfoParser(schedules, url).data
	return data

def main():
	res = []
	for url in URL:
		data_api = url + 'schedule?data=1'
		html = get_page(data_api)
		if not html:
			continue
		temp = parse_page(html, url)
		res.extend(temp)
	pprint(res)

if __name__ == "__main__":
	main()