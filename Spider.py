import praw
import requests
from bs4 import BeautifulSoup
import re
import sys

def download_image():
	pass


r         = praw.Reddit(user_agent= "Wallpaper fetch by Bose")
walls     = r.get_subreddit('wallpapers').get_top(limit=10)
urls      = [str(x.url) for x in walls]
chk_imgur = re.compile('(imgur)+?')

for j in urls:
	print j

print "--------------\n\n"

for j in urls:
	if chk_imgur.search(j):
		found          = re.search('(imgur\.com/a/)+', j)  #check if imgur album
		chk_image_only = re.search('(i\.imgur\.com)+', j)  #check if imgur image
		
		if found:
			album_imgs = []
			link       = requests.get(j)
			soup       = BeautifulSoup(link.content, "html.parser")
			img_links  = [str(x) for x in soup.select(".zoom img")]
			for k in img_links:
				imgs   = re.search('src="//(.+?)"/>', k)
				if imgs:
					album_imgs.append(imgs.group(1))	
			for k in album_imgs:
				print k
				download_image()

		elif chk_image_only:
			link = requests.get(j)
			download_image()

		else:
			link     = requests.get(j)			
			soup     = BeautifulSoup(link.content, "html.parser")
			img_link = (re.search('src="//(.+?)"/>', str(soup.select(".post-image img")))).group(1)
			print img_link
			download_image()