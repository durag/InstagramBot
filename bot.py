import atexit
import datetime
import itertools
import json
import logging
import random
import signal
import urllib2
import sys
import time
import requests
import threading
from datetime import datetime


# COLORS
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan
BL = '\033[30m' # black
UND = '\033[4m' # underline
BLINK = '\033[5m' # blink


# LIST FOR KEEPING TRACK OF WHAT TO LIKE/FOLLOW
# AND WHAT HAS BEEN LIKED/FOLLOWED
# AND TAGS
tags = []
ready_to_follow = []
ready_to_like = []
liked_media = []
followed_users = []

# POSSIBLE BAN
error_400 = 0
# PROBABLE BAN
error_400_to_ban = 3


# POPULATE TAG LIST
file = open('tags.txt', 'a')
file.close()
with open('tags.txt') as f:
	lines = f.readlines()

for line in lines:
	tags.append(str(line).replace('\n', ''))
print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'ACTION'+W+'] Tags loaded -> ' + str(len(tags)))



# URLS FOR VARIOUS FUNCTIONS
url = 'https://www.instagram.com/'
url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
url_likes = 'https://www.instagram.com/web/likes/%s/like/'
url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
url_comment = 'https://www.instagram.com/web/comments/%s/add/'
url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
url_login = 'https://www.instagram.com/accounts/login/ajax/'
url_logout = 'https://www.instagram.com/accounts/logout/'
url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
url_user_detail = 'https://www.instagram.com/%s/?__a=1'

user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
				  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'


# CLASS TO STORE USER INFORMATION
class bot:
	following = 0
	followers = 0
	username = ''
	password = ''
	id = ''
	
# FUNCTION TO GET PROGRESS
def get_progress():
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Users followed by bot -> ' + str(len(followed_users)))
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Media liked by bot -> ' + str(len(liked_media)))



# FUNCTION TO GET LIST OF MEDIA FROM TAG SEARCH
def get_media_by_tag(s, tag):
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] Loading media from tag -> ' + str(tag))
	url = 'https://www.instagram.com/explore/tags/' + str(tag) + '/?__a=1'
	try:
		got = s.get(url)
		data = json.loads(got.text)
		media = list(data['tag']['media']['nodes'])
		return media
	except Exception, e:
		media_by_tag = []
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] There was an error -> ' + str(e))


# FUNCTION TO GET MEDIA INFO BEFORE LIKING
def get_media_info(media):
	list = []
	for med in media:
		id = str(med['owner']['id'])
		entry = id
		list.append(entry)
	return list	

# FUNCTION TO LIKE MEDIA
def like_media_list(s, med):
#	for med in media:
	id = med['id']
	url = 'https://www.instagram.com/web/likes/' + str(id) + '/like/'
	try:
		if str(id) not in liked_media:
			liked = s.post(url)
			liked_media.append(str(id))
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+P+'LIKE'+W+'] Liked tagged media with ID -> ' + str(id))
		else:
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'LIKE'+W+'] Already liked tagged media with ID -> ' + str(id))
	except Exception, e:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] There was an error in like -> ' + str(e))

# FUNCTION TO FOLLOW LIST OF MEDIA OWNERS
def follow_owner_list(s, owner, obj):
#	for owner in owners:
	if str(owner) != str(obj.id):
		url = 'https://www.instagram.com/web/friendships/' + str(owner) + '/follow/'
		try:
			if str(owner) not in followed_users:
				follow = s.post(url)
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+O+'FOLLOW'+W+'] Followed user with ID -> ' + str(owner))
				followed_users.append(str(owner))
			else:
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'FOLLOW'+W+'] Already following user with ID -> ' + str(owner))
		except Exception, e:
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] There was an error in follow -> ' + str(e))
	else:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ACTION'+W+'] Cannot follow yourself -> ' + str(owner))


# FUNCTION TO RESOLVE USERNAME TO INSTAGRAM ID
def get_user_id_by_login(s, username):
	info_url = 'https://www.instagram.com/' + str(username) + '/?__a=1'
	info = s.get(info_url)
	data = json.loads(info.text)
	id = data['user']['id']
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Instagram ID -> ' + str(id))

	return id
	
# FUNCTION TO GET FOLLOWER/FOLLOWS COUNT
def get_follow_counts(s, username):
	url = 'https://www.instagram.com/' + str(username) + '/?__a=1'
	try:
		r = s.get(url)
		user_info = json.loads(r.text)

		follows = user_info['user']['follows']['count']
		followers = user_info['user']['followed_by']['count']
		
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Followers -> ' + str(followers))
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Following -> ' + str(follows))

		return follows, followers
	except Exception, e:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] There was an error getting following/follower count -> ' + str(e))
	

# FUNCTION TO LOGIN AND GATHER INFO
def login(obj):

	# ESTABLISH REQUEST SESISON
	s = requests.Session()
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'LOGIN'+W+'] Attempting to login...')
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'LOGIN'+W+'] Username -> ' + str(obj.username))
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'LOGIN'+W+'] Password -> ' + ('*' * len(obj.password)))
	s.cookies.update({
		'sessionid': '',
		'mid': '',
		'ig_pr': '1',
		'ig_vw': '1920',
		'csrftoken': '',
		's_network': '',
		'ds_user_id': ''
	})
	login_post = {
		'username': obj.username,
		'password': obj.password
	}
	s.headers.update({
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': accept_language,
		'Connection': 'keep-alive',
		'Content-Length': '0',
		'Host': 'www.instagram.com',
		'Origin': 'https://www.instagram.com',
		'Referer': 'https://www.instagram.com/',
		'User-Agent': user_agent,
		'X-Instagram-AJAX': '1',
		'X-Requested-With': 'XMLHttpRequest'
	})
	
	# ACTUALLY LOGIN HERE
	r = s.get(url)
	s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
	time.sleep(5 * random.random())
	login = s.post(
		url_login, data=login_post, allow_redirects=True)
	s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
	csrftoken = login.cookies['csrftoken']
	time.sleep(5 * random.random())

	# DETERMINE WHETHER OR NOT IT WAS SUCCESSFUL
	if login.status_code == 200:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'LOGIN'+W+'] Successful login')
		r = s.get('https://www.instagram.com/')
		finder = r.text.find(obj.username)
		if finder != -1:
			obj.id = str(get_user_id_by_login(s, obj.username))
			obj.following, obj.followers = get_follow_counts(s, obj.username)
			login_status = True
		else:
			login_status = False
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'LOGIN'+W+'] Your login credentials were incorrect')
	else:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'LOGIN'+W+'] There was a connection error when trying to login')
		
	return s, csrftoken

# FUNCTION TO LOGOUT ONCE THE WORK IS DONE
def logout(obj, s, csrftoken):
	try:
		logout_post = {'csrfmiddlewaretoken': csrftoken}
		logout = s.post(url_logout, data=logout_post)
		login_status = False
		print('\n[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'LOGOUT'+W+'] Successful logout')
	except Exception, e:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'LOGOUT'+W+'] There was an error while logging out -> ' + str(e))
		
		

# FUNCTION TO CONTROL FOLLOW PROTOCOL
def follow_time(s, obj):
	while 1:
		for owner in ready_to_follow:
			follow_owner_list(s, owner, obj)
			ready_to_follow.remove(owner)
			time.sleep(30)
		time.sleep(5)

# FUNCTION TO CONTROL LIKE PROTOCOL
def like_time(s):
	while 1:
		for med in ready_to_like:
			def like_media_list(s, med):
			ready_to_like.remove(med)
			time.sleep(5)
		time.sleep(5)

# FUNCTION TO CONTROL TIMING PROTOCOL
def timing(s, obj):
	while 1:
		time.sleep(300)
		get_follow_counts(s, obj.username)
		get_progress()


		
try:
#	try:
	obj = bot()
	bot.username = str(sys.argv[1])
	bot.password = str(sys.argv[2])
		
	# LOGIN AND GET USER INFO
	s, token = login(obj)

	# START A LIKE TIMER
	like_thread = threading.Thread(target=like_time, args=(s,))
	like_thread.daemon = True
	like_thread.start()

	# START A FOLLOW TIME
	follow_thread = threading.Thread(target=follow_time, args=(s, obj,))
	follow_thread.daemon = True
	follow_thread.start()
		
	for tag in tags:
		# GET BOT TODO LIST READY
		media = get_media_by_tag(s, str(tag))
		for med in media:
			if med not in ready_to_like:
				read_to_like.append(med)
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] Media loaded -> ' + str(len(ready_to_like)))
			
		# GET MEDIA OWNERS
		owners = get_media_info(media)
		for own in owners:
			if own not in read_to_follow:
				ready_to_follow.append(own)
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] Media owners found -> ' + str(len(ready_to_follow)))
	
		# LIKE ALL MEDIA IN MEDIA LIST
		#like_media_list(s, media)
	
		# FOLLOW LIST OF MEDIA OWNERS
		#follow_owner_list(s, owners, obj)
	
		# CHECK FOLLOW COUNTS AGAIN
		#get_follow_counts(s, obj.username)
	
		# CHECK PROGRESS
		#get_progress()

		#print('Waiting a minute...')
		time.sleep(10)
	timing(s, obj)
	# DON'T DIE
#	keep_alive()
#	except Exception, e:
#		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] There was an error -> ' + str(e))
#		sys.exit()
except KeyboardInterrupt:
	logout(obj, s, token)
	sys.exit()
