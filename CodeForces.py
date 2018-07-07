#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import RequestException
import re
import json
from pyquery import PyQuery as pq
from ContestInfo import ContestInfo
from pprint import pprint

URL = "http://codeforces.com/contests"

def get_page():
    headers={
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36" 
    }
    try:
        response=requests.get(URL, headers=headers, timeout=2)
        if response.status_code==200:
            return response.text
        return None
    except RequestException as e:
        return "Something went wrong! Error: " + e

def parse_page(html):
	print "now parsing..."
	doc = pq(html)
	data = {}
	try:
		dataTable = doc("#pageContent > div > div.datatable > div > table > tr:gt(0)")
		if not dataTable or len(dataTable) == 0:
			raise Exception("No Upcoming Event!")
		else:
			for tr in dataTable.items():
				event_id = int(tr.attr('data-contestid'))
				event_info = ContestInfo(tr)
				data[event_id] = event_info
	except Exception as e:
		print e
	finally:
		return data

def main():
	html = get_page()
	json = parse_page(html)
	pprint(json)

if __name__ == "__main__":
	main()