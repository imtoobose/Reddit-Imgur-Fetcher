import praw
import requests
from bs4 import BeautifulSoup
import re
import sys
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
print "Enter subreddit name:\n"
subreddit_n= stdin.readline().strip()
flag=0

while flag==0:
	print "Enter choice:\n1.Top\n2.Hot\n"
	try:
		choice    = int(stdin.readline())
	except TypeError:
		print "Invalid input"
		continue

	if choice== 1:
		print "1.Top all time\n2. Top Weekly\n3. Top Daily\n4.Top Hourly\n"
		try:
			answer= int(stdin.readline())
		except TypeError:
			print "Invalid input"
			continue

		if answer   == 1 :   
			red, flag = get_top_from_all,   1
		elif answer == 2 :
			red, flag = get_top_from_week,  1 
		elif answer == 3 :   
			red, flag = get_top_from_day,   1
		elif answer == 4 : 
			red, flag = get_top_from_hour,  1
		else:
			print "Invalid input"

	elif choice==2:
		red, flag = get_hot, 1

	else:
		continue		

print "Select number of links to be fetched (max 100, default 5)\n"
try:
	no_of_links = int(stdin.readline())
except TypeError:
	no_of_links = 5

folder      = r"C:\Users\BOSE\Documents\2016\Code\image"
r           = praw.Reddit(user_agent= "Wallpaper fetch by Bose")
walls       = r.get_subreddit('wallpapers').red(limit= no_of_links)		#fetch top 10 images
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