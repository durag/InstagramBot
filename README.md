# InstagramBot
This bot is not complete.
The creators of Instabot are credited with creating the login portion of this code
and the list of URLs used for liking and following.

I am not the most familiar with the requests module so the existing code helped me
to hit the ground running on this project.

So huge shoutout to those guys.


# Requirements
```pip install requests```


# Tags
To make your own list of tags for the bot to use when liking and following,
create a file in the same directory as ```bot.py``` and name it ```tags.txt```

Inside this file, place a return separated list of tags like so...

```
hack
hacking
computer
tech
technology
code
virus
follow4follow
ratemysetup
```
You can expect anywhere between 15-20 posts loaded from a single tag
and out of those posts, anywhere between 12-20 unique instagram pages


# Adjusting Rate
If you would like to adjust the rate at which the bot will like and follow,
you can change a couple of values in the script

```python
# THIS FUNCTION IS FOR CONTROLLING FOLLOW RATE
def follow_time(s, obj):
	while 1:
		for owner in ready_to_follow:
			follow_owner_list(s, owner, obj)
			ready_to_follow.remove(owner)
			time.sleep(30) # <---- CHANGE THE 30 TO WHATEVER TIME YOU WANT IN SECONDS
	time.sleep(5)

# THIS FUNCTION IS FOR CONTROLLING LIKE RATE
def like_time(s):
	while 1:
		for med in ready_to_like:
			like_media_list(s, med)
			ready_to_like.remove(med)
			time.sleep(5) # <---- CHANGE THE 5 TO WHATEVER TIME YOU WANT IN SECONDS
	time.sleep(5)
```

By default, the script will follow a page every 30 seconds and like a picture every 5 seconds.
Since this script is multi-threaded, the rate for liking does not affect the rate for following or vice versa.


# Results
![alt text](https://github.com/the-red-team/InstagramBot/blob/master/bot_capture.PNG "Bot running on fake account I created using another python script")

The bot will pull your following and follower counts from Instagram every 5 minutes to update you on the current status of your account.

It will also show you how many pictures it has liked, how many pages it has followed, and how many of both it has left to go through.


# Future Updates
At the moment this script will run through a list of tags, like the pictures associated with them, and following the pages who own those pictures. Once the list of tags is complete, the script will finish.

My next update to this script will be to make it so the script will reload those tags upon completion so it will continue to like and follow and never stop unless interrupted by the user which will make it completely automated.

I also intend to make the script continuously reload the ```tags.txt``` file so a user could add tags on-the-fly to ensure the bot will pull new tags even from a single run, making the bot more dynamic.

I would also like this script to keep track of whether or not a page which the bot has followed, follows back.
