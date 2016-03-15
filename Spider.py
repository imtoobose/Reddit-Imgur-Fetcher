import praw
from bs4 import beautifulsoup4

r= praw.Reddit(user_agent= "Wallpaper fetch by Bose"
walls= r.get_subreddit('wallpapers').get_top()
urls= [str(x.url) for x in walls]

