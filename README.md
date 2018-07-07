# CodingContestsCrawler
Scraper for popular coding contests.

[
	{'event_title': '', 
	 'event_info': optinal
	 'events': [
		 'duration': 
		 'name': 
		 'startDateTime':
		 'registrationDeadline':,
		 'url':,
		 'prerequisite': optional
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

* __[LeetCode Contest](https://leetcode.com/contest/)__: requests, ajax

AtCoder

Facebook Hacker Cup

HackerRank

CodeChef

TopCoder

Coderbyte

Project Euler

CodeEval

Codewars

hackerearth

## Installation
```
pip install requirements
```