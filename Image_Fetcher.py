import praw
import requests
from bs4 import BeautifulSoup
import re
from sys import stdin
import os

def download_image(thelink, storage):
	gg= requests.get(thelink)
	if gg.status_code==200:
		with open(storage , 'wb') as f:
			for chunk in gg.iter_content(2048):
				f.write(chunk)

def chk_not_reddit(pp):
	qq= pp.split("/")
	for i in qq:
		if i=="www.reddit.com":
			return false
	
print "Reddit Imgur Image Fetch Running v.1.0.1"
print "Enter subreddit name:"
subreddit_n = stdin.readline().strip()
print "Select number of links to be fetched (max 100, default 5)"
try:
	no_of_links = int(stdin.readline())
except TypeError:
	no_of_links = 5

flag        = 0
folder      = r"C:\Users\BOSE\Documents\2016\Code\image"
r           = praw.Reddit(user_agent= "Wallpaper fetch by Bose")

while True:
	print "Enter choice:\n1.Top\n2.Hot"
	
	try:
		choice    = int(stdin.readline())
	except TypeError:
		print "Invalid input"
		continue

	if choice == 1:
		print "1.Top all time\n2. Top Weekly\n3. Top Daily\n4.Top Hourly"
		try:
			answer= int(stdin.readline())
		except TypeError:
			print "Invalid input"
			continue

		if answer   == 1 :
			walls  = r.get_subreddit(subreddit_n).get_top_from_all(limit= no_of_links)   
			break
		elif answer == 2 :
			walls  = r.get_subreddit(subreddit_n).get_top_from_week(limit= no_of_links)   
			break
		elif answer == 3 :   
			walls  = r.get_subreddit(subreddit_n).get_top_from_day(limit= no_of_links)   
			break
		elif answer == 4 : 
			walls  = r.get_subreddit(subreddit_n).get_top_from_hour(limit= no_of_links)   
			break
		else:
			print "Invalid input"
			continue

	elif choice==2:
		walls  = r.get_subreddit(subreddit_n).get_hot(limit= no_of_links)
		break   

	else:
		print "Invalid input"
		continue		

urls        = [str(x.url) for x in walls]								#fetch urls and store as strings
chk_imgur   = re.compile('(imgur\.com)+?')								#check if imgur page
counter     = 0


print "The retrieved links are:\n"
for j in urls:
	print j

print "--------------\n\n Downloading links: \n"

for j in urls:
	if chk_imgur.search(j):
		found          = re.search('(imgur\.com/a/)+', j)  #check if imgur album
		chk_image_only = re.search('(i\.imgur\.com)+', j)  #check if imgur image
		counter       += 1
		path           = folder+str(counter)+".jpg"

		#code for imgur albums
		if found:										   
			album_imgs = []
			link       = requests.get(j)
			soup       = BeautifulSoup(link.content, "html.parser")
			img_links  = [str(x) for x in soup.select(".zoom img")]
			for k in img_links:
				imgs   = re.search('src="//(.+?)"/>', k)
				if imgs:
					album_imgs.append(imgs.group(1))

			print "Downloading an album\n"
			for k in album_imgs:
				counter += 1
				a_path   = folder+str(counter)+".jpg"
				print "Downloading image: " + str(counter) +".....%"
				download_image("http://"+k, a_path)
			print "\nAlbum downloaded\n"

		#code for imgur images
		elif chk_image_only:
			link = requests.get(j)
			if link.status_code==200:
				print "Downloading image: " + str(counter) +".....%"
				print path
				with open(path , 'wb') as f:
					for chunk in link.iter_content(2048):
						f.write(chunk)
			

		#for when imgur page with image is given
		elif chk_not_reddit(j):
			link     = requests.get(j)			
			soup     = BeautifulSoup(link.content, "html.parser")
			img_link = (re.search('src="//(.+?)"/>', str(soup.select(".post-image img")))).group(1)
			print "Downloading image: " + str(counter) +".....%"
			download_image("http://"+img_link, path)

		else:
			continue