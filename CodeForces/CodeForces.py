#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import RequestException
import re
import json
from pyquery import PyQuery as pq
from ContestInfoParser import ContestInfoParser
from pprint import pprint

URL = ["http://codeforces.com/contests"]

def get_page(url):
	headers={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36" 
    }
	res = None
	try:
		print "downloading %s" % url
		response=requests.get(url, headers=headers, timeout=2)
		if response.status_code==200:
			res = response.text
	except Exception as e:
		print "Something went wrong! Error: " + e
	finally:
		return res

def parse_page(html):
	print "now parsing ..."
	doc = pq(html)
	data = []
	try:
		dataTable = doc("#pageContent > div > div.datatable > div > table > tr:gt(0)")
		if not dataTable or len(dataTable) == 0:
			raise Exception("No Upcoming Event!")
		else:
			data = ContestInfoParser(dataTable).data
	except Exception as e:
		print e
	finally:
		return data

def main():
	res = []
	for url in URL:
		html = get_page(url)
		if not html:
			continue
		temp = parse_page(html)
		res.extend(temp)
	pprint(res)

if __name__ == "__main__":
	main()