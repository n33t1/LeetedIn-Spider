# CodingContestsCrawler
Scraper for popular coding contests. Currently only scrapying active contests. 

[
	{'event_title': '', 
	 'event_info': optinal
	 'events': [
		 'duration': 
		 'name': 
		 'startDateTime':
		 'registrationDeadline':,
		 'url':,
		 'prerequisite': optional,
		 'addtionalInfo': optional
	 ]
	}
]

List of coding contests scraped and Python crawler libraries used:
* __[Code Forces](http://codeforces.com/contests)__: CodeForces presents (all of their) contest info with static html webpage. We only need to parse the table which stores all the contest info. 
  * requests, pyquery, re
  * url: http://codeforces.com/contests

* __[Google Code Jam](https://code.google.com/codejam/)__: Google Code Jam web page was written with dynamic Javascript, meaning that if we request the contest schedule base url directly it will return pre compiled js script, instead of the compiled html we want. But luckily, we can cheat by requesting their base url with additional `data=1` token. This will directly provide their event info json, which is what we want. 
  * requests, re， XPath(lxml)
  * url: https://code.google.com/codejam/schedule, https://code.google.com/codejam/kickstart/schedule
  * However, Google Code Jam has more than one contest event. The entire [Google Code Jam Family](https://code.google.com/codejam/past-contests) consists of Google Code Jam, Distributed Code Jam 2018, Google Code Jam Kickstart, Google Code Jam I/O for Woman, and other contests. And their schedule are likely to be stored in different webpages. With the url listed above, we were only able to scrape Google Code Jam, Distributed Code Jam and Google Code Jam Kickstart. Also, their website are likely to change each year. We should also use a monitor to watch for possible changes. 

* __[LeetCode Weekly Contest](https://leetcode.com/contest/)__: I tried to request from their graphQL API, but it seems like x-csrftoken (or other possible incorrect information in header) was causing trouble. So I'm temporarily using Selenium to fetch the data, although it's facing proformance bottlenecks.
  * Selenium, re

* __[AtCoder](https://atcoder.jp/contest)__: Contests info stored in static html. Easy Peasy. 
  * ... aND I LIED. I tried to experiment around with lxml (aka XPATH). It was a torture, altough on performance it beats all other selectors (pyquery, bs4, etc). So far I prefer pyquery the most.  
  * requests, XPATH(lxml)

* __[Facebook Hacker Cup](https://www.facebook.com/hackercup)__: All the info stored in a Facebook group. Hard to read directly. Will come back later. ###TODO

* __[HackerRank](https://www.hackerrank.com/contests)__: All active contest info can be fetched with [this url](https://www.hackerrank.com/rest/contests/upcoming?offset=0&limit=10&contest_slug=active). 

* __[CodeChef](https://www.codechef.com/contests)__: Static HTML page as well. Pretty standard. 

TopCoder

Coderbyte

Project Euler

CodeEval

Codewars

hackerearth

Kaggle 

## Setup
```
pip install requirements
```