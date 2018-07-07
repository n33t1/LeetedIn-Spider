from lxml import etree
import requests
from requests.exceptions import RequestException
import re
import json
from pprint import pprint
from ContestInfoParser import ContestInfoParser 

URL = ["https://code.google.com/codejam/schedule?data=1", "https://code.google.com/codejam/kickstart/schedule?data=1"]

def get_page(url):
    headers={
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36" 
    }
    try:
		print "downloading %s" % url
		response=requests.get(url, headers=headers, timeout=2)
		if response.status_code==200:
			return response.text
		return None
    except RequestException as e:
        return "Something went wrong! Error: " + e

def parse_page(html):
	print "now parsing ..."
	temp = eval(html)
	schedules = temp['schedules']
	data = ContestInfoParser(schedules).data
	return data

def main():
	res = []
	for url in URL:
		html = get_page(url)
		temp = parse_page(html)
		res.extend(temp)
	pprint(res)

if __name__ == "__main__":
	main()