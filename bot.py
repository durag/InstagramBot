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


# POSSIBLE BAN
error_400 = 0
# PROBABLE BAN
error_400_to_ban = 3

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
	

# FUNCTION TO RESOLVE USERNAME TO INSTAGRAM ID
def get_user_id_by_login(s, username):
	info_url = 'https://www.instagram.com/' + str(username) + '/?__a=1'
	info = s.get(info_url)
	data = json.loads(info.text)
	id = data['user']['id']
	return id
	
# FUNCTION TO GET FOLLOWER/FOLLOWS COUNT
def get_follow_counts(s, username):
	url = 'https://www.instagram.com/' + str(username) + '/?__a=1'
	try:
		r = s.get(url)
		user_info = json.loads(r.text)

		follows = user_info['user']['follows']['count']
		followers = user_info['user']['followed_by']['count']
		
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
		
		
def keep_alive():
	while 1:
		time.sleep(1)
		
try:
	try:
		obj = bot()
		bot.username = str(sys.argv[1])
		bot.password = str(sys.argv[2])
		
		# LOGIN AND GET USER INFO
		s, token = login(obj)
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Followers -> ' + str(obj.followers))
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Following -> ' + str(obj.following))
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+C+'INFO'+W+'] Instagram ID -> ' + str(obj.id))
		
		# GET BOT TODO LIST READY
		media = get_media_by_tag(s, sys.argv[3])
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+T+'ACTION'+W+'] Media loaded -> ' + str(len(media)))
		
		
		# DON'T DIE
		keep_alive()
	except Exception, e:
		print('[' + str(datetime.now().date()) + '|' + str(datetime.now().time()) + '] ['+R+'ERROR'+W+'] There was an error -> ' + str(e))
		sys.exit()
except KeyboardInterrupt:
	logout(obj, s, token)
	sys.exit()
