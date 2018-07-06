#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import RequestException
import re
import json
from pyquery import PyQuery as pq

URL = "http://codeforces.com/contests"
START_DATE_INFO_KEYS = ["day", "month", "year", "hour", "min", "sec", "p1"]
CONTEST_INFO_KEYS = ["event_name", "starting_date", "event_duratoin", "registration_ddl"]
DATE_HASH = {'days': 1, 'day': 1, 'weeks': 7, 'week': 7}

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

def get_item(tr):
	res = []
	cnt = 0
	for td in tr("td").items():
		if td(".format-time"):
			href = td("a").attr("href")
			pattern = re.compile(".*?day=(.*?)&month=(.*?)&year=(.*?)&hour=(.*?)&min=(.*?)&sec=(.*?)&p1=(.*?)?$", re.S)
			items = re.findall(pattern, href)
			date_info = dict(zip(START_DATE_INFO_KEYS, items))
			# print date_info
			res.append(date_info)
		elif cnt == 5:
			temp = td.text()
			if re.search(r'Before registration', temp):
				temp = re.findall("(\d+)\s(.*?)$", temp)
			elif re.search(r'Until closing', temp):
				temp = re.findall(".*?Until closing.*?(\d+)\s(.*?)$", temp)
			# get current date in UTC
			# shift date
			temp = temp[0]
			temp = int(temp[0]) * DATE_HASH[temp[1]]
			# closing date/opening date = curr + shift
			res.append(temp)

		elif cnt != 1 and cnt != 4:
			data = td.text()
			res.append(data)
		cnt += 1

	yield res

def parse_page(html):
	print "now parsing..."
	doc = pq(html)
	data, res = [], []
	try:
		dataTable = doc("#pageContent > div > div.datatable > div > table > tr:gt(0)")
		if not dataTable or len(dataTable) == 0:
			raise Exception("No Upcoming Event!")
		else:
			for tr in dataTable.items():
				for td in get_item(tr):
					data.append(td)
		res = dict(zip(CONTEST_INFO_KEYS, data))
	except Exception as e:
		print e
	finally:
		return res

def main():
	html = get_page()
	json = parse_page(html)
	print json

if __name__ == "__main__":
	main()