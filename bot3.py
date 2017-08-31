import itertools
import json
import random
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
ready_to_follow = []
ready_to_like = []
liked_media = []
followed_users = []
global x
global cycle_grace_time_s

print('''
---------------------------------------------------------------
|        ____           __                                    |
|       /  _/___  _____/ /_____ _____ __________ _____ ___    |
|       / // __ \/ ___/ __/ __ `/ __ `/ ___/ __ `/ __ `__ \   |
|     _/ // / / (__  ) /_/ /_/ / /_/ / /  / /_/ / / / / / /   |
|    /___/_/ /_/____/\__/\__,_/\__, /_/   \__,_/_/ /_/ /_/    |
|               ____        __/____/                          |
|              / __ )____  / /_                               |
|             / __  / __ \/ __/                               |
|            / /_/ / /_/ / /_                                 |
|           /_____/\____/\__/                                 |
|                                                             |
|                                        @the.red.team        |
|                                                             |
---------------------------------------------------------------''')


print('Bot start time -> ' + str(datetime.now().date()) + ' | ' + str(datetime.now().time()))

if len(sys.argv) < 4:
	print('Usage: python ' + str(sys.argv[0]) + ' [USERNAME] [PASSWORD] [PROTOCOL]\n')
	print('Protocol:')
	print('	1 - Follow 120 pages/day')
	print('	2 - Follow 240 pages/day')
	print('	3 - Follow 360 pages/day')
	print('	4 - Follow 480 pages/day')
	print('	5 - Follow 600 pages/day')
	print('	6 - Follow 720 pages/day')
	print('	7 - Follow 840 pages/day')



# Now lets put it into one line
try:
	mode = int(sys.argv[3])
except:
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] You did not select a valid protocol')
	sys.exit()

if mode == 1:
	x = 120
elif mode == 2:
	x = 240
elif mode == 3:
	x = 360
elif mode == 4:
	x = 480
elif mode == 5:
	x = 600
elif mode == 6:
	x = 720
elif mode == 7:
	x = 840
else:
	x = 960



# URLS FOR VARIOUS FUNCTIONS
url = 'https://www.instagram.com/'
url_login = 'https://www.instagram.com/accounts/login/ajax/'
url_logout = 'https://www.instagram.com/accounts/logout/'

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
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Users followed by bot -> ' + str(len(followed_users)) + '/' + str(len(ready_to_follow)))
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Media liked by bot -> ' + str(len(liked_media)) + '/' + str(len(ready_to_like)))



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
		media = []
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] There was an error -> ' + str(e))
		return media

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
	url = 'https://www.instagram.com/' + str(username) + '/?__a=1'
	info = s.get(url)
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
		
		





# MATH
# Time it takes to complete one cycle of follows if you follow 120 pages and there is 30 seconds between follows
# 120 * 30 = 3600 seconds = 60 minutes

# MATH
# How log would the grace period between cycles be if you only wanted to follow 360 people a day when each cycle of 120 takes 60 minutes?
# Total cycle time = 60 * 3 = 120 Minutes = 3 hours
# 24 - 3 = 21 Hours = 1260 Minutes = 75600 Seconds
# 75600 / 3 = 25200 Seconds
# Each Grace period would have to be time.sleep(25200)


# Now lets put it in a way python can understand it
# cycle_time = 60 # MINUTES
# number_of_cycles = x / 120 # TARGET FOLLOWER COUNT / FOLLOW CYCLE COUNT
# total_cycle_time_m = cycle_time * number_of_cycles
# total_grace_time_s = ((24 - (total_cycle_time_m / 60))*60)*60
# cycle_grace_time_s = total_grace_time_s / number_of_cycles




# FUNCTION TO CONTROL FOLLOW PROTOCOL
def follow_time(s, obj):
	global following_bool
	global cycle_grace_time_s
	count = 0
	while 1:
		for owner in ready_to_follow:
			following_bool = True
			follow_owner_list(s, owner, obj)
			ready_to_follow.remove(owner)
			count = count + 1

			# THIS IS TO MAINTIAN YOUR DAILY RATE
			if count < 120:
				time.sleep(30)
			elif count >= 120:
				count = 0
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'NOTICE'+W+'] Finished FOLLOW cycle | waiting ' + str(cycle_grace_time_s) + ' until next cycle')
				time.sleep(cycle_grace_time_s)
		time.sleep(5)
		if following_bool == True:
			following_bool = False

# FUNCTION TO CONTROL LIKE PROTOCOL
def like_time(s):
	global liking_bool
	global cycle_grace_time_s
	count = 0
	while 1:
		for med in ready_to_like:
			liking_bool = True
			like_media_list(s, med)
			ready_to_like.remove(med)
			count = count + 1

			# THIS IS TO MAINTIAN YOUR DAILY RATE
			if count < 120:
				time.sleep(5)
			elif count >= 120:
				count = 0
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'NOTICE'+W+'] Finished LIKE cycle | waiting ' + str(cycle_grace_time_s) + ' until next cycle')
				time.sleep(cycle_grace_time_s)
		time.sleep(5)
		if liking_bool == True:
			liking_bool = False	

# FUNCTION TO CONTROL TIMING PROTOCOL
def timing(s, obj):
	while 1:
		time.sleep(300)
		get_follow_counts(s, obj.username)
		get_progress()


		
try:
	# THE BOOLEANS WHICH ARE RESPONSIBLE FOR SHOWING WHEN THE CYCLES ARE COMPLETE
	global liking_bool
	global following_bool

	liking_bool = False
	following_bool = False

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

	# START A PROGRESS THREAD
	progress_thread = threading.Thread(target = timing, args = (s, obj,))
	progress_thread.daemon = True
	progress_thread.start()

	# SET THE BOTS PACE
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Daily target follow count -> ' + str(x))

	cycle_grace_time_s = (((24 - (( 60 * (x / 120)) / 60)) * 60) * 60) / (x / 120)

	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] There will be a total of ' + str(x/120) + ' cycles')
	print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Your cyclic grace period will be -> ' + str(cycle_grace_time_s) + ' seconds')


	while 1:
		if (liking_bool == False) and (following_bool == False):

			# POPULATE TAG LIST
			tags = []
			file = open('tags.txt', 'a')
			file.close()
			with open('tags.txt') as f:
				lines = f.readlines()
			
			# LOAD THE LIST OF TAGS
			for line in lines:
				tags.append(str(line).replace('\n', ''))
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+W+'ACTION'+W+'] Tags loaded -> ' + str(len(tags)))


			for tag in tags:
				# GET BOT TODO LIST READY
				media = get_media_by_tag(s, str(tag))
				for med in media:
					if med not in ready_to_like:
						ready_to_like.append(med)
				print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] Media loaded -> ' + str(len(ready_to_like)))
					
				# GET MEDIA OWNERS
				owners = get_media_info(media)
				for own in owners:
					if own not in ready_to_follow:
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
			print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+G+'NOTICE'+W+'] Finished retrieving all media | Waiting for next cycle to retrieve more')
		else:
			time.sleep(30)

except KeyboardInterrupt:
	logout(obj, s, token)
	sys.exit()
