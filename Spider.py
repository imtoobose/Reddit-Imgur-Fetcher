import praw
import requests
from bs4 import BeautifulSoup
import re

r= praw.Reddit(user_agent= "Wallpaper fetch by Bose")
walls= r.get_subreddit('wallpapers').get_top()
urls= [str(x.url) for x in walls]
chk_a= re.search('')
for j in urls:
	#we want to check if j is album
	#or not
	
	link= requests.get(j)
	soup= BeautifulSoup(open(link.content))