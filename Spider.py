import praw
import requests
from bs4 import BeautifulSoup
import re

r= praw.Reddit(user_agent= "Wallpaper fetch by Bose")
walls= r.get_subreddit('wallpapers').get_top()
urls= [str(x.url) for x in walls]

for j in urls:
	#we want to check if j is album
	#or not

	found= re.search('(imgur.com/a/)+', j)
	if found:
		vals= []
		link= requests.get(j)
		soup= BeautifulSoup(link.content)
		img_links= [str(x) for x in soup.select(".zoom img")]
		for k in img_links:
			imgs= re.search('src="//(.+?)"/>', k)
			if imgs:
				vals.append(imgs.group(1))	
		print j			
		print vals