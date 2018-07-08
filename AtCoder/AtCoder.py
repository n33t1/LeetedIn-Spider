#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import RequestException
from lxml import etree
from ContestInfoParser import ContestInfoParser
from pprint import pprint

URL = ['https://atcoder.jp/contest']

def get_page(url):
	headers={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36" 
    }
	res = None
	try:
		print "downloading %s" % url
		response = requests.get(url, headers=headers, timeout=2)
		if response.status_code==200:
			res = response.text
	except Exception as e:
		print "Something went wrong! Error: " + e
	finally:
		return res
		
def parse_page(html):
	print "now parsing ..."

	selector = etree.HTML(html)
	data = []
	try:
		active_contests = selector.xpath('//*[@id="main-div"]/div/div/div[2]/h3[1]/parent::*/div[1]/table/tbody/tr')
		upcoming_contests = selector.xpath('//*[@id="main-div"]/div/div/div[2]/h3[2]/parent::*/div[2]/table/tbody/tr')

		contests = active_contests + upcoming_contests
		if not active_contests and not upcoming_contests:
			raise Exception("No Upcoming Event!")
		else:		
			data = ContestInfoParser(contests).data
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
    # result = html.xpath('//li')
    # print(type(result))  # 输出结果的类型  <class 'list'>
    # for item in result:
    #     print(type(item))   # 输出每个item对象的类型 <class 'lxml.etree._Element'>
    #     print(etree.tostring(item).decode('utf-8')) # 输出<li>标签的文本内容 如：<li class="item-0"><a href="link1.html">first item</a></li>

if __name__ == '__main__':
	main()
